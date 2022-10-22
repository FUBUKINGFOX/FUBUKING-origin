from cProfile import label
from tkinter.ttk import Style
from venv import create
import discord
from discord.ext import commands
from bin.class_init.cog_init import cog_init
import time
class functions(cog_init):
    @commands.command()
    async def cha_happa(self, ctx) :
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        await ctx.send('<:cha:1028744563411656734><:happa:1028744605807681536>')

def setup(bot) :
    bot.add_cog(functions(bot))