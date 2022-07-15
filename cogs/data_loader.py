import discord
from discord.ext import commands
from bin import file_loader

class option(commands.Cog) :
    def __init__(self, bot) :
        self.bot = bot

    @commands.command()
    async def list_server(self, ctx) :
        for i in file_loader.server_id :
            print(self.bot.get_guild(i))
    
        await ctx.send("test")
        

def setup(bot) :
    bot.add_cog(option(bot))