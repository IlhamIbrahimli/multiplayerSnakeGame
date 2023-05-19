from classes import *
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = input("Enter IP:")

name = input("Enter your name.Max 3 characters:")
if len(name) > 3:
    name = name[:3]
elif len(name) < 3:
    name = name + "E"

server_address = (ip, 12345)
sock.connect(server_address)
isReady = sock.recv(1)
while isReady.decode() != "1":
    isReady = sock.recv(1)
game = Game(sock, name)
game.run()
