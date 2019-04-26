# Pose Detection with Zmq

## 環境
- Mac 10.14.4
- Python 3.7.3

## python packages
- `requirments.txt`

## インストール
1. clone this repository
2. `python3 -m venv ZMQ_PAGE_ENV` (ZMQ_PAGE_ENVの部分は任意)
3. `source activate ZMQ_PAGE_ENV/bin/activate`
4. `pip install -r requirments.txt`


## 実行
1. `source POZE_ZMQ_ENV/bin/activate`
2. `python main.py` (最初の実行はモデルをインストールするため、時間かかる)
終わるときは
3. `deactivate`