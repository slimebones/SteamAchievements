import httpx
from typing import TYPE_CHECKING
from orwynn.mongo import Query

from pydantic import BaseModel
from pykit.log import log
from src.achievement import AchievementDoc

from src.game import GameDoc

if TYPE_CHECKING:
    from src.user import UserDoc

class PlatformProcessorArgs(BaseModel):
    user: "UserDoc"
    platform_user_sid: str
    api_token: str

class PlatformProcessor:
    async def process(self, args: PlatformProcessorArgs):
        raise NotImplementedError

class SteamUrls:
    GET_PLAYER_ACHIEVEMENTS = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_token}&steamid={steam_id}"
    GET_OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_token}&steamid={steam_id}&format=json"

class SteamPlatformProcessor(PlatformProcessor):
    async def process(self, args: PlatformProcessorArgs):
        async with httpx.AsyncClient() as client:
            res = await client.get(SteamUrls.GET_OWNED_GAMES.format(
                steam_id=args.platform_user_sid,
                api_token=args.api_token))
            if res.status_code >= 400:
                log.err(
                    "err occured during http req to get owned games:"
                    + f" {res.text}"
                    " => abort processing of steam platform")
                return
            data = res.json()
            for rawgame in data["response"]["games"]:
                platform = "steam"
                key = str(rawgame["appid"])
                playtime = float(rawgame["playtime_forever"])
                # name will be fetched later during achievements request
                name = ""

                game, is_created = GameDoc(
                    platform=platform,
                    key=key,
                    playtime=playtime,
                    name=name
                ).get_or_create(Query({
                    "platform": platform,
                    "key": key
                }))
                if not is_created:
                    game = game.upd(Query.as_upd(
                        set={"playtime": playtime, "name": name}
                    ))
                achievements_res = await self._try_create_or_upd_achievements(
                    game, args)
                if not achievements_res:
                    return
                game, achievements = achievements_res

    async def _try_create_or_upd_achievements(
        self,
        game: GameDoc,
        args: PlatformProcessorArgs
    ) -> tuple[GameDoc, list[AchievementDoc]] | None:
        async with httpx.AsyncClient() as client:
            res = await client.get(SteamUrls.GET_PLAYER_ACHIEVEMENTS.format(
                steam_id=args.platform_user_sid,
                api_token=args.api_token,
                app_id=game.key))
            if res.status_code >= 400:
                log.err(
                    f"err occured during http req to get achievements for game"
                    + f"{game.key}: {res.text}"
                    " => abort further processing of steam platform")
                return None
            data = res.json()["playerstats"]

            # upd game name since it appear only on achievements gathering
            game = game.upd(Query.as_upd(set={"name": data["gameName"]}))
            achievements = []
            for raw_achievement in data["achievements"]:
                key = raw_achievement["apiname"]
                # todo: find out friendly name, icon url from
                #       external sources, and rarity from steam info
                #       (global achievements API)
                name = key
                is_achieved = raw_achievement["achieved"] == 1
                completion_time = float(raw_achievement["unlocktime"])
                if not is_achieved:
                    completion_time = None
                achievement, is_created = AchievementDoc(
                        key=key,
                        name=name,
                        completion_time=completion_time) \
                    .get_or_create(Query({
                        "key": key
                    }))

                if not is_created:
                    assert \
                        achievement.sid in game.achievement_sids, \
                        f"already created achievement {achievement.key}" \
                                f"should be part of game {game.key}"
                    achievement = achievement.upd(Query.as_upd(set={
                        "name": name,
                        "completion_time": completion_time
                    }))

                game = game.upd(Query.as_upd(push={
                    "achievement_sids": achievement.sid
                }))
                achievements.append(achievement)

            return game, achievements

PLATFORM_TO_PROCESSOR: dict[str, PlatformProcessor] = {
    "steam": SteamPlatformProcessor()
}
PLATFORMS = list(PLATFORM_TO_PROCESSOR.keys())
