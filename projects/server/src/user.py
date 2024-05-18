from orwynn.mongo import Doc, DocField, Udto, OkEvt
from orwynn.sys import Sys
from pykit.err import ValueErr
from pykit.query import Query
from rxcat import Req
from pykit.fcode import code

from src.platform import PLATFORMS

class UserUdto(Udto):
    username: str
    global_completion: float
    platform_to_api_token: dict[str, str | None]
    game_sids: list[str]

class UserDoc(Doc):
    COLLECTION_NAMING = "snake_case"
    FIELDS = [
        DocField(name="username", unique=True),
        DocField(name="game_sids", linked_doc="game_doc")
    ]

    username: str
    global_completion: float = 0.0
    platform_to_api_token: dict[str, str | None] = {}
    game_sids: list[str] = []

    def to_udto(self) -> UserUdto:
        return UserUdto(
            sid=self.sid,
            username=self.username,
            global_completion=self.global_completion,
            platform_to_api_token=self.platform_to_api_token,
            game_sids=self.game_sids)

@code("register_platform_api_token_req")
class RegisterPlatformApiTokenReq(Req):
    user_sid: str
    platform: str
    token: str

@code("deregister_platform_api_token_req")
class DeregisterPlatformApiTokenReq(Req):
    user_sid: str
    platform: str

class UserSys(Sys):
    async def enable(self):
        await self._sub(
            RegisterPlatformApiTokenReq, self._on_register_token)
        await self._sub(
            DeregisterPlatformApiTokenReq, self._on_deregister_token)

    async def _on_register_token(self, req: RegisterPlatformApiTokenReq):
        if req.platform not in PLATFORMS:
            raise ValueErr(f"unrecognized platform {req.platform}")

        UserDoc.get_and_upd(
            Query.as_search_sid(req.user_sid),
            Query.as_upd(set={
                f"platform_to_api_token.{req.platform}": req.token}))
        await self._pub(OkEvt(rsid="").as_res_from_req(req))

    async def _on_deregister_token(self, req: DeregisterPlatformApiTokenReq):
        if req.platform not in PLATFORMS:
            raise ValueErr(f"unrecognized platform {req.platform}")
        UserDoc.get_and_upd(
            Query.as_search_sid(req.user_sid),
            Query.as_upd(set={
                f"platform_to_api_token.{req.platform}": None}))
        await self._pub(OkEvt(rsid="").as_res_from_req(req))
