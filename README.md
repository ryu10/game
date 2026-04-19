# pong

```
pip install pygame
python pong.py
```

# click game

```
pip install pygame
python click.py
```

# click game with external buttons

```
python click2.py
```

[hardware description](click2.md)

# click game w/ External buttons + LED feedback

```
pipenv shell
python3 click3.py
```

Also : 

` DISPLAY=:0 python3 click3.py ` ... if you want to run it from a remoote terminal

`sudo systemctl disable serial-getty@ttyACM0.service` ... Prevent controller USB port from being used as a serial console (Linux)

`sudo systemctl mask serial-getty@ttyACM0.service` ... Mask the serial login session permanently

# puyo
puyo

version: solo play 

```
python puyo2.py
```

version: battle vs CPU  

```
python puyo3.py
```
