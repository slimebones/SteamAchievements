import asyncio

from orwynn.mongo import (
    CreateDocReq,
    DelDocReq,
    Doc,
    DocField,
    GetDocsReq,
    Sys,
    Udto,
    UpdDocReq,
    filter_collection_factory,
)
from orwynn.rbac import OkEvt


class GameUdto(Udto):
    key: str
    name: str
    completion: float
    platform: str
    icon_url: str | None
    achievement_sids: list[str]

class GameDoc(Doc):
    COLLECTION_NAMING = "snake_case"
    FIELDS = [
        DocField(name="achievement_sids", linked_doc="achievement_doc")
    ]

    key: str
    """
    Association of game with it's main platform.

    E.g. in case of steam, this could be app id.
    """
    platform: str
    name: str
    completion: float
    """
    Calculated on-possibility. Signifies percent of completed achievements, to
    all achievements.
    """
    achievement_sids: list[str] = []
    icon_url: str | None = None

    def to_udto(self) -> GameUdto:
        return GameUdto(
            sid=self.sid,
            key=self.key,
            name=self.name,
            platform=self.platform,
            completion=self.completion,
            icon_url=self.icon_url,
            achievement_sids=self.achievement_sids)

class GameSys(Sys):
    CommonSubMsgFilters = [
        filter_collection_factory(GameDoc.get_collection())
    ]

    async def enable(self):
        await self._sub(GetDocsReq, self._on_get_docs)
        await self._sub(CreateDocReq, self._on_create_doc)
        await self._sub(UpdDocReq, self._on_upd_doc)
        await self._sub(DelDocReq, self._on_del_doc)

    async def _on_get_docs(self, req: GetDocsReq):
        docs = list(GameDoc.get_many(req.searchQuery))
        await self._pub(GameDoc.to_got_doc_udtos_evt(req, docs))

    async def _on_create_doc(self, req: CreateDocReq):
        doc = GameDoc(**req.createQuery).create()
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_upd_doc(self, req: UpdDocReq):
        doc = GameDoc.get_and_upd(req.searchQuery, req.updQuery)
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_del_doc(self, req: DelDocReq):
        doc = GameDoc.get(req.searchQuery)
        doc.delete()
        await self._pub(OkEvt(rsid="").as_res_from_req(req))

