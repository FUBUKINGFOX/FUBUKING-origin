import requests
from bs4 import BeautifulSoup
import random
import time
from discord.ext import commands
from bin.class_init.cog_init import cog_init
#=========> test cog methods
class methods():
    def req_covic():
        info = []
        url = "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"
        r = requests.get(url)
        r = BeautifulSoup(r.text, "html.parser")
        r = r.find_all("span", class_="country_confirmed_percent")
        for i in r :
            info.append(str(i).replace("<span class=\"country_confirmed_percent\"><small>","").replace("</small></span>",""))
        return info

class test(cog_init):

    @commands.command(name='choice', aliases=["ce"], description="")
    async def choice_(self, ctx, list: str) :
        list_ = list.replace(","," ").split()
        ans = random.choice(list_)
        list_ = " ".join(str(i) for i in list_)
        
        await ctx.send(f"> 你的選擇有:\n {list_}")
        time.sleep(1)

        await ctx.send(f"> 最後我幫你選擇了:\n{ans}")

    @commands.command(name='covic', description="")
    @commands.is_owner()
    async def covic_(self, ctx):
        i = methods.req_covic()
        await ctx.send("累計" + i[0])
        await ctx.send(i[1])



def setup(bot):
    bot.add_cog(test(bot))