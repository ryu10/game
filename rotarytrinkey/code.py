# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Based on Adafruit sample program for Rotary Trinkey
# to be used with pong2.py

import rotaryio
import board
import time

encoder = rotaryio.IncrementalEncoder(board.ROTB, board.ROTA)
last_position = None
while True:
    position = encoder.position
    t = time.monotonic()
    if last_position is None or position != last_position:
        if last_position is None or position > last_position:
            dir = "CW"
        else:
            dir = "CCW"
        print(f"{{\"time\": {t}, \"event\": \"change\", \"state\": {{\"re0\": {{\"direction\": \"{dir}\", \"position\": {position}}}}}}}")
    last_position = position
