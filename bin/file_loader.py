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
    file_ = "server.cfg"
    server_id = []
    with open(file = f"./cfg/{file_}", mode = "r", encoding = "utf-8") as id_ :
        end = False
        while end == False :
            id = id_.readline().strip("\n")
            if id == ".end" :
                end = True
            else :
                server_id.append(int(id))

    ctc.printBlue(f"{file_} loaded...\n")
    print("server_id:")
    for w in server_id :
        ctc.printDarkGreen(str(w)+"\n")
    time.sleep(0.5)
    return server_id

#===============
def load_playchannel() :
    file_ = "play_channel.cfg"
    playchannel = []
    with open(file = f"./cfg/{file_}", mode = "r", encoding = "utf-8") as id_ :
        end = False
        while end == False :
            id = id_.readline().strip("\n")
            if id == ".end" :
                end = True
            else :
                playchannel.append(int(id))

    ctc.printBlue(f"{file_} loaded...\n")
    print("channel_id:")
    for w in playchannel :
        ctc.printDarkGreen(str(w)+"\n")
    time.sleep(0.5)
    return playchannel

    #===============
def load_songs_filter(enable_songs_filter :bool) :
    file_ = "songs_filter.cfg"
    songs_filter = []
    if enable_songs_filter == True :
        with open(file = f"./cfg/{file_}", mode = "r", encoding = "utf-8") as n_ :
            end = False
            while end == False :
                n = n_.readline().strip("\n")
                if n == ".end" :
                    end = True
                else :
                    songs_filter.append(n)
        ctc.printBlue(f"{file_} loaded...\n")
        time.sleep(0.5)
    return songs_filter
