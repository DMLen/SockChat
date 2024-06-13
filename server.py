from message import Message
from command import Command
import pickle
import socket
import threading

### CONFIG VARIABLES ###

host = 'localhost'
port = 5000      

### END CONFIG ###

def displaybanner():
    banner = f"""   SockChat == SERVER
Running on host: {host}
Running on port: {port}"""
    print(banner)


clientlst = [] #list of current client sockets for broadcasting

def handleClient(clientsocket):
    try:
        while True:
            data = clientsocket.recv(1024)
            if not data:
                break
            else:
                msg = pickle.loads(data)
                if msg.cmd == True:
                    handleUserCommand(msg.content, clientsocket) #handle user commands on the serverside
                else:
                    print(f"> {addr} {msg}") #deserialize message and print it
                    for client in clientlst: #broadcast received message to all current client sockets
                        client.sendall(data)
    except (BrokenPipeError, ConnectionResetError):
        print(f"Connection closed: {addr}")

    finally:
        clientlst.remove(clientsocket)
        clientsocket.close()

def handleUserCommand(input, clientsocket): #handle commands received from clients
    command = input.replace("#", "")

    if command == "ping":
        cmd = Command(0, "server", "pong")
        clientsocket.send(cmd.serialize())
    
    else:
        print(f"Unknown command received from {clientsocket}! This should never be displayed!")

### EXECUTION

displaybanner()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(10)

while True:
    clientsocket, addr = serversocket.accept()
    print(f"Incoming connection: {addr}")
    clientlst.append(clientsocket)
    client_thread = threading.Thread(target=handleClient, args=(clientsocket,))
    client_thread.start()

