# 

from GameMessages import GameMessages 

msg_system = GameMessages()

# Main loop to monitor button presses
while True:
    if msg_system.start_button.is_pressed():
        msg_system.send_message("button", {"start_button": True, "pressed": True})
    elif msg_system.main_button.is_pressed():
        msg_system.send_message("button", {"main_button": True, "pressed": True})
    else:
        mesg = msg_system.receive_message()
        if mesg != None:
            print("Received message:", mesg)