from bin import ctc
import pathlib
import time
import os
import random
#============
sources_ = str(pathlib.Path(__file__).parent.absolute()) + "\\source\\"
#============
def on_cv() :
    on_cv = []
    with open(sources_ + "on_cv.cov", mode="r", encoding="utf-8") as cv_ :
        end = False
        while end == False :
            f = cv_.readline().strip("\n")
            if f == ".end" :
                end = True
            else :
                on_cv.append(str(f))
    
    return random.choice(on_cv)

#============
def off_cv() :
    off_cv = []
    with open(sources_ + "off_cv.cov", mode="r", encoding="utf-8") as cv_ :
        end = False
        while end == False :
            f = cv_.readline().strip("\n")
            if f == ".end" :
                end = True
            else :
                off_cv.append(str(f))

    return random.choice(off_cv)

#============
seeya = sources_ + "seeya.wav"
welcome = sources_ + "welcome.wav"
#============

#============ouput
# adminpic = sources_ + "admin.jpg"
#======methods


