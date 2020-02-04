rcc web
=======

RCCのWeb班の成果物


## Description
読解問題を解くAPI


## Requirements
- Python 3
- Flask


## Usage
### APIを起動
```sh
$ python api.py
```
### POSTリクエストで推論結果を得る
1. {text: 対象のテキスト, question: 問題文, choices: 選択肢}
2. 推論結果をjsonで受け取る


## Installation
```sh
$ git clone https://github.com/AjxLab/rcc_web
$ cd rcc_web
$ pip install -r requirements.txt
```
