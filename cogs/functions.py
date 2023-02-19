import discord
from discord.ext import commands
from bin.class_init.cog_init import cog_init
import time
from bin.public import var
class functions(cog_init):
    @commands.command()
    async def cha_happa(self, ctx) :
        time.sleep(1)
        await ctx.message.delete()
        await ctx.send('<:cha:1028744563411656734><:happa:1028744605807681536>')


    @commands.command()
    async def fuck(self, ctx) :
        time.sleep(1)
        await ctx.message.delete()
        await ctx.send('<:OKO:1028581472749240362>')
        try :
            await ctx.author.move_to(channel=None)
        except Exception :
            pass

    @commands.command()
    async def test_button(self, ctx):
        btn = discord.ui.Button(
            label="press me.",
            style= discord.ButtonStyle.danger
        )
        view = discord.ui.View()
        view.add_item(btn)
        await ctx.send(view=view)
        


async def setup(bot) :
    await bot.add_cog(functions(bot))