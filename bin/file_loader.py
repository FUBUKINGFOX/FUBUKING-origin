import json
import time
import os
#===============
file_ = "config.json"
with open(file_, mode="r", encoding="utf-8") as e :
    setting = json.load(e)

print(f"succeed import {file_}")
time.sleep(1)
os.system("cls")
#===============
server_id = []
with open(file = "server.config", mode = "r", encoding = "utf-8") as id_ :
    end = False
    while end == False :
        id = id_.readline().strip("\n")
        if id == ".end" :
            end = True
        else :
            server_id.append(int(id))

print("server_id:")
for w in server_id :
    print(w)

time.sleep(1)
os.system("cls")
#===============
