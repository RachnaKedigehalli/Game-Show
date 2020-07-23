import socket
import sys
import select

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("")
port = 9003
client.connect((host, port))

flag = False
while True:
    if flag == True:
        break
    inputs = [sys.stdin, client]
    read, write, error = select.select(inputs, [], [])
    for s in read:
        if s == client:
            msg = client.recv(1024)
            msg = msg.decode("utf-8")
            sys.stdout.write(msg)
            if "Exit" in msg:
                sys.stdin.flush()
                flag = True
                break
        elif s == sys.stdin:
            msg = sys.stdin.readline()
            client.send(bytes(msg, "utf-8"))
            sys.stdin.flush()
