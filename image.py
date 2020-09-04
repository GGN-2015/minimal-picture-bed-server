#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
import time
import traceback

import translator
from server import getip

from config import WAN_IP
from config import PORT
import ggntalk

def eprint(s):
    sys.stderr.write(s+"\n")

cid = ""

def sprint(s):
    global cid
    if type(s) == str:
        s = s.encode("utf-8")
    fi = open("tmp-out" + cid, "ab")
    fi.write(s+b"\n")
    fi.close

def getf(filename): # 读取文本文件的全部内容
    fi = open(filename, "r")
    ans = fi.read()
    fi.close()
    return ans

try:
    #global cid
    cid = sys.argv[1]

    inp = ""
    try:
        inp=input()
    except:
        pass

    eprint("    [服务器 工人] 正在生成图片返回信息.")

    #if inp != "favicon.ico":
    #    inp = inp[len("image/"):]
    
    # print("inp = " + inp)

    outp = "HTTP/1.1 200 OK\n"
    outp += "Accept-Ranges: bytes\n"
    outp += "Content-Type: image/png\n"
    outp += "Server: Apache-Coyote/1.1\n"
    outp += "Date: " + time.ctime() + " GMT\n"
    outp += "Content-Length: $SIZE$\n\n"

    ans = b""
    if inp == "favicon.ico":
        #print("    [服务器 工人] 正在绘制图标文件 ...")
        fi = open("favicon.png", "rb")
        #outp.replace("png", "jpeg")
        ans = fi.read()
        outp.replace("$SIZE$", str(len(ans))) # 填写文件大小
        fi.close()

        outp = outp.encode("utf-8") + ans
        eprint("    [服务器 工人] 图标文件绘制成功 ...")
        print(outp)
        os._exit(0)

    eprint("    [服务器 工人] 正在读取图片文件 ...")

    if not os.path.isfile(inp):
        # 文件不存在
        eprint("[服务器 工人] 图片不存在.")
        outp = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        outp += "<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>"
        outp += "<body style='max-width: 500px; margin: 0 auto'><h4>喵呜~ 您的图丢了!</h4>"
        outp += "<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\"></img></body>"
        sprint(outp)
        os._exit(0)

    ans = ggntalk.getfb(inp)
    eprint("    [服务器 工人] 文件读取完成...")
    outp.replace("$SIZE$", str(len(ans)))
    sprint(outp.encode("utf-8") + ans)
    os._exit(0)

except:
    sprint("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    sprint("<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>")
    sprint("<body style='max-width: 500px; margin: 0 auto'>")
    sprint("<h1>执行程序时出错!</h1>")
    sprint("    <img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\" style=\"width:20%\"></img><br><br>")
    sprint("    <pre>" + traceback.format_exc().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) # 输出错误信息
    sprint("    </pre>\n</body>")
