# -*- encoding: utf-8 -*-

# i swear to use a single file to contain the whole server! -- GGN_2015
# GGN_2015 is a true programmer

# 我是中国人，只说中国话，凭什么在注释里面写英文。
# 小声说：英语不好，怕被喷
# 请用 utf-8 解析此文件

# 共和新纪元！
# 万物皆插件！

version = "2020-08-26"
author  = "GGN_2015"

import socket
import os
import time
import traceback
import threading

cflag = True # 先前用这个变量控制循环是否终止

from config import PORT    # 从 config.py 中读取变量
from config import HOST_IP 
from config import WAN_IP
import ggntalk

def href(appendix = ""):
    return "http://" + WAN_IP + ":" + str(PORT) + "/" + appendix

def matchpre(s, p): # 匹配字符串前缀
    if type(s) == str:
        s += "#"
    else:
        s += b"#"
        p = p.encode("utf-8")

    for i in range(0, len(p)):
        if s[i] != p[i]:
            return False

    return True

def worker(inp, cid): # 操作员函数，将HTML代码作为返回值

    inp = inp.decode("utf-8")
    inp = inp.split("\n", 1)[0].replace("GET /", "").split(" HTTP")[0]

    # 执行一个 python 程序，将输出作为 HTML 返回
    print("    [服务器 工人] 执行一个 python 插件程序")
    if inp == "":
        inp = "welcome" # 直接定向到欢迎文件里
    
    res = ""
    if inp.find("/") != -1:
        fname, res = inp.split("/", 1)
        inp = fname
        print("fname = " + fname + " res = " + res)

    inp += ".py"

    if not os.path.isfile(inp): # 文件不存在
        print("    [服务器 工人] python 插件程序不存在!")
        outp = "HTTP/1.1 200 OK\nContent-Type: text\n\n"
        outp += "<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>"
        outp += "<body style='max-width: 500px; margin: 0 auto'><h4>喵呜~ 您的插件程序丢了!</h4>"
        outp += "<img src=\"" + href("image/cry.jpg") +"\"></img></body>"
        return outp
    
    fi = open("tmp-in" + str(cid), "w")
    fi.write(res)
    fi.close()

    print("     执行 python 程序 inp = " + inp + " ...")
    os.system("python3 " + inp + " " + str(cid) + " < tmp-in" + str(cid))
    
    print("     生成返回结果 ...")
    outp = ggntalk.getfb("tmp-out" + str(cid))

    os.system("rm tmp-in" + str(cid))
    os.system("rm tmp-out" + str(cid))

    return outp

conid = 0

def enco(s):
    if type(s) == str:
        return s.encode("utf-8")
    return s

def csend(cli, msg):
    while len(msg) > 500:
        cli.send(msg[:500])
        msg = msg[500:]
    cli.send(msg) # 分条发送消息

def consultant(cli): # use this in threads to answer for clients
    global conid
    conid += 1
    cid = conid # get an id by count

    try:
        print("    [服务器 顾问] 等待客户端反馈信息, cid = " + str(cid))
        msg = cli.recv(1024 * 1024 * 33)

    except:
        print("    [服务器 顾问] 等待客户端反馈信息时出错. cid = " + str(cid))
        print(traceback.format_exc())

    print("    [服务器 顾问] 向客户端反馈信息 cid = " + str(cid))
    csend(cli, enco(worker(msg, cid)))
    cli.close()


def getf(filename): # 读入文件中的所有内容
    fi = open(filename, "r")
    ans = fi.read()
    fi.close()
    return ans

def getip(): # 得到本机在局域网中的 IP
    tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp.connect(("8.8.8.8", 80))
    ip = tcp.getsockname()[0]
    tcp.close()
    return ip

def sloop(): # 服务器的主循环
    global PORT
    global HOST_IP
    global WAN_IP
    print("[服务器] 启动.")
    print(" 版本 : " + version + " 作者 : " + author)
    print(" 端口: " + str(PORT))
    print(" 广域网 IP：" + str(WAN_IP))

    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if HOST_IP == "auto":
            HOST_IP = getip()
            print(" 局域网 IP：" + HOST_IP)

        tcp.bind((HOST_IP, PORT))
        tcp.listen(5)

    except:
        print("[服务器] 无法启动服务器，原因可能是端口已经被占用。")
        print(traceback.format_exc())
        tcp.close()
        return

    else:
        global cflag
        clfag = True # True means continue to loop

        while cflag: # cflag can be set by worker
            try:
                print("[服务器] 等待客户端连接 ...")
                cli, addr = tcp.accept()

                th = threading.Thread(target = consultant, args = (cli, ))
                th.setDaemon(True)
                th.start()

            except:
                print("[服务器] 在访问服务器顾问时出错，错误信息如下：")
                print(traceback.format_exc())

        print("[服务器] 服务器成功终止。")
        tcp.close()

if __name__ == "__main__":
    print("[服务器] 正在准备启动 ...")
    sloop()
