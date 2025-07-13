
import _thread
from time import sleep
import random

from LedArray import LedArray  # Assuming LedArray is defined in a separate module

leds = LedArray()
leds.led_array_start()  # Start the LED run process

while True:
    try:
        for i in range (32):  # wait for 32 seconds, meanwhile randomly change interval times
            if random.randint(0, 4) == 0:
                leds.swap_intervals()
            sleep(1)
        if leds.interval < leds.interval2:
            leds.swap_intervals()
        leds.led_pattern = (leds.led_pattern + 1) % 2  # Change pattern
        with leds.lock:
            leds.go = False
        print(f"Changed led_pattern to {leds.led_pattern}")
        sleep(0.3)  # Allow time for the thread to stop
        print(f"go: {leds.go}")
    except KeyboardInterrupt:
        print("Stopping LED run thread.")
        with leds.lock:
            go = False
        sleep(1)
        # turn off all LEDs when the thread exits
        leds.strip.fill((0, 0, 0))
        leds.strip.write()
        print("Pattern 1 ended")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        with leds.lock:
           leds.go = False
        sleep(1)
        # turn off all LEDs when the thread exits
        leds.strip.fill((0, 0, 0))
        leds.strip.write()
        print("Pattern 1 ended")
        break  