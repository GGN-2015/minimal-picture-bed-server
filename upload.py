
import ggntalk # my own lib

print("[send-file] start.")

fname = input("input fname>>>")
ans = ggntalk.getfb(fname)
fname = input("input store name>>>")
hostip = input("input hostip>>>")
port = int(input("input port>>>"))

all_len = len(ans)

while len(ans) > 1000:
    msg = ggntalk.csnd(b"append|" + fname.encode("utf-8") + b"|" + ans[:1000], hostip, port,1024)
    ans = ans[1000:]
    print(str(int((all_len - len(ans))/all_len * 100)) + "% " + msg)

if len(ans) != 0:
    msg = ggntalk.csnd(b"append|" + fname.encode("utf-8") + b"|" + ans, hostip, port, 1024)
    print("100% " + msg)

print("[send-file] senf-file end.")
