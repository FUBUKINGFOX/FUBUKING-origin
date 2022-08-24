import imp
import discord
import random
import time
from discord.ext import commands
class test(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot

    @commands.command(name='test', description="")
    async def test_(self, ctx, list: str) :
        list_ = list.replace(","," ").split()
        list_ = " ".join(str(i) for i in list_)
        
        await ctx.send(f"> 你的選擇有:\n {list_}")
        ans = random.choice(list)
        time.sleep(1)

        await ctx.send(f"> 最後我幫你選擇了\n{ans}")


def setup(bot):
    bot.add_cog(test(bot))