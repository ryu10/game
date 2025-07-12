# pico switch messenger

from machine import Pin
import time
import json
import select
import sys

debounce_delay = 0.01 # debounce delay in seconds

class Button:
    # define button status 
    pressed = False
    just_pressed = False
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)


    def is_pressed(self): 
        # Check if the button is pressed (active low)
        # Returns True if it has just been pressed (previous status was "not pressed" and the current status is "pressed")
        # check debounce before determining the state
        if not self.pin.value() != self.pressed:
            time.sleep(debounce_delay)
            # check again 
            if not self.pin.value() != self.pressed:
                self.pressed = not self.pressed
        # update the status 'just_pressed'
        if self.pressed and not self.just_pressed:
            self.just_pressed = True
            return True
        if not self.pressed:
            self.just_pressed = False
        return False

# send json message to serial 
# message like {"time": time_ticks/1000, "event": "pressed", "state": { "start_button": true, "position" : true }} # position true if pressed
def send_message(event, state):
    message = {
        "time": time.ticks_ms() / 1000,
        "event": event,
        "state": state
    }
    print(json.dumps(message))

# Init serial read polling
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)
serial_input_buf = []

# Receive json message from serial
def receive_message():
    events = poll_obj.poll(1)  # Poll for events with a timeout of 0ms (non-blocking)
    for obj, event in events:
        if obj == sys.stdin and event & select.POLLIN:
            # Read a char from stdin and append to serial input buffer
            char = sys.stdin.read(1)
            serial_input_buf.append(char)
            # Check for complete JSON messages in the buffer
            if "\n" in serial_input_buf:
                line = "".join(serial_input_buf)
                serial_input_buf.clear()
                if line:
                    try:
                        message = json.loads(line)
                        return message
                    except json.JSONDecodeError:
                        print("Invalid JSON received:", line)
                        serial_input_buf.clear()
    # If no complete message is found, return None
    return None  

# Global variables
start_button_pin = 7 # start button
main_button_pin = 6 # main button
start_button = Button(start_button_pin)
main_button = Button(main_button_pin)


# Main loop to monitor button presses
while True:
    if start_button.is_pressed():
        send_message("button", {"start_button": True, "pressed": True})
    elif main_button.is_pressed():
        send_message("button", {"main_button": True, "pressed": True})
    else:
        mesg = receive_message()
        if mesg != None:
            print("Received message:", mesg)