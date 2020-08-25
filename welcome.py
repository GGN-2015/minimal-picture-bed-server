import time
import traceback

import translator
from server import getip

from config import WAN_IP
from config import PORT

def getf(filename): # 读取文本文件的全部内容
    fi = open(filename, "r")
    ans = fi.read()
    fi.close()
    return ans

try:

    inp = ""
    try:
        inp = input() # 获取输入信息
    except:
        pass # 不能获取说明没有输入信息

    print("<head>")
    print("<title>欢迎页</title>")
    print(getf("css.html"))
    print("<meta charset=\"utf-8\">")
    print("</head>")

    print("<body style=\"max-width: 700px; margin: 0 auto\">")
    #print("<h1>" + time.ctime() + " </h1>")

    #if inp != "":
    #    print("<h4> 您的输入是{" + inp + "} </h4>")
    #    if inp[0] == "%":
    #        print("<h4> 解码后您的输入是{" + translator.translate(inp) + "}</h4>")

    print("<h1>欢迎使用 GGN_2015 的迷你图床程序</h1>")
    print("<table>")
    print("    <tr><th>公网 IP</th><th>局域网 IP</th><th>端口</th></tr>")
    print("    <tr><td>" + WAN_IP + "</td><td>" + getip() + "</td><td>" + str(PORT) + "</td></tr>")
    print("</table>")

    print("</body>")

    print("<p>来自 github 的开源 repository：<a onclick=\"window.location.href='https://github.com/GGN-2015/minimal-picture-bed-server/tree/Version1002'\">minimal-picture-bed-server/Version1002</a></p>")

    print("<p>GGN_2015 的 github 账户：<button onclick=\"window.location.href='https://github.com/GGN-2015'\">GGN_2015</button></p>")


except:
    print("<hr>")
    print("<h1>执行程序时出错!</h1>")
    print("<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\" style=\"width:20%\"></img><br><br>")
    print("<pre>" + traceback.format_exc().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) # 输出错误信息
    print("</pre></body>")
