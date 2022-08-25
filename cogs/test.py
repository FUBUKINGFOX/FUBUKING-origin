import discord
import requests as req
import random
import time
from discord.ext import commands
class methods():
    def req_covic():
        url = "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"
        r = req.get(url).text
        return r


class test(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot

    @commands.command(name='choice', aliases=["ce"], description="")
    async def choice_(self, ctx, list: str) :
        list_ = list.replace(","," ").split()
        ans = random.choice(list_)
        list_ = " ".join(str(i) for i in list_)
        
        await ctx.send(f"> 你的選擇有:\n {list_}")
        time.sleep(1)

        await ctx.send(f"> 最後我幫你選擇了:\n{ans}")

    @commands.command(name='covic', description="")
    async def covic_(self, ctx):
        await ctx.send("test")
        print(methods.req_covic())



def setup(bot):
    bot.add_cog(test(bot))