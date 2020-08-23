# -*- encoding: utf-8 -*-

# i swear to use a single file to contain the whole server! -- GGN_2015
# GGN_2015 is a true programmer

# 我是中国人，只说中国话，凭什么在注释里面写英文。
# 小声说：英语不好，怕被喷
# 请用 utf-8 解析此文件

version = "2020-08-23"
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

    if matchpre(inp, "append|"): # 无法用浏览器访问此功能
        inp = inp[len("append|"):]
        lis = inp.split(b"|", 1)
        fname = lis[0] # 文件名
        res = lis[1]   # 文件内容
        
        parts = fname.split(b".")
        if parts[-1] == b"py": # 我不可能让你上传一个程序
            return "[服务器] 上传文件后缀不合法。"

        fi = open(fname, "ab") # 写二进制文件
        fi.write(res)
        fi.close()

        return "[服务器] 追加成功 " + str(len(res)) + " 字节。"

    inp = inp.decode("utf-8")
    inp = inp.split("\n", 1)[0].replace("GET /", "").split(" HTTP")[0]
    #inp.replace("--", "..")  # 如果您希望客户从浏览器访问到服务器上的全部文件，请取消这行的注释。

    print("[服务器 工人] inp = " + inp)

    if matchpre(inp, "image/") or inp == "favicon.ico":
        print("[服务器 工人] 正在生成图片返回信息.")

        if inp != "favicon.ico":
            inp = inp[len("image/"):]
        
        # print("inp = " + inp)

        outp = "HTTP/1.1 200 OK\n"
        outp += "Accept-Ranges: bytes\n"
        outp += "Content-Type: image/png\n"
        outp += "Server: Apache-Coyote/1.1\n"
        outp += "Date: " + time.ctime() + " GMT\n"
        outp += "Content-Length: $SIZE$\n\n"

        ans = b""
        if inp == "favicon.ico":
            print("[服务器 工人] 正在绘制图标文件 ...")
            fi = open("qwq.png", "rb")
            outp.replace("png", "jpeg")
            ans = fi.read()
            outp.replace("$SIZE$", str(len(ans))) # 填写文件大小
            fi.close()

            outp = outp.encode("utf-8") + ans
            print("[服务器 工人] 图标文件绘制成功 ...")
            return outp

        try:
            print("[服务器 工人] 正在读取图片文件 ...")

            if not os.path.isfile(inp):
                # 文件不存在
                print("[服务器 工人] 图片不存在.")
                outp = "HTTP/1.1 200 OK\nContent-Type: text\n\n"
                outp += "<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>"
                outp += "<body style='max-width: 500px; margin: 0 auto'><h4>喵呜~ 您的图丢了!</h4>"
                outp += "<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\"></img></body>"
                return outp

            fi = open(inp, "rb")
            ans = fi.read()
            fi.close()
            print("[服务器 工人] 文件读取完成...")
            outp.replace("$SIZE$", str(len(ans)))
        except:
            print("[服务器 工人] 图片文件读取出错 ...")
            outp = "HTTP/1.1 200 OK\nContent-Type: text\n\n"
            ans = traceback.format_exc().encode("utf-8")
            print(traceback.format_exc())
        outp = outp.encode("utf-8") + ans
        return outp

        

    outp = """HTTP/1.1 200 OK\nContent-Type: html\nCharset: UTF-8\n\n"""
    outp += "<head><title>显示代码</title><meta charset=\"utf-8\"></head>"
    outp += "<body>\n"

    # ----- 在线下填写你的代码 -----


    #if inp == "stop/" or inp == "stop":
    #    outp += "<h3>[server] server stop successfully</h3>"
    #    global cflag
    #    cflag = False

    if matchpre(inp, "code/"): # 显示程序代码
        inp = inp[len("code/"):]
        outp += "<h2>"+inp+"</h2><hr>\n"
        outp += "<pre>"+getf(inp).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")+"</pre>"
        outp += "<img src=\"http://" + WAN_IP + ":" + str(PORT) +"/image/look.png\"></img>"
        return outp

    if matchpre(inp, "show/"): # 直接显示 HTML 文件
        inp = inp[len("show/"):]
        outp = getf(inp)
        return outp

    elif matchpre(inp, "run/"): # 执行一个 python 程序，将输出作为 HTML 返回
        print("[服务器 工人] 执行一个 python 程序")
        inp = inp[len("run/"):]
        
        res = ""
        if inp.find("/") != -1:
            fname, res = inp.split("/", 1)
            inp = fname
            print("fname = " + fname + " res = " + res)

        inp += ".py"

        if not os.path.isfile(inp): # 文件不存在
            print("[服务器 工人] python 程序不存在!")
            outp = "HTTP/1.1 200 OK\nContent-Type: text\n\n"
            outp += "<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>"
            outp += "<body style='max-width: 500px; margin: 0 auto'><h4>喵呜~ 您的程序丢了!</h4>"
            outp += "<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\"></img></body>"
            return outp
        
        fi = open("tmp-in" + str(cid), "w")
        fi.write(res)
        fi.close()

        print(" 执行 python 程序 inp = " + inp + " ...")
        os.system("python3 " + inp + " < tmp-in" + str(cid) + " > tmp-out" + str(cid))
        
        print(" 生成返回结果 ...")
        outp += getf("tmp-out" + str(cid))

        os.system("rm tmp-in" + str(cid))
        os.system("rm tmp-out" + str(cid))

        return outp

    else:
        #outp += "[ggnserver] instruction not found."
        print("[服务器] 客户端输入的指令不是指令。")
        outp += "<h2>[服务器] 你输入了:{" + inp + "} \n但是这并不是一个指令</h2>"
        outp += "<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\"></img>"

    outp += "</body>"

    # ----- add your code above this line -----

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
        print("[服务器 顾问] 等待客户端反馈信息, cid = " + str(cid))
        msg = cli.recv(1024 * 1024 * 33)

    except:
        print("[服务器 顾问] 等待客户端反馈信息时出错. cid = " + str(cid))
        print(traceback.format_exc())

    print("[服务器 顾问] 向客户端反馈信息 cid = " + str(cid))
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
