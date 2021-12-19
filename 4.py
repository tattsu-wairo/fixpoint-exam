# ログファイルの読み取り
with open("log.txt", 'r', encoding='utf-8') as f:
    l = f.read().splitlines()

list_t = []  # ログファイルの1行ずつ格納するためのリスト

N = int(input("何回連続でアイムアウトしたらだめですか : "))

# 時間、IP、pingで区切る
for i in l:
    list_t.append(i.split(','))

checked_ip = [] # 調べたipを格納
checked_subnet = [] # 調べたsubnetを格納

start_dict={}

log_dict={} # logの情報をipごとに管理
subnet_dict = {}  # サブネットとサーバーアドレスごとの状態を格納
subnet_dict_copy={}


# サブネットとサーバーアドレスごとの状態を格納する辞書型を作成する
# 故障していない状態をFalseとする
# subnetマスク→サーバーアドレスで故障状態を確認できる
def make_subnet_dict(ip):
    global subnet_dict,subnet_dict_copy
    ip_address2 = ""
    subnet = ""
    ip_split = []
    ip_split = ip.split('/')
    subnet_num = ip_split[1]
    ip_address_split = ip_split[0].split('.')
    for i in ip_address_split:
        ip_address = format(int(i), '08b')
        ip_address2 += ip_address
    count = 0
    while count < int(subnet_num):
        subnet += ip_address2[count]
        count += 1
    if(subnet in subnet_dict.keys()):
        if not(ip in subnet_dict[subnet].keys()):
            subnet_dict[subnet][ip] = False
    else:
        subnet_dict[subnet] = {}
        subnet_dict[subnet][ip] = False
    subnet_dict_copy=subnet_dict

# サーバーアドレスからサブネットマスクを取得する(2進数での表記)
def get_subnet(ip):
    ip_address2 = ""
    subnet = ""
    ip_split = []
    ip_split = ip.split('/')
    subnet_num = ip_split[1] # サブネット数
    ip_address_split = ip_split[0].split('.')
    for i in ip_address_split:
        ip_address = format(int(i), '08b') # 2進数表記で8桁に。足らない上位桁は0でうめる
        ip_address2 += ip_address
    count = 0
    while count < int(subnet_num):
        subnet += ip_address2[count]
        count += 1
    return subnet

# サブネット内のサーバーすべて故障中か確認
def check_all_error(subnet):
    global subnet_dict
    for i in subnet_dict[subnet]:
        if not(subnet_dict[subnet][i]):
            return False
    return True

# 過負荷状態かを確認するために呼ばれる
def check_subnet(ip):
    global subnet_dict
    subnet=get_subnet(ip)
    num={} # サブネット内の各サーバーごとにカウントを分ける
    if not(subnet in checked_subnet):
        print(f"\n＞＞サブネット : {subnet}＜＜")
        start_time=0
        no_error_flag = True
        for i in list_t:
            if not (i[1] in num.keys()):
                num[i[1]] = 1
            if(subnet == get_subnet(i[1])):
                if(i[2] == '-' and start_time == 0):
                    if(num[i[1]] >= N):
                        subnet_dict[subnet][i[1]] = True
                        # サブネット内すべてエラーなら
                        if (check_all_error(subnet)):
                            start_time = i[0]
                    else:
                        num[i[1]] += 1
                else:
                    num[i[1]] = 1
                    subnet_dict[subnet][i[1]] = False
                    if(i[2] != '-' and start_time != 0):
                        # サブネット内すべてエラーでないなら
                        if not (check_all_error(subnet)):
                            print(f"故障期間 : {start_time} - {i[0]}")
                            start_time = 0
                            no_error_flag = False
        if(start_time != 0):
            # サブネット内すべてエラーなら
            if (check_all_error(subnet)):
                print(f"故障期間 : {start_time} - 現在も故障の可能性あり")
        elif(no_error_flag):
            print("故障なし")
        checked_subnet.append(subnet)



def make_log_dict(log):
    time=log[0]
    ip=log[1]
    ping=log[2]
    if(ip in log_dict.keys()):
        if not(time in log_dict[ip].keys()):
            log_dict[ip][time] = ping
    else:
        log_dict[ip] = {}
        log_dict[ip][time] = ping

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
    make_subnet_dict(t[1])

print("----------------------")

for i in list_t:
    check_subnet(i[1])
