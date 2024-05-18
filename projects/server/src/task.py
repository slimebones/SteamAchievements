from orwynn.dto import Udto
from orwynn.mongo import (
    CreateDocReq,
    DelDocReq,
    Doc,
    GetDocsReq,
    UpdDocReq,
    filter_collection_factory,
)
from orwynn.sys import Sys
from pykit.dt import DtUtils
from rxcat import OkEvt


class TaskUdto(Udto):
    text: str
    is_completed: bool
    completion_time: float

class TaskDoc(Doc):
    text: str
    isCompleted: bool = False
    completionTimestamp: float = 0.0

    def to_udto(self) -> TaskUdto:
        return TaskUdto(
            sid=self.sid,
            text=self.text,
            is_completed=self.isCompleted,
            completion_time=self.completionTimestamp
        )

class TaskSys(Sys):
    CommonSubMsgFilters = [
        filter_collection_factory(TaskDoc.get_collection())
    ]

    async def enable(self):
        await self._sub(GetDocsReq, self._on_get_docs)
        await self._sub(CreateDocReq, self._on_create_doc)
        await self._sub(UpdDocReq, self._on_upd_doc)
        await self._sub(DelDocReq, self._on_del_doc)

    async def _on_get_docs(self, req: GetDocsReq):
        docs = list(TaskDoc.get_many(req.searchQuery))
        await self._pub(TaskDoc.to_got_doc_udtos_evt(req, docs))

    async def _on_create_doc(self, req: CreateDocReq):
        doc = TaskDoc(**req.createQuery).create()
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_upd_doc(self, req: UpdDocReq):
        if "$set" in req.updQuery and "isCompleted" in req.updQuery["$set"]:
            req.updQuery["$set"]["completionTimestamp"] = \
                DtUtils.get_utc_timestamp()
        doc = TaskDoc.get_and_upd(req.searchQuery, req.updQuery)
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_del_doc(self, req: DelDocReq):
        TaskDoc.get_and_del(req.searchQuery)
        await self._pub(OkEvt(rsid="").as_res_from_req(req))

