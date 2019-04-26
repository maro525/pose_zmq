# Pose Detection with Zmq 

A PoseNet GUI. PoseNet implementation is based on this(https://github.com/rwightman/posenet-python)

- 

## 環境
- Mac 10.14.4
- Python 3.7.3

## python packages
- `requirments.txt`
- GUI is made with Kivy(https://kivy.org/#home) 

## Install
1. clone this repository
2. `python3 -m venv ZMQ_PAGE_ENV` (ZMQ_PAGE_ENVの部分は任意)
3. `source ZMQ_PAGE_ENV/bin/activate`
4. `pip install -r requirments.txt`

## Usage
1. `source POZE_ZMQ_ENV/bin/activate`
2. `python main.py` (最初の実行はモデルをインストールするため、時間かかる)
3. To deactivate this env, `deactivate`

## GUI
![GUI](screen.png)

1. Top Left
    - ZMQ settings
    - push connect button to reconnect
        - default ip : "127.0.0.1" port : "3000"

2. Top Middle
    - Camera / Video settings
    - src
        - Camera : input src number 
        - Video : input path
        - defult : 
    - loadボタンで自動で切り替わる
        - デフォルトで、カメラ（ソース：0）が起動する
  
    - Showのトグルスイッチ
        - 切り替えによって、カメラ表示/非表示切り替え

3. Top Middle 
    - Posenet Parameter
    - Scale Factor
        - 画像をどのくらい小さくして処理するか
        - 大きいほど遅いが、小さすぎると精度減
    - Max Pose Num
        - 認識する人の最大数
        - 1~10
    - Min Pose Score
        - ポーズのスコアの閾値
    - Min Part Score
        - ポーズの部位のスコアの閾値

4. Bottom Left
    - 処理後の画像表示
 
5. Bottom Right
    - pose data in the frame 

## ファイル説明
- `main.py`
    - 実行ファイル
    - GUI event handle
- `main.kv`
    - style file
    - evnetbind setting
- `data_send.py`
    - zmq protocol handler
- `detection.py`
    - pose detector
- `video`
    - 動画ファイルを入れるフォルダ