import discord
from discord.ext import commands
from bin.public import var
from bin.class_init.cog_init import cog_init

class admin(cog_init):
    
    @commands.command(name="closed_beta",aliases=['cb'], description="closed_beta")
    @commands.is_owner()
    async def closed_beta_(self, ctx):
        game = discord.Activity(type=discord.ActivityType.watching, name='開發者封測')
        await self.bot.change_presence(status=discord.Status.dnd, activity=game)
        embed = discord.Embed(title="==封閉測試==", description="機器人封測中", color=0xff0000)
        await ctx.send(embed=embed)


    @commands.command(name="un_closed_beta",aliases=['ucb'], description="un_closed_beta")
    @commands.is_owner()
    async def un_closed_beta_(self, ctx):
        game = discord.Activity(type=discord.ActivityType.listening, name='YouTube')
        await self.bot.change_presence(status=discord.Status.idle, activity=game)
        embed = discord.Embed(title="==解除封閉測試==", description="", color=0x00ff15)
        await ctx.send(embed=embed)

    @commands.command(name="v_kick", description="kick member from voice_channel")
    @commands.is_owner()
    async def v_kick(self, ctx, member: discord.Member):

        await member.move_to(channel=None)

        await ctx.send("<:OKO:1028581472749240362>")
        embed = discord.Embed(title=(f'已將{member}踢出語音頻道'), color=0xff0000)
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(admin(bot))