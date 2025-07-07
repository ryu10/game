# pico switch messenger

from machine import Pin
    import time
    import json

class Button:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        return not self.pin.value()
    def wait_for_press(self):
        while not self.is_pressed():
            pass
        # Debounce delay
        self.wait_for_release()
    def wait_for_release(self):
        while self.is_pressed():
            pass    
    def just_now_pressed(self):
        if self.is_pressed():
            self.wait_for_release()
            return True
        return False

start_button_pin = 6 # start button
main_button_pin = 7 # main button
start_button = Button(start_button_pin)
main_button = Button(main_button_pin)

# send json message to serial 
# message like {"time": time_ticks/1000, "event": "pressed", "state": { "start_button": true, "position" : true }} # position true if pressed
def send_message(event, state):
    message = {
        "time": time.ticks_ms() / 1000,
        "event": event,
        "state": state
    }
    print(json.dumps(message))

# Main loop to monitor button presses
while True:
    if start_button.is_pressed():
        send_message("pressed", {"start_button": True, "position": True})
    elif main_button.is_pressed():
        send_message("pressed", {"main_button": True, "position": True})