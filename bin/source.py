from bin import ctc
import pathlib
import time
import os
import random
#============
sources_ = str(pathlib.Path(__file__).parent.absolute()) + "\\source\\"
#============
on_cv = []
with open(sources_ + "bot_cv.cov", mode="r", encoding="utf-8") as cv_ :
    end = False
    while end == False :
        f = cv_.readline().strip("\n")
        if f == ".end" :
            end = True
        else :
            on_cv.append(str(f))

#============
off_cv = []
with open(sources_ + "shutdown.cov", mode="r", encoding="utf-8") as cv_ :
    end = False
    while end == False :
        f = cv_.readline().strip("\n")
        if f == ".end" :
            end = True
        else :
            off_cv.append(str(f))

#============ouput
on_cv = random.choice(on_cv)
off_cv = random.choice(off_cv)
adminpic = sources_ + "admin.jpg"

