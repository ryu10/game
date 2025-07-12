# rp2040 rotary encoder (RE)
# This micropython code is for the REs connected to a Raspberry Pi Pico
# Orig: by Yuya Kato https://zenn.dev/yuyakato/articles/8c148a11a8bbb7

from machine import Pin
import utime
import sys
import time
import json

pin_re0_r = 2
pin_re0_l = 3
pin_re1_r = 5
pin_re1_l = 4

class RotaryEncoder:
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.position = 0
        self.last_pin_a = pin_a.value()

    def read(self):
        current_pin_a = self.pin_a.value()
        current_pin_b = self.pin_b.value()
        direction = None
        if current_pin_a != self.last_pin_a:
            if current_pin_b != current_pin_a:
                self.position += 1
                direction = "CW"
            else:
                self.position -= 1
                direction = "CCW"
        self.last_pin_a = current_pin_a
        return (direction, self.position)

re0 = RotaryEncoder(Pin(pin_re0_r, Pin.IN, Pin.PULL_UP), Pin(pin_re0_l, Pin.IN, Pin.PULL_UP))
re1 = RotaryEncoder(Pin(pin_re1_r, Pin.IN, Pin.PULL_UP), Pin(pin_re1_l, Pin.IN, Pin.PULL_UP))

print(json.dumps({
    "time": time.ticks_ms() / 1000,
    "event": "init",
}))

while True:
    re0_state = re0.read()
    if re0_state[0] is not None:
        print(json.dumps({
            "time": time.ticks_ms() / 1000,
            "event": "change",
            "state": {
                "re0": {"direction": re0_state[0], "position": re0_state[1]},
            },
        }))
    re1_state = re1.read()
    if re1_state[0] is not None:
        print(json.dumps({
            "time": time.ticks_ms() / 1000,
            "event": "change",
            "state": {
                "re1": {"direction": re1_state[0], "position": re1_state[1]},
            },
        }))
    utime.sleep(0.001)


