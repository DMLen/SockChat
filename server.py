from message import Message
import pickle
import socket
import threading

### CONFIG VARIABLES ###

host = 'localhost'
port = 5000      

### END CONFIG ###

def displaybanner():
    print("SockChat == SERVER")

def handle_client(clientsocket):
    while True:
        data = clientsocket.recv(1024)
        if not data:
            break
        print(pickle.loads(data))
    print(f"Connection closed: {addr}")
    clientsocket.close()

### EXECUTION

displaybanner()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(10)

while True:
    clientsocket, addr = serversocket.accept()
    print(f"Incoming connection: {addr}")
    client_thread = threading.Thread(target=handle_client, args=(clientsocket,))
    client_thread.start()

