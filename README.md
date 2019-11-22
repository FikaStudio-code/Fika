# Fika：ブロックチェーンネットワークシミュレータ
OS レベル仮想化機構実装の一つである FreeBSD Jails を利用し、任意のトポロジーを形成したブロックチェーンネットワークをプログラミングできる Python ライブラリ Fika を作成した。Bitcoinが始まってから約 10 年が経つが、ブロックチェーンに対して多くの論文でプロトコル設計や実装上の問題が報告されている。Fika はそのような問題を解決するための研究手段や、ブロックチェーンを取り巻く環境の学習 手段として有効に活用することができるだろう。このシミュレータに関する論文は**main.pdf**を参照してください。

Fika ライブラリは以下のように大きく 2 つのプログラムに分かれている。
- jail を用いてネットワークを構築するプログラム（fika/vitothon/）
- jail を仮想通貨ネットワーク内のノードとして機能させるプログラム（fika/sim/）

## 導入方法
ライブラリを使用できる環境整備についての手順を簡単に示す。  
1. VirtualBox をインストールする  
インストール方法は各自で確認されたい。
2. 使用する OS を Web サイトからダウンロードする  
Fika ライブラリは FreeBSD の OS パーティショニング機能である jail とネットワーク仮想化機能 VIMAGE を操作する必要があるため、VIMAGE がデフォルトで備わっている **FreeBSD 12.0-RELEASE** を使用することを勧める。それ以前のバージョンを用いる場合はカーネルの再構築の必要がある。
3. VirtualBox で新規マシン作成  
上記の OS を用いて仮想マシンを作成する。
4. 以下のコマンドを実行する

<!--
```python:FreeBSD
root@fika: portsnap fetch
root@fika: portsnap extract
root@fika: pkg install sysutils/ezjail
root@fika: vi /usr/loca/etc/ezjail.conf
# ezjail_jaildir = /usr/jails/ <- この行のコメントアウトを外し、ディレクトリを変更
ezjail_jaildir = /jails
root@fika: mkdir /jails
root@fika: ezjail-admin install
# server client 用の jail の雛形を作成
root@fika: cp -pR /jails/flavours/example /jails/flavours/server
root@fika: cp -pR /jails/flavours/example /jails/flavours/client

# PC から仮想マシン（FreeBSD）にファイル送信する
yourpc username$ scp -r server client fika fika_pkg "hostname@<host address>:~"

root@fika: cd /home/username
# 先ほど作成した雛形にプログラムと pkg ファイルをコピーする
root@fika: cp -r client /jails/flavours/client/usr/local
root@fika: cp -r server /jails/flavours/server/usr/local
root@fika: mv fika_pkg pkg
root@fika: cp -r pkg /jails/flavours/server
root@fika: cp -r pkg /jails/flavours/client
```  
-->
