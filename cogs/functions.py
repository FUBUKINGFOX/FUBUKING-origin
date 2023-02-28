import discord
from discord.ext import commands
from bin.class_init.cog_init import cog_init
import time
from bin import config_loader
from bin.public import var
class functions(cog_init):
    @commands.command()
    async def cha_happa(self, ctx) :
        time.sleep(1)
        await ctx.message.delete()
        await ctx.send('<:cha:1028744563411656734><:happa:1028744605807681536>')








    #===========================


    @commands.command(aliases=["fuck"])
    async def msg_handler(self, ctx) :
        time.sleep(1)
        await ctx.message.delete()
        await ctx.send('<:OKO:1028581472749240362>')
        try :
            await ctx.author.move_to(channel=None)
        except Exception :
            pass
    
     #=========================== 
    @commands.command()
    @commands.is_owner()
    async def send_update_msg(self, ctx):
        embed = discord.Embed(
            title="BUG FIX",
            color=0xff00e1,
            description="bug 修復"
            
        ).add_field(name="module fix" ,value="youtube-dl ==> yt-dlp")
        i = config_loader.load_playchannel()
        for i in i :
            id =  self.bot.get_channel(i)
            await id.send(embed=embed)
            time.sleep(0.5)
        


async def setup(bot) :
    await bot.add_cog(functions(bot))