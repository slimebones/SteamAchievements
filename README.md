# Steam Achievements
Tracks steam achievements.

## Steam-API-Specific Rate Limits
ISteamUser: 100 requests per minute
ISteamFriends: 100 requests per minute
ISteamUserStats: 100 requests per minute
ISteamCommunity: 100 requests per minute
ISteamApps: 500 requests per minute
ISteamEconomy: 500 requests per minute

This means we need to collect data gradually, not in one shot. For example launch long-term task, which will collect user data in 10 minutes.

## References
* https://steamapi.xpaw.me/
