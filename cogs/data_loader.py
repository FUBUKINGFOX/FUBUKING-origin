import discord
from discord.ext import commands
from bin import config_loader
from bin.class_init.cog_init import cog_init

class option(cog_init) :

    @commands.command()
    async def list_server(self, ctx) :
        embed = discord.Embed(title="Server list", description="", color=0xf700ff)
        embed.set_author(icon_url=self.bot.user.avatar_url, name=f"CORN Studio _Data_loader")
        for i in config_loader.load_server_id() :
            embed.add_field(name=self.bot.get_guild(i), value=f"```{i}```", inline=False)
            
    
        await ctx.send(embed=embed)


    @commands.command()
    async def list_playchannel(self, ctx) :
        embed = discord.Embed(title="Play_channel list", description="", color=0xf700ff)
        embed.set_author(icon_url=self.bot.user.avatar_url, name=f"CORN Studio _Data_loader")
        for i in config_loader.load_playchannel() :
            embed.add_field(name=self.bot.get_channel(i), value=f"```{i}```", inline=False)
            
    
        await ctx.send(embed=embed)
        

async def setup(bot) :
    await bot.add_cog(option(bot))