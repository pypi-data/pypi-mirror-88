import aiohttp

class DisTop:
    def __init__(self, token):
        self.token = token

    async def post_stats(self, bot_id, guild_count:int):
        async with aiohttp.ClientSession() as session:
            async with session.post('https://distop.xyz/api/update' + str(bot_id),
            headers={'Authorization': str(self.token)},
            data={"guilds": guild_count}) as r:
                return await r.json()

    async def get_stats(self, bot_id):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://distop.xyz/api/bot' + str(bot_id)) as r:
                return await r.json()
    
