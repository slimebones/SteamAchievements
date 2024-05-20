import httpx
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.user import UserDoc

class PlatformProcessor:
    async def process(self, user: "UserDoc", api_token: str):
        raise NotImplementedError

class SteamUrls:
    GET_PLAYER_ACHIEVEMENTS = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_token}&steamid={steam_id}"
    GET_OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_token}&steamid={steam_id}&format=json"

class SteamPlatformProcessor(PlatformProcessor):
    async def process(self, user: "UserDoc", api_token: str):
        pass
        # async with httpx.AsyncClient() as client:
        #     res = client.get(url)
    # res = httpx.request("get", url)

    # if res.status_code >= 400:
    #     print(res.text)
    #     exit(1)

    # data = res.json()
    # pprint(data)
    # with open("out.json", "w") as f:
    #     json.dump(data, f)

PLATFORM_TO_PROCESSOR: dict[str, PlatformProcessor] = {
    "steam": SteamPlatformProcessor()
}
PLATFORMS = list(PLATFORM_TO_PROCESSOR.keys())
