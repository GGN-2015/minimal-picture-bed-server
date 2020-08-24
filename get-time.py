import time
import traceback
import translator

from config import WAN_IP
from config import PORT

try:

    inp = ""
    try:
        inp = input() # 获取输入信息
    except:
        pass # 不能获取说明没有输入信息

    print("<head>")
    print("<title>获取系统时间</title>")
    print("<meta charset=\"utf-8\">")
    print("</head>")

    print("<body style=\"max-width: 700px; margin: 0 auto\">")
    print("<h1> 当前的时间是 " + time.ctime() + " </h1>")

    if inp != "":
        print("<h4> 您的输入是{" + inp + "} </h4>")
        if inp[0] == "%":
            print("<h4> 解码后您的输入是{" + translator.translate(inp) + "}</h4>")

    print("</body>")

except:
    print("<hr>")
    print("<h1>执行程序时出错!</h1>")
    print("<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\" style=\"width:20%\"></img><br><br>")
    print("<pre>" + traceback.format_exc().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) # 输出错误信息
    print("</pre></body>")
