import os
import requests

GET_PLAYER_ACHIEVEMENTS = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api_key}&steamid={steam_id}"
GET_OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
GET_RECENTLY_PLAYED_GAMES = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
GET_USER_STATS_FOR_GAME = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={app_id}&key={api_key}&steamid={steam_id}&format=json"
GET_GLOBAL_ACHIEVEMENT_PERCENTAGES_FOR_APP = "http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={app_id}&format=json"
GET_NEWS_FOR_APP = "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={app_id}&count=3&format=json"
GET_PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}&format=json"

steam_id = "76561198016051984"

def _calculate_average_completion(steam_id: str) -> float:
    """
    Collect all achievements for a steam id, calculate completion per game,
    then arithmetic average for all owned games.
    """


def main():
    api_key = os.getenv("STEAM_API_KEY", None)
    if api_key is None:
        print("Define STEAM_API_KEY.")
        exit(1)

    response = requests.get(
        # GET_OWNED_GAMES.format(steam_id=steam_id, api_key=api_key)
        # GET_RECENTLY_PLAYED_GAMES.format(steam_id=steam_id, api_key=api_key)
        # GET_USER_STATS_FOR_GAME.format(steam_id=steam_id, api_key=api_key, app_id=1643320)
        # GET_GLOBAL_ACHIEVEMENT_PERCENTAGES_FOR_APP.format(app_id=70)
        GET_NEWS_FOR_APP.format(app_id=1643320)
        # GET_PLAYER_SUMMARIES.format(api_key=api_key, steam_id=steam_id)
    )
    data = response.json()
    print(data)

if __name__ == "__main__":
    main()
