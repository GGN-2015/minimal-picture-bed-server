
import ggntalk # my own lib

print("[上传文件] 开始.")

fname = input("输入文件在本地的位置（含文件名）>>>")
ans = ggntalk.getfb(fname)
fname = input("输入上传到服务器后文件的名称>>>")
hostip = input("输入服务器 IP>>>")
port = int(input("输入服务器端口 >>>"))

all_len = len(ans)
print("[上传文件] 总长度 = " + str(all_len))

def nstr(i): # i 是一个整数
    if i < 10:
        return "  " + str(i)
    elif i < 100:
        return " " + str(i)
    return str(i)

flag = False # 出错标记

while len(ans) > 1000:
    msg = ggntalk.csnd(b"append|" + fname.encode("utf-8") + b"|" + ans[:1000], hostip, port,1024)
    ans = ans[1000:]
    print(" 已上传 " + nstr(int((all_len - len(ans))/all_len * 100)) + "% \t" + msg)
    if msg == "" or msg == "#error: can not connect to the server.":
        YN = input("  服务器没有回应或出错，是否终止上传文件？")
        if YN == "y" or YN == "Y":
            flag = True
            print("[上传文件]您终止了文件上传!")
            break

if len(ans) != 0 and not flag:
    msg = ggntalk.csnd(b"append|" + fname.encode("utf-8") + b"|" + ans, hostip, port, 1024)
    print("已上传 100% \t" + msg)

print("[上传文件] 文件上传结束.")
