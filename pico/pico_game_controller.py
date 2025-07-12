# pico_game_controller. 
# 1. ボタンの状態を読み取り、押し下げ情報を Json メッセージとして USB シリアルへ送信する。
# 2. USB シリアルから Json メッセージを読み取り、LED ストリップを光らせる。

# VSCode MicroPico 環境では、Upload to Pico コマンドを使ってこれらのライブラリファイルを Pico へあらかじめアップロードしておく。

from GameMessages import GameMessages
from LedArray import LedArray
import json

msg_system = GameMessages()
leds = LedArray()

# 初期化
leds.led_array_start()  # LED 実行プロセスをサブコアで起動

# メインループ
while True:
    try:
        # ボタンの状態をチェック
        if msg_system.start_button.is_pressed():
            msg_system.send_message("button", {"start_button": True, "pressed": True})
        elif msg_system.main_button.is_pressed():
            msg_system.send_message("button", {"main_button": True, "pressed": True})
        else:
            # USB シリアルからメッセージを受信
            mesg = msg_system.receive_message()
            if mesg is not None:
                print("Received message:", mesg)
                # 受信したメッセージに基づいて LED ストリップを制御
                leds.process_message(mesg)

    except KeyboardInterrupt:
        print("Stopping LED run thread.")
        leds.stop()  # LED ストリップを停止
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        leds.stop()  # エラー時も LED ストリップを停止
        break