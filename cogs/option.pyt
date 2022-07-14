import discord
from discord.ext import commands

class option(commands.Cog) :
    def __init__(self, bot) :
        self.bot = bot

    @commands.command()
    async def _test(self, ctx) :
        pass

def setup(bot) :
    bot.add_cog(option(bot))