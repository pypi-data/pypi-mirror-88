# UBPY
# UniqueBot 파이썬 **비공식** SDK입니다. 
### SaidBySolo님의 KoreanBots비공식 sdk레포의 일부를 사용해 제작되었습니다. [URL](<https://github.com/SaidBySolo/DBKR-API-Python>)

### 현재는 길드수업데이트 모듈만 존재합니다, 이 모듈은 자동으로 1시간마다 자동으로 요청을 보내고 따로 길드수를 비교하는 함수는 필요가 없습니다.

### 파이썬 3.6이상을 필요로 합니다.

**Using Cogs**
```py
from UBPY import PostGuilds
import discord
from discord.ext import commands

class GuildCount(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = "UniqueBot TOKEN"
        PostGuilds.UpdateGuilds(self.bot,self.token)

def setup(bot):
    bot.add_cog(GuildCount(bot))
```
