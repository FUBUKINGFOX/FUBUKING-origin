import json
import os
import time
from bin import ctc
#===============
def load_config_json() :
    file_ = "config.json"
    with open(file_, mode="r", encoding="utf-8") as e :
        setting = json.load(e)

    ctc.printBlue(f"{file_} loaded...\n")
    time.sleep(0.5)
    return setting

#===============
def load_server_id() :
    server_id = []
    with open(file = "./cfg/server.cfg", mode = "r", encoding = "utf-8") as id_ :
        end = False
        while end == False :
            id = id_.readline().strip("\n")
            if id == ".end" :
                end = True
            else :
                server_id.append(int(id))

    ctc.printBlue(f"server.cfg loaded...\n")
    print("server_id:")
    for w in server_id :
        ctc.printDarkGreen(str(w)+"\n")
    time.sleep(0.5)
    return server_id


#===============
def load_playchannel() :
    playchannel = []
    with open(file = "./cfg/play_channel.cfg", mode = "r", encoding = "utf-8") as id_ :
        end = False
        while end == False :
            id = id_.readline().strip("\n")
            if id == ".end" :
                end = True
            else :
                playchannel.append(int(id))

    ctc.printBlue(f"play_channel.cfg loaded...\n")
    print("channel_id:")
    for w in playchannel :
        ctc.printDarkGreen(str(w)+"\n")
    time.sleep(0.5)
    return playchannel

