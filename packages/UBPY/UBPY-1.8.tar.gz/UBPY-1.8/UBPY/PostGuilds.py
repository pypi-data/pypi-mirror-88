import json
import aiohttp
import asyncio
from .PostUrl import mainurl
"""
이 소스는 SaidBySolo님의 KoreanBots비공식 sdk레포의 일부를 사용해 제작되었습니다.
URL: https://github.com/SaidBySolo/DBKR-API-Python
"""

class Client:
    def __init__(self, bot, token, id,log=True):
        """
        클래스 입니다.
        해당 클래스에 인자값을 주시면
        ``main_loop`` 함수가 봇이 꺼질때 까지 루프를 돌아서
        ``post_guild_count``함수를 이용해서 post 요청을 보냅니다.
        log는 로깅 여부입니다 기본값은 True입니다.
        """
        self.bot = bot
        self.token = token
        self.id = id
        loop = asyncio.get_event_loop()
        loop.create_task(self.main_loop(bot, token, id,log))

    async def main_loop(self, bot, token, id,log):
        """
        메인 루프 함수입니다
        봇종료 전까지 30분마다 post_guild_count를 이용해서 post요청을합니다.

        서버수 동일,성공 요청이 아닐시 ``Exception``을 ``raise``합니다.
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            guilds = len(self.bot.guilds)
            getguild = await self.before_guild_count(token, id)
            before = getguild["data"]["bot"]["guilds"]
            if guilds == before:
                if log is True:
                    print("서버수가 동일하네요. 잠시후에 다시요청할께요!")
                    await asyncio.sleep(1800)
                else:
                    await asyncio.sleep(1800)
            elif guilds > before:
                getres = await self.post_guild_count(token, guilds)
                code = getres["data"]["botAccount"]["guilds"]
                if log is True:
                    print(f"서버수를 성공적으로 갱신했어요! 현재 서버수는 {code}이네요.")
                    await asyncio.sleep(1800)
                else:
                    await asyncio.sleep(1800)
            else:
                if log is True:
                    print("서버수가 동일하네요. 잠시후에 다시요청할께요!")
                    await asyncio.sleep(1800)
                else:
                    await asyncio.sleep(1800)


    @staticmethod
    async def post_guild_count(token, guild_count):
        URL = mainurl
        headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
        data = {"query": "query($guilds: Int!) {botAccount {guilds(patch: $guilds)}}",
                "variables": {"guilds": guild_count}}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(URL, headers=headers, json=data) as r:
                response = await r.read()
                sid = response.decode('utf-8')
                answer = json.loads(sid)
                return answer
    
    @staticmethod
    async def before_guild_count(token, id):
        URL = mainurl
        headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
        data = {'query': 'query' '{bot(id:' f"{id}"'){guilds}}'}
        async with aiohttp.ClientSession() as cs:
            async with cs.post(URL, headers=headers, json=data) as r:
                response = await r.read()
                sid = response.decode('utf-8')
                answer = json.loads(sid)
                return answer