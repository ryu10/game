# led_array.py
#  Usage : import led_array
# 
# 以下は初期プロンプトです
# 同じディレクトリにある aled.py を参考にして次の機能を実装
# led_run() を別プロセスで実行
# 変数 go および led_pattern をグローバルに宣言
# led_run() は次の機能を持つ：
#  * run_pattern0(), run_pattern1(), run_pattern2(), run_pattern3() を呼び出す
#  * 各パターンは、go が True の間、特定の LED 点灯動作をループする。go が False になるとループを抜ける
#  * 各パターンは、go が False になると終了する
#  * 各パターンの終了後、go を True に戻す
#  * led_pattern の値が変更したことを検出したら、1) go を false に変更して run_pattern*() を終了させる
#  * run_pattern*() の終了後、go を true に戻し、led_pattern の値に応じて新しい run_pattern*() を呼び出す
# メインループはスタブとして、10 秒おきに led_pattern の値を変更する。ループする。

import machine
import neopixel
from utime import sleep
import _thread
import random

class LedArray:
    def __init__(self):
        # Define number of LEDs
        self.n0 = 32  # outer
        self.n1 = 24  # inner
        self.n = self.n0 + self.n1  # inner 24 + outer 32

        # interval
        self.interval = 0.07
        self.interval2 = 0.4

        self.data_pin = machine.Pin(5, machine.Pin.OUT)  # Use GPIO 5 for data pin

        self.strip = neopixel.NeoPixel(self.data_pin, self.n)
        self.pallette = {
            "red": (63, 0, 0),
            "green": (0, 63, 0),
            "blue": (0, 0, 63),
            "white": (63, 63, 63),
            "black": (0, 0, 0),
            "yellow": (63, 63, 0),
            "cyan": (0, 63, 63),
            "magenta": (63, 0, 63)
        }

        self.colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
        self.col = 0  # Color index for patterns

        # create a lock to manage access to shared variables
        self.lock = _thread.allocate_lock()

        # Global variables
        self.go = True
        self.led_pattern = 0 

    def led_array_start(self):  # Initiate the LED run process
        # Initiate the LED run process
        _thread.start_new_thread(self.led_run, ())
        # print("LED run thread started. Press Ctrl+C to stop.")

    def led_run(self):
        while True:
            if self.led_pattern == 0:
                self.run_pattern0()
            elif self.led_pattern == 1:
                self.run_pattern1()
            elif self.led_pattern == 2:
                self.run_pattern2()
            elif self.led_pattern == 3:
                self.run_pattern3()
            else:
                # print("Unknown pattern")
                break   
            sleep(0.1)  

    def swap_intervals(self): 
        with self.lock:
            t = self.interval
            self.interval = self.interval2
            self.interval2 = t
            # print(f"Swapped intervals: {self.interval}, {self.interval2}")

    def run_pattern0(self):  # demo pattern
        global go
        col = 0  # Reset color index for pattern 0
        while self.go:
            # print("Running Pattern 0")
            col = random.randint(0, len(self.colors) - 2)  # Randomly select a color
            for i in range(self.n):
                if not self.go:
                    break
                self.strip[i] = self.pallette[self.colors[col]]
                self.strip.write()
                sleep(self.interval)
                if not self.go:
                    break
                self.strip[i] = (0, 0, 0)  # Turn off the LED
                self.strip.write()
            col = random.randint(0, len(self.colors) - 2)  # Randomly select a color
            for i in range(0, self.n, 4):
                if not self.go:
                    break
                self.strip[i] = self.pallette[self.colors[col]]
                self.strip.write()
                sleep(self.interval2)
            for i in range(0, self.n, 4):
                if not self.go:
                    break
                self.strip[i] = (0, 0, 0)
                self.strip.write()
                sleep(self.interval2)
        # Reset the strip to off state
        self.strip.fill((0, 0, 0))
        self.strip.write()
        # print("Pattern 0 ended")
        with self.lock:
            self.go = True

    def run_pattern1(self): # slow effect
        global go
        col = 0  # Reset color index for pattern 0
        while self.go:
            col1 = random.randint(0, len(self.colors) - 2)  # Randomly select a color
            col2 = random.randint(0, len(self.colors) - 2)  # Randomly select a second color
            for i in range(0, self.n0, int(self.n0/8)):
                if not self.go:
                    break
                self.strip[i] = self.pallette[self.colors[col1]]
            for i in range(int(self.n1/16), self.n1, int(self.n1/8)):
                if not self.go:
                    break
                self.strip[self.n0 + i] = self.pallette[self.colors[col2]]  
                self.strip.write()
            sleep(self.interval)
            # Turn off all the leds
            self.strip.fill((0, 0, 0))
            self.strip.write()
            # switch the outer and inner colors
            for i in range(0, self.n0, int(self.n0/8)):
                if not self.go:
                    break
                self.strip[i] = self.pallette[self.colors[col2]]
            for i in range(int(self.n1/16), self.n1, int(self.n1/8)):
                if not self.go:
                    break
                self.strip[self.n0 + i] = self.pallette[self.colors[col1]]
                self.strip.write()
            sleep(self.interval)
            # Turn off all the leds
            self.strip.fill((0, 0, 0))
            # print("Running Pattern 1")
            if not self.go:
                break
        # turn off all LEDs when the thread exits
        self.strip.fill((0, 0, 0))
        self.strip.write()
        # print("Pattern 1 ended")
        with self.lock:
            self.go = True


    def run_pattern2(self): # Medium effect
        global go
        col = 0  # Reset color index for pattern 0
        while self.go:
            # print("Running Pattern 2")
            sleep(0.5)  # Simulate LED operation
            if not self.go:
                break
        # print("Pattern 2 ended")    
        with self.lock:
            self.go = True

    def run_pattern3(self): # Fast effect
        global go
        col = 0  # Reset color index for pattern 0
        while self.go:             
            # print("Running Pattern 3")
            sleep(0.5)  # Simulate LED operation
            if not self.go:
                break
        # print("Pattern 3 ended")    
        with self.lock:
            self.go = True  
