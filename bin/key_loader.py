from bin import ctc
import time

def load_key() :
    with open("./cfg/bot.key", mode="r", encoding="utf-8") as e :
        key = e.readline().strip("\n")
        # ctc.printGreen("bot.key loaded...\n")
    return key
time.sleep(0.5)
