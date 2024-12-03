# Remote　Procedure　Call

## 概要
このプログラムはソケット通信を通じて、クライアントとサーバが異なるプログラミング言語で書かれていても、クライアントプログラムがサーバ上の機能を呼び出せるようなシステムです。クライアントがPythonで書かれたサーバに対してNode.jsに対して命令を出しています。

## 操作

- **floor**: 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
- **nroot**: 方程式 rn = x における、r の値を計算する。
- **reverse**: 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
- **validAnagram**:  2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
- **sort**: 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。

サーバーへのリクエスト
```
{
   "method": "subtract", 
   "params": [42, 23], 
   "param_types": [int, int],
   "id": 1
}
```

サーバーからのリスポンス
```
{
   "results": "19",
   "result_type": "int",
   "id": 1
}
```

## 使い方

プログラムを以下の形式で実行してください

1. ターミナルでserver.pyを立ち上げます
```bash
$ python RPC-server.py
```
2. 別のターミナルでclient.pyを立ち上げる
```bash
$ nodejs node RPC-client.js
```

#### 使用技術
<p style="display: inline">
<img src="https://img.shields.io/badge/-Linux-212121.svg?logo=linux&style=popout">
<img src="https://img.shields.io/badge/-Python-FFC107.svg?logo=python&style=popout">
<img src="https://img.shields.io/badge/-Node.js-339933.svg?logo=node.js&style=flat-square">
</p>

&nbsp;

## 環境構築
### 開発環境
| OS・言語・ライブラリ | バージョン |
| :------- | :------ |
| Ubuntu | 22.04.4 LTS |
| Python | 3.10.12 |
| Node.js | 22.3.0 |

&nbsp;

&nbsp;
