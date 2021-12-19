# 株式会社フィックスポイント プログラミング試験

【試験期間】2021/12/17(金) 22:00 ~ 2021/12/20(月) 22:00

## 実行環境

【使用言語】Python 3.8.3

【使用モジュール】標準ライブラリのみ

## 各問題ごとの説明

すべての設問において、logファイルは各実行ファイルと同じディレクトリ内にあることを想定している。

出力として期間に終わりが見つからない場合は故障などの可能性があるといった表現をしている。故障がない場合は故障なしとしている。

また、実行時に使用したlogファイルはlog.txtである。

```txt:log.txt
20201019133124,10.20.30.1/16,1
20201019133125,10.20.30.2/16,-
20201019133134,192.168.1.1/24,10
20201019133135,192.168.1.2/24,-
20201019133224,10.20.30.1/16,-
20201019133225,10.20.30.2/16,-
20201019133230,10.20.30.2/16,5
20201019133234,192.168.1.1/24,8
20201019133235,192.168.1.2/24,15
20201019133324,10.20.30.1/16,-
20201019133325,10.20.30.2/16,2
20201019133330,10.20.30.1/16,1
20201019133340,10.20.30.1/16,4
20201019133344,10.20.30.1/16,10
20201019133350,10.20.30.1/16,-
20201019133351,192.168.1.2/24,-
20201019133352,192.168.1.2/24,-
20201019133353,192.168.1.2/24,6
```

### 設問1

1.pyを実行することで確認ができる。

logファイルにでてくるサーバーアドレスを1つずつ見ていく。

logファイル内の各サーバーアドレスだけを見た時に応答結果が'-'であるときの確認日時を故障期間の始まりとし、次に応答結果が'-'以外のものになったときの確認日時を故障期間の終わりとしている。

出力は各サーバーアドレス毎に行っている。

### 1.pyの実行結果

```txt
＞＞サーバーアドレス : 10.20.30.1/16＜＜
故障期間 : 20201019133224 - 20201019133330
故障期間 : 20201019133350 - 現在も故障の可能性あり

＞＞サーバーアドレス : 10.20.30.2/16＜＜
故障期間 : 20201019133125 - 20201019133230

＞＞サーバーアドレス : 192.168.1.1/24＜＜
故障なし

＞＞サーバーアドレス : 192.168.1.2/24＜＜
故障期間 : 20201019133135 - 20201019133235
故障期間 : 20201019133351 - 20201019133353
```

### 設問2

2.pyを実行し、何回以上連続してタイムアウトした場合にするかをコンソールで入力することで確認ができる。

1.pyの関数check(ip)の中身を編集している。

連続して応答結果が'-'であるときにカウントを増やしていき、指定のN回以上になったときの確認日時を故障期間の始まりとし、次に応答結果が'-'以外のものになったときの確認日時を故障期間の終わりとしている。

出力は各サーバーアドレス毎に行っている。

### 2.pyの実行結果(N=2)

```txt
＞＞サーバーアドレス : 10.20.30.1/16＜＜
故障期間 : 20201019133324 - 20201019133330

＞＞サーバーアドレス : 10.20.30.2/16＜＜
故障期間 : 20201019133225 - 20201019133230

＞＞サーバーアドレス : 192.168.1.1/24＜＜
故障なし

＞＞サーバーアドレス : 192.168.1.2/24＜＜
故障期間 : 20201019133352 - 20201019133353
```

### 設問3

3.pyを実行し、

1. 何回以上連続してタイムアウトした場合にするか

2. 直近何回の平均応答時間を見るのか

3. 何ミリ秒を超えた場合にするか

をコンソールで入力することにより確認できる。

直近m回の応答結果は関数get_recent_ping(logの1行)で取得ができる。

読み取ったサーバーアドレスの応答時間を関数set_recent_ping(logの1行)で直近m回の応答結果を更新することができる。

関数average_recent_ping(直近m回の応答結果)で直近m回の応答結果の平均時間を取得できる。

average_recent_ping(直近m回の応答結果)で取得した値が指定したtミリ秒よりも多くなったときの確認日時を過負荷状態期間の始まりとし、次に応答結果が'-'以外のものになったときの確認日時を過負荷状態期間の終わりとしている。

出力は各サーバーアドレス毎に行っている。

### 3.pyの実行結果(N=2, m=2, t=100)

```txt
＞＞サーバーアドレス : 10.20.30.1/16＜＜
---- 過負荷エラー ----
過負荷状態期間 : 20201019133224 - 20201019133340
---------------------

---- 過負荷エラー ----
過負荷状態期間 : 20201019133350 - 現在も過負荷状態の可能性あり
---------------------

故障期間 : 20201019133324 - 20201019133330

＞＞サーバーアドレス : 10.20.30.2/16＜＜
---- 過負荷エラー ----
過負荷状態期間 : 20201019133125 - 20201019133325
---------------------

故障期間 : 20201019133225 - 20201019133230

＞＞サーバーアドレス : 192.168.1.1/24＜＜
---------------------
過負荷状態なし
---------------------

故障なし

＞＞サーバーアドレス : 192.168.1.2/24＜＜
---- 過負荷エラー ----
過負荷状態期間 : 20201019133135 - 現在も過負荷状態の可能性あり
---------------------

故障期間 : 20201019133352 - 20201019133353
```

### 設問4

4.pyを実行し、何回以上連続してタイムアウトした場合にするかをコンソールで入力することで確認ができる。

関数make_subnet_dict(サーバーアドレス)はサブネットとサーバーアドレスごとの状態を格納する辞書型を作成する。作成した辞書型は「subnetマスク」→「サーバーアドレス」でアクセスすることで故障状態を確認できる。故障していない状態をFalseとする。

関数get_subnet(サーバーアドレス)はサーバーアドレスから2進数のサブネットマスクを取得する

関数check_all_error(サブネットマスク)はサブネット内のサーバーすべて故障中か取得する。故障中ならばTrueが返る。

関数check_subnet(サーバーアドレス)は関数check(サーバーアドレス)を編集したものであり、各サブネット内のサーバーがN回以上タイムアウトになったときに故障状態とし、サブネット内すべてのサーバーが故障状態になったときの確認日時を過負荷状態期間の始まりとし、次にサブネット内のサーバーが少なくとも1つでも正常になったときの確認日時を過負荷状態期間の終わりとしている。

### 4.pyの実行結果(N=1)

```txt
＞＞サーバーアドレス : 10.20.30.1/16＜＜
故障期間 : 20201019133224 - 20201019133330        
故障期間 : 20201019133350 - 現在も故障の可能性あり

＞＞サーバーアドレス : 10.20.30.2/16＜＜
故障期間 : 20201019133125 - 20201019133230        

＞＞サーバーアドレス : 192.168.1.1/24＜＜
故障なし

＞＞サーバーアドレス : 192.168.1.2/24＜＜
故障期間 : 20201019133135 - 20201019133235        
故障期間 : 20201019133351 - 20201019133353        
----------------------

＞＞サブネット : 0000101000010100＜＜
故障期間 : 20201019133224 - 20201019133230

＞＞サブネット : 110000001010100000000001＜＜
故障なし
```

### 4.pyの実行結果(N=2)

```txt
＞＞サーバーアドレス : 10.20.30.1/16＜＜  
故障期間 : 20201019133324 - 20201019133330

＞＞サーバーアドレス : 10.20.30.2/16＜＜  
故障期間 : 20201019133225 - 20201019133230

＞＞サーバーアドレス : 192.168.1.1/24＜＜ 
故障なし

＞＞サーバーアドレス : 192.168.1.2/24＜＜ 
故障期間 : 20201019133352 - 20201019133353
----------------------

＞＞サブネット : 0000101000010100＜＜     
故障なし

＞＞サブネット : 110000001010100000000001＜＜
故障なし
```