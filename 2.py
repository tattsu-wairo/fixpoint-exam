# ログファイルの読み取り
with open("log.txt", 'r', encoding='utf-8') as f:
    l = f.read().splitlines()

list_t = [] # ログファイルの1行ずつ格納するためのリスト

N=int(input("何回連続でアイムアウトしたらだめですか : "))

# 時間、ip、pingで区切る
for i in l:
    list_t.append(i.split(','))

checked_ip = []  # 調べたipを格納

# サーバーアドレス毎にタイムアウトになったログデータを見つけたときに呼び出す関数
def check(ip):
    global checked_ip
    num=1
    if not(ip in checked_ip):
        print(f"\n＞＞サーバーアドレス : {ip}＜＜")
        start_time = 0
        no_error_flag = True
        for i in list_t:
            if(ip == i[1]):
                if (i[2] == '-' and start_time == 0):
                    if(num>=N):
                        start_time = i[0]
                    else:
                        num+=1
                else:
                    num=1
                    if(i[2] != '-' and start_time != 0):
                        print(f"故障期間 : {start_time} - {i[0]}")
                        start_time = 0
                        no_error_flag = False
        if(start_time != 0):
            print(f"故障期間 : {start_time} - 現在も故障の可能性あり")
        elif(no_error_flag):
            print("故障なし")
        checked_ip.append(ip)


for t in list_t:
    check(t[1])