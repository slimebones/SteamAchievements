from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.user import UserDoc

class PlatformProcessor:
    async def process(self, user: UserDoc, api_token: str):
        raise NotImplementedError

class SteamUrls:
    GET_PLAYER_ACHIEVEMENTS = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_token}&steamid={steam_id}"

class SteamPlatformProcessor(PlatformProcessor):
    async def process(self, user: UserDoc, api_token: str):
    # url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}&format=json"

    res = httpx.request("get", url)

    if res.status_code >= 400:
        print(res.text)
        exit(1)

    data = res.json()
    pprint(data)
    with open("out.json", "w") as f:
        json.dump(data, f)

PLATFORM_TO_PROCESSOR: dict[str, PlatformProcessor] = {
    "steam": SteamPlatformProcessor()
}
PLATFORMS = list(PLATFORM_TO_PROCESSOR.keys())
