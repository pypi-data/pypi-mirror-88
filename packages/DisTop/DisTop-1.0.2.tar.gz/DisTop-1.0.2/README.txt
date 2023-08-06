# DisTop
The official Python Library for the [distop.xyz](https://distop.xyz) website!

# Installation
## Install via pip (Recommended)
```from DisTop import DisTop```


# Examples
## Post stats
With Tasks (Must be using discord.py version 1.1.0+):
```python
import discord, asyncio
from DisTop import DisTop
from discord.ext import tasks

class DisTop(commands.Cog):
    """Interacts with the DisTop API"""

    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()
        self.DisTop = DisTop(token=token)# Make sure you put your token from DisTop.xyz here!

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30.0)
    async def update_stats(self):
        """This automatically updates your server count to DisTop.xyz every 30 minutes."""
        try:
            await DisTop.post_stats(self.bot.user.id, len(self.bot.guilds))
        except Exception as e:
            print('Failed to post server count to DisTop.xyz\n' + type(e).__name__ + ':' + e')

def setup(bot):
    bot.add_cog(DisTop(bot))
```
