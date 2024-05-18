import asyncio
from typing import Any, Literal

from orwynn.dto import Udto
from orwynn.mongo import (
    CreateDocReq,
    DelDocReq,
    Doc,
    DocField,
    GetDocsReq,
    Query,
    UpdDocReq,
    filter_collection_factory,
)
from orwynn.sys import Sys
from pykit.dt import DtUtils
from pykit.err import AlreadyProcessedErr, InpErr, ValErr
from pykit.fcode import code
from pykit.log import log
from rxcat import Evt, OkEvt, Req

TimerStatus = Literal["tick", "paused", "finished"]

class TimerUdto(Udto):
    current_duration: float
    total_duration: float
    last_launch_time: float
    finish_sound_asset_sid: str | None
    status: TimerStatus

class TimerDoc(Doc):
    COLLECTION_NAMING = "snake_case"

    current_duration: float = 0.0
    """
    This is written only on status change. Clients should calc it themselves
    and verify on timer changes.
    """
    last_launch_time: float = 0.0
    """
    When last tick status was assigned to a timer.

    It's helpful to measure how long from the currentDuration the timer is
    ticking.
    """
    total_duration: float
    status: TimerStatus = "paused"

    finish_sound_asset_sid: str | None = None

    def to_udto(self) -> TimerUdto:
        return TimerUdto(
            sid=self.sid,
            current_duration=self.current_duration,
            total_duration=self.total_duration,
            last_launch_time=self.last_launch_time,
            finish_sound_asset_sid=self.finish_sound_asset_sid,
            status=self.status
        )

TimerEndActionType = Literal["none", "start_next"]
TimerEndActionData = dict[
        str, TimerEndActionType | str | int | float]
TimerGroupEndActionType = Literal["none", "restart", "start_another"]
TimerGroupEndActionData = dict[
        str, TimerGroupEndActionType | str | int | float]

class TimerGroupUdto(Udto):
    name: str
    timer_sids: list[str]
    current_timer_index: int
    timer_end_action: TimerEndActionData
    group_end_action: TimerGroupEndActionData

class TimerGroupDoc(Doc):
    COLLECTION_NAMING = "snake_case"
    FIELDS = [
        DocField(name="name", unique=True),
        DocField(name="timer_sids", linked_doc="timer_doc")
    ]

    name: str
    timer_sids: list[str] = []
    current_timer_index: int = 0
    timer_end_action: TimerEndActionData = {"type": "none"}
    group_end_action: TimerGroupEndActionData = {"type": "none"}

    def to_udto(self) -> TimerGroupUdto:
        return TimerGroupUdto(
                sid=self.sid,
                name=self.name,
                timer_sids=self.timer_sids,
                current_timer_index=self.current_timer_index,
                timer_end_action=self.timer_end_action,
                group_end_action=self.group_end_action)

@code("start_timer_req")
class StartTimerReq(Req):
    sid: str

@code("started_timer_evt")
class StartedTimerEvt(Evt):
    sid: str

@code("stopped_timer_evt")
class StoppedTimerEvt(Evt):
    sid: str

@code("stop_timer_req")
class StopTimerReq(Req):
    sid: str

@code("finished_timer_evt")
class FinishedTimerEvt(Evt):
    udto: TimerUdto

class TimerGroupSys(Sys):
    CommonSubMsgFilters = [
        filter_collection_factory(TimerGroupDoc.get_collection())
    ]

    async def enable(self):
        self._timer_sid_to_tick_task: dict[str, asyncio.Task] = {}

        await self._sub(GetDocsReq, self._on_get_docs)
        await self._sub(CreateDocReq, self._on_create_doc)
        await self._sub(UpdDocReq, self._on_upd_doc)
        await self._sub(DelDocReq, self._on_del_doc)
        await self._sub(FinishedTimerEvt, self._on_finished_timer)

    async def _on_finished_timer(self, evt: FinishedTimerEvt):
        group = TimerGroupDoc.try_get(Query({
            "timer_sids": {"$in": evt.udto.sid}}))
        if group is None:
            log.err(f"cannot find group for finished timer {evt.udto}")
            return

        group.current_timer_index += 1
        if group.current_timer_index >= len(group.timer_sids):
            group.current_timer_index = 0

        if group.timer_sids[-1] == evt.udto.sid:
            if group.group_end_action["type"] == "restart":
                group.current_timer_index = 0
                await self._pub(StartTimerReq(sid=group.timer_sids[0]))
            if group.group_end_action["type"] == "start_another":
                raise NotImplementedError

            return

        if group.timer_end_action["type"] == "start_next":
            await self._pub(StartTimerReq(
                sid=group.timer_sids[group.current_timer_index]))

        group.upd(Query.as_upd(set={
            "current_timer_index": group.current_timer_index}))

    async def _on_get_docs(self, req: GetDocsReq):
        docs = list(TimerGroupDoc.get_many(req.searchQuery))
        await self._pub(TimerGroupDoc.to_got_doc_udtos_evt(req, docs))

    async def _on_create_doc(self, req: CreateDocReq):
        doc = TimerGroupDoc(**req.createQuery).create()
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_upd_doc(self, req: UpdDocReq):
        doc = TimerGroupDoc.get_and_upd(req.searchQuery, req.updQuery)
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_del_doc(self, req: DelDocReq):
        doc = TimerGroupDoc.get(req.searchQuery)

        # on group deletion - delete all timers
        for timer_sid in doc.timer_sids:
            await self._pub(DelDocReq(collection="timerDoc",
                                      searchQuery=Query({"sid": timer_sid})))

        doc.delete()
        await self._pub(OkEvt(rsid="").as_res_from_req(req))

class TimerSys(Sys):
    CommonSubMsgFilters = [
        filter_collection_factory(TimerDoc.get_collection())
    ]

    async def enable(self):
        self._timer_sid_to_tick_task: dict[str, asyncio.Task] = {}

        await self._sub(GetDocsReq, self._on_get_docs)
        await self._sub(CreateDocReq, self._on_create_doc)
        await self._sub(UpdDocReq, self._on_upd_doc)
        await self._sub(DelDocReq, self._on_del_doc)
        await self._sub(StartTimerReq, self._on_start_timer)
        await self._sub(StopTimerReq, self._on_stop_timer)

    def _create_tick_task_for_timer(self, timer_doc: TimerDoc, orig_req: Req):
        if timer_doc.sid in self._timer_sid_to_tick_task:
            raise AlreadyProcessedErr(f"tick task for timer {timer_doc}")
        self._timer_sid_to_tick_task[timer_doc.sid] = asyncio.create_task(
            self._tick_timer(
                timer_doc.sid,
                timer_doc.current_duration,
                timer_doc.total_duration,
                orig_req
            )
        )

    def _try_stop_tick_task_for_timer(self, sid: str) -> bool:
        task = self._timer_sid_to_tick_task.get(sid, None)
        if not task:
            return False
        task.cancel()
        return True

    async def _stop_all_timers(self):
        for sid, task in self._timer_sid_to_tick_task.items():
            task.cancel()
            await self._finish_timer(sid, None)

    async def _finish_timer(self, sid: str, orig_req: Req | None):
        timer_doc = TimerDoc.get(Query({"sid": sid}))
        if timer_doc.status != "tick":
            raise ValErr(
                f"timer status must be \"tick\", got {timer_doc.status}"
            )

        timer_doc = timer_doc.upd(Query.as_upd(
            set={
                "status": "finished",
                "current_duration": 0.0
            }
        ))
        finished_evt = FinishedTimerEvt(
            rsid="",
            udto=timer_doc.to_udto()
        )
        if orig_req:
            finished_evt = finished_evt.as_res_from_req(orig_req)
        await self._pub(finished_evt)

    async def _tick_timer(
        self,
        sid: str,
        current_duration: float,
        total_duration: float,
        orig_req: Req
    ):
        delta_duration = total_duration - current_duration
        if delta_duration > 0:
            await asyncio.sleep(delta_duration)
        await self._finish_timer(sid, orig_req)

    async def _on_start_timer(self, req: StartTimerReq):
        timer_doc = TimerDoc.get(Query({"sid": req.sid}))
        if timer_doc.status == "tick":
            raise AlreadyProcessedErr(f"timer {timer_doc} start")

        setq: dict[str, Any] = {
            "status": "tick"
        }
        # restart ticked duration upon starting a finished timer again
        if timer_doc.status == "finished":
            setq["current_duration"] = 0.0

        # it's ok here to pass not upded yet timer doc, an err may happen here,
        # so we don't want to upd the mongo doc before this point
        self._create_tick_task_for_timer(timer_doc, req)
        setq["last_launched_time"] = DtUtils.get_utc_timestamp()

        timer_doc = timer_doc.upd(Query.as_upd(set=setq))
        await self._pub(timer_doc.to_got_doc_udto_evt(req))
        await self._pub(StartedTimerEvt(rsid=req.sid, sid=timer_doc.sid))

    async def _on_stop_timer(self, req: StopTimerReq):
        timer_doc = TimerDoc.get(Query({"sid": req.sid}))
        if timer_doc.status != "tick":
            raise InpErr(
                f"on timer with status {timer_doc.status}, an attempt to stop"
            )
        self._try_stop_tick_task_for_timer(timer_doc.sid)

        now_timestamp = DtUtils.get_utc_timestamp()
        assert timer_doc.last_launch_time > 0.0
        passed_delta = now_timestamp - timer_doc.last_launch_time
        new_current_duration = timer_doc.current_duration + passed_delta
        assert new_current_duration < timer_doc.total_duration

        setq: dict[str, Any] = {
            "status": "paused",
            "current_duration": new_current_duration
        }
        timer_doc = timer_doc.upd(Query.as_upd(set=setq))
        await self._pub(timer_doc.to_got_doc_udto_evt(req))

    async def _on_get_docs(self, req: GetDocsReq):
        docs = list(TimerDoc.get_many(req.searchQuery))
        await self._pub(TimerDoc.to_got_doc_udtos_evt(req, docs))

    async def _on_create_doc(self, req: CreateDocReq):
        q = req.createQuery.copy().disallow(
            "current_duration",
            "last_launched_time"
            "status",
            raise_mod="warn"
        )
        doc = TimerDoc(**q).create()
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_upd_doc(self, req: UpdDocReq):
        updq = req.updQuery.copy().disallow(
            "current_duration",
            "last_launched_time",
            "status",
            raise_mod="warn"
        )
        doc = TimerDoc.get(req.searchQuery)
        if doc.status == "tick":
            # reset timer on any upd
            doc.status = "paused"
            doc.current_duration = 0.0
            doc.last_launch_time = 0.0
        doc = doc.upd(updq)
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_del_doc(self, req: DelDocReq):
        doc = TimerDoc.get(req.searchQuery)
        if doc.status == "tick":
            await self._pub(StopTimerReq(sid=doc.sid))
        doc.delete()
        await self._pub(OkEvt(rsid="").as_res_from_req(req))

