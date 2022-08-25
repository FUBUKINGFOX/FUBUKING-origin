import discord
import random
import time
from discord.ext import commands
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


def setup(bot):
    bot.add_cog(test(bot))