# ログファイルの読み取り
with open("log.txt", 'r', encoding='utf-8') as f:
    l = f.read().splitlines()

list_t = []  # ログファイルの1行ずつ格納するためのリスト

N=int(input("何回連続でアイムアウトしたらだめですか : "))

m=int(input("直近何回の平均応答時間をみますか : "))
t=int(input("何ミリ秒超えた場合ですか : "))

ping_dict = {}  # サーバーアドレスごとに直近m回のping値を保存
start_dict = {}  # 各ipごとにサーバー過負荷状態の開始時間を格納

# 時間、IP、pingで区切る
for i in l:
    list_t.append(i.split(','))

checked_ip = []  # 調べたサーバーアドレスを格納

def set_recent_ping(ip_list):
    global m, t, ping_dict
    # 直近m回のping値を取得
    # すでに見たことのあるサーバーアドレスの場合
    if(ip_list[1] in ping_dict.keys()):
        recent_ping = ping_dict[ip_list[1]]
        recent_ping.append(ip_list[2])
        recent_ping.pop(0)
    # まだ見たことないサーバーアドレスの場合
    else:
        recent_ping = [0]*m
        recent_ping.append(ip_list[2])
        recent_ping.pop(0)
        ping_dict[ip_list[1]] = recent_ping


def get_recent_ping(ip_list):
    if(ip_list[1] in ping_dict.keys()):
        return ping_dict[ip_list[1]]
    else:
        return [0]*m


def average_recent_ping(recent_ping_list):
    count = 0
    sum = 0
    for i in recent_ping_list:
        if(i != 0):
            count += 1
            if(i == '-'):
                sum += float(t*m)
            else:
                sum += float(i)
    # 直近の平均がない場合は平均時間0秒を返す
    if(count == 0):
        average = 0
    # 直近m回のping値の平均を返す
    else:
        average = float(sum)/float(count)
    return average

# サーバーに負荷がかかってないか確認するための関数
# log = [time, ip, ping]
def check_time(ip):
    global start_dict,checked_ip
    if not(ip in checked_ip):
        print(f"\n＞＞サーバーアドレス : {ip}＜＜")
        start_time=0
        no_error_flag = True
        for i in list_t:
            if(ip == i[1]):
                time=i[0]
                set_recent_ping(i)
                recent_ping_list = get_recent_ping(i)
                recent_average = average_recent_ping(recent_ping_list)
                if(recent_average > t):
                    if(start_time == 0):
                        start_time = int(time)
                else:
                    if(start_time != 0):
                        print("---- 過負荷エラー ----")
                        print(f"過負荷状態期間 : {start_time} - {time}")
                        print("---------------------")
                        print()
                        start_time = 0
                        no_error_flag=False
        if(start_time != 0):
            print("---- 過負荷エラー ----")
            print(f"過負荷状態期間 : {start_time} - 現在も過負荷状態の可能性あり")
            print("---------------------")
            print()
        elif(no_error_flag):
            print("---------------------")
            print("過負荷状態なし")
            print("---------------------")
            print()


# サーバーアドレス毎にタイムアウトになったログデータを見つけたときに呼び出す関数
def check(ip):
    global checked_ip
    num=1
    if not(ip in checked_ip):
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



#list_t=[time, ip, ping]*n
for l in list_t:
    check_time(l[1])
    check(l[1])