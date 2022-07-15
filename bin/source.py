from bin import ctc
import pathlib
import time
import os
import random
#============
sources_ = str(pathlib.Path(__file__).parent.absolute()) + "\\bin\\source\\"
#============
cv = []
with open("./bin/source/bot_cv.cov", mode="r", encoding="utf-8") as cv_ :
    end = False
    while end == False :
        f = cv_.readline().strip("\n")
        if f == ".end" :
            end = True
        else :
            cv.append(str(f))

cv = random.choice(cv)

ctc.printBlue("Source loaded...\n")
time.sleep(1)
os.system("cls")
