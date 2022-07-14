import json
import time
from bin import ctc
#===============
file_ = "config.json"
with open(file_, mode="r", encoding="utf-8") as e :
    setting = json.load(e)

ctc.printBlue(f"{file_} loaded...")
time.sleep(0.5)
#===============
server_id = []
with open(file = "./cfg/server.cfg", mode = "r", encoding = "utf-8") as id_ :
    end = False
    while end == False :
        id = id_.readline().strip("\n")
        if id == ".end" :
            end = True
        else :
            server_id.append(int(id))

ctc.printBlue(f"server.cfg loaded...")
print("server_id:")
for w in server_id :
    ctc.printDarkGreen(w)

time.sleep(0.5)
#===============
