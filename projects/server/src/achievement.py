import asyncio

from orwynn.mongo import (
    CreateDocReq,
    DelDocReq,
    Doc,
    GetDocsReq,
    Sys,
    Udto,
    UpdDocReq,
    filter_collection_factory,
)
from orwynn.rbac import OkEvt


class AchievementUdto(Udto):
    key: str
    name: str
    icon_url: str | None
    rarity: float | None
    completion_time: float | None

class AchievementDoc(Doc):
    COLLECTION_NAMING = "snake_case"

    key: str
    name: str
    rarity: float | None = None
    icon_url: str | None = None
    completion_time: float | None = None

    def to_udto(self) -> AchievementUdto:
        return AchievementUdto(
            sid=self.sid,
            key=self.key,
            name=self.name,
            icon_url=self.icon_url,
            rarity=self.rarity,
            completion_time=self.completion_time)

class FocusDomainSys(Sys):
    CommonSubMsgFilters = [
        filter_collection_factory(AchievementDoc.get_collection())
    ]

    async def enable(self):
        self._timer_sid_to_tick_task: dict[str, asyncio.Task] = {}

        await self._sub(GetDocsReq, self._on_get_docs)
        await self._sub(CreateDocReq, self._on_create_doc)
        await self._sub(UpdDocReq, self._on_upd_doc)
        await self._sub(DelDocReq, self._on_del_doc)

    async def _on_get_docs(self, req: GetDocsReq):
        docs = list(AchievementDoc.get_many(req.searchQuery))
        await self._pub(AchievementDoc.to_got_doc_udtos_evt(req, docs))

    async def _on_create_doc(self, req: CreateDocReq):
        doc = AchievementDoc(**req.createQuery).create()
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_upd_doc(self, req: UpdDocReq):
        doc = AchievementDoc.get_and_upd(req.searchQuery, req.updQuery)
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_del_doc(self, req: DelDocReq):
        doc = AchievementDoc.get(req.searchQuery)
        doc.delete()
        await self._pub(OkEvt(rsid="").as_res_from_req(req))

