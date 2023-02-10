#== encoding utf-8 ==
import asyncio
import time
import discord
from discord.ext import commands
from bin.class_init.cog_init import cog_init
from bin.public import var
from datetime import datetime

var.var_creat("start_bg",False)

class back_ground_task(cog_init) :
    def __init__(self, *arg, **kwargs) :
        super().__init__(*arg, **kwargs)
        

        async def back_ground():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed() and var.var["start_bg"] == True:



                await asyncio.sleep(1)

        self.bg_task = self.bot.loop.create_task(back_ground())


async def setup(bot):
    await bot.add_cog(back_ground_task(bot))