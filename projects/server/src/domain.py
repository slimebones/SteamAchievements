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

from src.color import ColorPalette


class FocusDomainUdto(Udto):
    name: str
    color_palette: ColorPalette
    timer_sids: list[str] = []

class FocusDomainDoc(Doc):
    FIELDS = [DocField(name="name", unique=True)]
    name: str
    color_palette: ColorPalette
    timer_sids: list[str] = []

    def to_udto(self) -> FocusDomainUdto:
        return FocusDomainUdto(
                sid=self.sid,
                name=self.name,
                timer_sids=self.timer_sids,
                color_palette=self.color_palette)

class FocusDomainSys(Sys):
    CommonSubMsgFilters = [
        filter_collection_factory(FocusDomainDoc.get_collection())
    ]

    async def enable(self):
        self._timer_sid_to_tick_task: dict[str, asyncio.Task] = {}

        await self._sub(GetDocsReq, self._on_get_docs)
        await self._sub(CreateDocReq, self._on_create_doc)
        await self._sub(UpdDocReq, self._on_upd_doc)
        await self._sub(DelDocReq, self._on_del_doc)

    async def _on_get_docs(self, req: GetDocsReq):
        docs = list(FocusDomainDoc.get_many(req.searchQuery))
        await self._pub(FocusDomainDoc.to_got_doc_udtos_evt(req, docs))

    async def _on_create_doc(self, req: CreateDocReq):
        doc = FocusDomainDoc(**req.createQuery).create()
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_upd_doc(self, req: UpdDocReq):
        doc = FocusDomainDoc.get_and_upd(req.searchQuery, req.updQuery)
        await self._pub(doc.to_got_doc_udto_evt(req))

    async def _on_del_doc(self, req: DelDocReq):
        doc = FocusDomainDoc.get(req.searchQuery)
        doc.delete()
        await self._pub(OkEvt(rsid="").as_res_from_req(req))

