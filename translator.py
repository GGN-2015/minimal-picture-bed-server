# GGN_2015 made this file to translate encode msg back to utf-8
import codecs
import time
import datetime
import os

def GetPrice(date, weight, size):
    fi = open("tmp", "w")
    fi.write(DateToString(date) + " " + str(weight) + " " + str(size))
    fi.close()

    os.system("python3 calculator.py")

    fo = open("tmp", "r")
    ans = int(fo.read())
    fo.close()

    return ans

def DateToString(date): # change datetime.date to string
    return date.strftime("%Y-%m-%d")

def GetDateDelta(date2, date1): # date1, date2 is a string like "2008-05-12"
    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")

    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    
    tmp = str(date2-date1)
    if tmp == "0:00:00":
        return 1
    else:
        return int(tmp.split("day")[0])+1

#def translate(s): # s is a string like "%E9%9D%92%E5%B7%9E%E5%88%86%E5%BA%97"
#    return codecs.decode(s.replace("%", ""), "hex").decode("utf-8")

from trans_ext import translate

def retranslate(s): # s is a string like "这是汉字"
    s = codecs.encode(s.encode("utf-8"), "hex").decode("utf-8")
    ans = ""
    for i in range(0, len(s)): # for all the char
        if i%2 == 0:
            ans += "%"
        ans += s[i]
    return ans
        

def timeNow():
    return time.strftime("%H:%M:%S", time.localtime())

def dateNow():
    return time.strftime("%Y-%m-%d", time.localtime())

if __name__ == "__main__":
    print("[debug] for translator...")
    print("dateNow() = " + dateNow())
    print("timeNow() = " + timeNow())
    
    s = input("输入一个纯汉字字符串>>>")
    print("retranslate(s) = " + retranslate(s))
    s = input("输入一个纯编码字符串>>>")
    print("translate(s) = " + translate(s))

    a = input("輸入一個日期：(如：2001-10-02)")
    b = input("輸入另一個日期：(如：2002-01-10)")

    print(GetDateDelta(b, a)) # b - a 前減后
