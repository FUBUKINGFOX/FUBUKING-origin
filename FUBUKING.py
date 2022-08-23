#== encoding utf-8 ==
from bin import ctc, ctt, key_loader, file_loader
import os
import psutil
import time
import pathlib
import discord
from discord.ext import commands
from discord_slash import SlashCommand
#===============
os.system("cls")
ctc.printSkyBlue("Discord Bot Server [版本 3.0.0.1]\n")
ctc.printDarkSkyBlue("(c) CORN Studio. 著作權所有，並保留一切權利。\n")
ctc.printDarkGray(ctt.time_now())
ctc.printDarkGray("connecting to discord...\n")
#===============bot setting
prefix = ["/","F ","f "]
bot = commands.Bot(command_prefix=prefix, description='FUBUKING music bot.', help_command=None)
slash = SlashCommand(bot, sync_commands=True)
path = str(pathlib.Path(__file__).parent.absolute())
setting = file_loader.setting
server_id = file_loader.server_id
listener_port = (960010657506394132)
#===============cmd
@slash.slash(name="ping",description="Show ping.", guild_ids=server_id)
async def ping(ctx):
    #==========cpu, ram useage
    warn = []
    # CPU usage
    CPU_use = psutil.cpu_percent(interval=0.3)
    # Memory usage
    RAM_use = psutil.virtual_memory()[2]
    #ping
    ping = round(bot.latency*1000)
    #==========embed_color
    if CPU_use > 30 :
        warn.append(f"⚠️[CPU] > 30%")
    if RAM_use > 70 :
        warn.append(f"⚠️[RAM] > 70%")
    if ping > 210 :
        warn.append(f"⚠️[PING] > 210-ms")
    
    if len(warn) >= 3 :
        e_color = 0xff0000
    elif len(warn) == 2 :
        e_color = 0xff6200
    elif len(warn) == 1 :
        e_color = 0xfff700
    else :
        e_color = 0x59ff00

    warn = ((str(warn)[1:-1]).replace(", ", "\n")).replace("'", "")
    
    #==========
    embed = (discord.Embed(title=u'🍵{0.user.name}'.format(bot),
                               description=f'```ini\n[system/INFO]                                            \n```',
                               color=e_color)
                 .add_field(name='💠CPU usage', value=f"{CPU_use}%")
                 .add_field(name='🧱RAM usage', value=f"{RAM_use}%")
                 .add_field(name='📡ping', value=f"{ping}-ms")
                 .set_author(icon_url=bot.user.avatar_url, name=f"CORN Studio"))
    if e_color != 0x59ff00 :
        embed.add_field(name='WARN', value=f"```css\n{warn}```")

    await ctx.send(embed=embed)
    
    ctc.printGreen(u"==============================\n")
    ctc.printYellow("=====>Bot_system\n")
    #time_now(False)
    ctc.printYellow(f'ping:[{round(bot.latency*1000)}]-ms=>[{bot.latency*1000000}]-us\n')
    ctc.printGreen(u"==============================\n")

@slash.slash(name="shutdown", description="Closes the connection to Discord.", guild_ids=server_id)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('shutdown')
    await bot.close()
#===============else

#===============cog
for cog_files in os.listdir("./cogs") :
    if cog_files.endswith(".py") :
        bot.load_extension(f"cogs.{cog_files[:-3]}")

@bot.command(name="load",description="Load cog.")
@commands.is_owner()
async def load(ctx, extension):
    await ctx.message.add_reaction('✅')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"succed load `{extension}` cog")

@bot.command(name="unload",description="Unload cog.")
@commands.is_owner()
async def load(ctx, extension):
    await ctx.message.add_reaction('⚠️')
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"succed unload `{extension}` cog")

@bot.command(name="reload",description="Reload cog.")
@commands.is_owner()
async def reload(ctx, extension):
    await ctx.message.add_reaction('🔄')
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f"succed reload `{extension}` cog")

#===============on ready
@bot.event
async def on_ready() :
    ctc.printGreen(u'Logged in as:\n'.format(bot))
    ctc.printPink(u'{0.user.name}\n'.format(bot))
    ctc.printYellowRed(u'{0.user.id}\n'.format(bot))
    game = discord.Activity(type=discord.ActivityType.listening, name='YouTube')
    await bot.change_presence(status=discord.Status.idle, activity=game)
    id = bot.get_channel(listener_port)
    await id.send(u'💽:{0.user.name}`{0.user.id}`'.format(bot))
#===============BOT run
if __name__ == "__main__" :
    bot.run(key_loader.key)
