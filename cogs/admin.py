import discord
from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def cmd(self, ctx):
        pass

def setup(bot):
    bot.add_cog(admin(bot))