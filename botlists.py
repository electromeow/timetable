import aiohttp
import json

TOPGGBASE = "https://top.gg/api/bots/789202881336311849"
BOTSGGBASE = "https://discord.bots.gg/api/v1/bots/789202881336311849"
DBLBASE = "https://discordbotlist.com/api/v1/bots/789202881336311849"
DBOATSBASE = "https://discord.boats/api/bot/789202881336311849"

class BotLists:
    def __init__(self, db):
        f = open("botlisttokens.json",'r')
        self.tokens = json.load(f)
        f.close()
        self.db = db
        self.session = aiohttp.ClientSession()
    """
    async def isVoted(uid):
        if self.db.checkVotedUser(uid):
            return True
        else:
            resp = await self.session.get(TOPGGBASE+f"/check?userId={uid}", headers={"Authorization": self.tokens["topgg"]})
            resp = json.loads(await resp.text())
            if resp["voted"] > 0:
                self.db.addVotedUser(uid)
                return True
            else:
                return False
    Will be used when bot is approved in top.gg
    """
    async def postServerCount(self, svcount):
        """
        self.session.post(TOPGGBASE+"/stats",
            headers={"Authorization":self.tokens["topgg"]},
            data={"server_count":svcount})
        Will be used when bot is approved in top.gg
        """
        await self.session.post(BOTSGGBASE+"/stats",
            headers={"Authorization":self.tokens["botsgg"]},
            data={"guildCount":svcount})
        await self.session.post(DBLBASE+"/stats",
            headers={"Authorization":self.tokens["discordbotlist"]},
            data={"guilds":svcount})
        await self.session.post(DBOATSBASE,
            headers={"Authorization":self.tokens["discordboats"]},
            data={"server_count":svcount})
