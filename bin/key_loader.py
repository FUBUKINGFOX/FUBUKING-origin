from bin import ctc
import time

def load_key() :
    with open("./cfg/bot.key", mode="r", encoding="utf-8") as e :
        key = e.readline().strip("\n")
    return key

ctc.printGreen("bot.key loaded...\n")
time.sleep(0.5)
