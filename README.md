# PongMultiplayer
A pong game for 2 players connected over sockets.

# Packages
Pygame is used to make the gui of the game

`pip install pygame`

# Usage
```
python main.py [-h] (-b | -ip ADDRESS) -p PORT

requiered arguments:
  -b, --bind            Binds the socket to this ip. Acts as host for game
    or
  -ip, --address        Ip address of the host

  -p, --port            Port to connect to

optional arguments:
  -h, --help            show this help message and exit
```
