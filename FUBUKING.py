#== encoding utf-8 == discord 2.0 ==
from bin import config_loader, ctc, ctt, key_loader, source
from bin.class_init.cog_init import cog_init
from bin.public import var
import os
import sys
import getopt #input args
import psutil
import time
import pathlib
import numpy
import asyncio
import discord
from discord.ext import commands
#===============app start
argv = sys.argv[1:]
arg_token = None
try:
    opts, args = getopt.getopt(argv,"ht:",["token="])
except getopt.GetoptError:
    print ('main.py -t <token>')
    sys.exit(2)
for opt, arg in opts:
      if opt == '-h':
         print ('main.py -t <token>')
         sys.exit()
      elif opt in ("-t", "--token"):
         arg_token = arg
#===============bot setting
prefix = numpy.array(["/","F ","f "])
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, description='FUBUKING music bot.', help_command=None ,intents=intents)
path = str(pathlib.Path(__file__).parent.absolute())
var.var_creat("path", path)
server_id = config_loader.load_server_id()
listener_port = (960010657506394132)
#===============
server_start_time = time.time()
#===============cmd
@bot.command(name="ping",description="Show ping.", guild_ids=server_id)
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
    server_test_time = time.time()
    #==========
    embed = (discord.Embed(title=u'🍵{0.user.name}'.format(bot),
                               description=f'```ini\n[system/INFO]                                            \n```',
                               color=e_color)
                 .add_field(name='💠CPU usage', value=f"{CPU_use}%")
                 .add_field(name='🧱RAM usage', value=f"{RAM_use}%")
                 .add_field(name='📡ping', value=f"{ping}-ms")
                 .set_author(icon_url="https://cdn.discordapp.com/emojis/1028895182290161746.webp", name=f"CORN Studio")
                 .set_footer(text=f"伺服器自啟動已經運行{round(server_test_time - server_start_time, 4)}-s"))
    if e_color != 0x59ff00 :
        embed.add_field(name='WARN', value=f"```css\n{warn}```")

    await ctx.send(embed=embed)
    
    ctc.printGreen(u"==============================\n")
    ctc.printYellow("=====>Bot_system\n")
    #time_now(False)
    ctc.printYellow(f'ping:[{ping}]-ms=>[{bot.latency*1000}]-us\n')
    ctc.printGreen(u"==============================\n")

@bot.command(name="shutdown", description="Closes the connection to Discord.", guild_ids=server_id)
@commands.is_owner()
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.invisible)
    await ctx.send("> " + source.off_cv() + "<:ANG:1028735212621938719>")
    await bot.close()
#===============else
class commands_error_handler(cog_init) :
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title="<:SAD:1028588126291120219>Command ERROR :", description=f"{error}", color=0xf6ff00)
        await ctx.message.delete()
        await ctx.send(embed=embed)
async def load_error_handler():
    await bot.add_cog(commands_error_handler(bot))
#===============cog
async def load_extensions() :
    for cog_files in os.listdir("./cogs") :
        if cog_files.endswith(".py") :
            await bot.load_extension(f"cogs.{cog_files[:-3]}")
        elif cog_files.endswith(".pyc") :
            await bot.load_extension(f"cogs.{cog_files[:-4]}")

@bot.command(name="load",description="Load cog.")
@commands.is_owner()
async def load(ctx, extension):
    await ctx.message.add_reaction('✅')
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"succeed load `{extension}` cog")

@bot.command(name="unload",description="Unload cog.")
@commands.is_owner()
async def unload(ctx, extension):
    if extension == "commands_error_handler" :
        await ctx.send("Can't unload this cog.")
    else:
        await ctx.message.add_reaction('⚠️')
        await bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"succeed unload `{extension}` cog")

@bot.command(name="reload",description="Reload cog.")
@commands.is_owner()
async def reload(ctx, extension):
    await ctx.message.add_reaction('🔄')
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f"succeed reload `{extension}` cog")


@bot.command(name="kick", description="kick member from voice_channel", guild_ids=server_id)
@commands.is_owner()
async def kick(ctx, member: discord.Member):
    await member.move_to(channel=None)

#===============on ready
@bot.event
async def on_ready() :
    os.system("cls")
    ctc.printSkyBlue("Discord Bot Server [版本 3.3.1.0]\n")
    ctc.printDarkSkyBlue("(c) CORN Studio. 著作權所有，並保留一切權利。\n")
    ctc.printGreen(u'Logged in as:\n'.format(bot))
    ctc.printPink(u'{0.user.name}\n'.format(bot))
    ctc.printYellowRed(u'{0.user.id}\n'.format(bot))
    game = discord.Activity(type=discord.ActivityType.listening, name='YouTube')
    await bot.change_presence(status=discord.Status.idle, activity=game)
    id = bot.get_channel(listener_port)
    await id.send(u'💽:{0.user.name}`{0.user.id}`'.format(bot))
#===============BOT run
async def main(token):
    async with bot:
        await load_extensions()
        await load_error_handler()
        await bot.start(token)

if __name__ == "__main__" :
    asyncio.run(main(key_loader.load_key(arg_token)))
