import json
import os
import httpx

from server.models import Achievement, PlayerGameAchievements
from server.utils import Result, is_error

GET_PLAYER_ACHIEVEMENTS = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_key}&steamid={steam_id}"
GET_OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
GET_RECENTLY_PLAYED_GAMES = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
GET_USER_STATS_FOR_GAME = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={app_id}&key={api_key}&steamid={steam_id}&format=json"
GET_GLOBAL_ACHIEVEMENT_PERCENTAGES_FOR_APP = "http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={app_id}&format=json"
GET_NEWS_FOR_APP = "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={app_id}&count=3&format=json"
GET_PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}&format=json"
GET_SCHEMA_FOR_GAME = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2?key={api_key}&appid={app_id}"

API_KEY = ""

def _get_owned_game_ids(steam_id: str) -> set[str]:
    response = httpx.get(
        GET_OWNED_GAMES.format(steam_id=steam_id, api_key=API_KEY)
    )
    data = response.json()
    games = data["response"]["games"]
    game_ids = set()
    for game in games:
        game_ids.add(game["appid"])
    return game_ids

def _get_player_achievements(
        steam_id: str, game_id: str
    ) -> Result[PlayerGameAchievements]:
    response = httpx.get(
        GET_PLAYER_ACHIEVEMENTS.format(
            steam_id=steam_id, api_key=API_KEY, app_id=game_id
        )
    )
    if response.status_code >= 400:
        return Exception()
    data = response.json()["playerstats"]
    achievements = []
    raw_achievements = data.get("achievements")
    if not raw_achievements:
        return Exception()
    achieved_count = 0
    for raw_achievement in raw_achievements:
        achievement = Achievement(
            key=raw_achievement["apiname"],
            is_achieved=raw_achievement["achieved"] == 1,
            unlock_time=raw_achievement["unlocktime"] * 1000,
        )
        if achievement.is_achieved:
            achieved_count += 1
        achievements.append(achievement)
    completion = achieved_count / len(achievements)
    game_achievements = PlayerGameAchievements(
        steam_id=data["steamID"],
        game_name=data["gameName"],
        achievements=achievements,
        completion=completion,
    )
    return game_achievements

def _calculate_average_completion(steam_id: str) -> float:
    """
    Collect all achievements for a steam id, calculate completion per game,
    then arithmetic average for all owned games.
    """
    game_ids = _get_owned_game_ids(steam_id)
    game_total_len = len(game_ids)
    print(f"Got {len(game_ids)} owned games.")
    completions: list[float] = []
    i = 0
    for game_id in game_ids:
        i += 1
        game_achievements = _get_player_achievements(steam_id, game_id)
        if is_error(game_achievements):
            continue
        completed_count = 0
        for achievement in game_achievements.achievements:
            if achievement.is_achieved:
                completed_count += 1
        completions.append(
            completed_count / len(game_achievements.achievements)
        )
        print(
            f"[{i}/{game_total_len}] Got {len(game_achievements.achievements)}"
            f" achievements for a game `{game_achievements.game_name}`"
            f" (Completion {game_achievements.completion*100:.1f}%)."
        )
    return sum(completions) / len(completions)

def _get_game_schema(game_id: str):
    response = httpx.get(
        GET_SCHEMA_FOR_GAME.format(api_key=API_KEY, app_id=game_id)
    )
    json.dump(response.json(), open("examples/game_schema.json", "w"))

def main():
    global API_KEY
    API_KEY = os.getenv("STEAM_API_KEY", None)
    if API_KEY is None:
        print("Define STEAM_API_KEY.")
        exit(1)

    _get_game_schema("220")
    # steam_id = "76561198016051984"
    # print(_calculate_average_completion(steam_id))

if __name__ == "__main__":
    main()
