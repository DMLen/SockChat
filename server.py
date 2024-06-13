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

clientlst = [] #list of current client sockets for broadcasting

def handleClient(clientsocket):
    try:
        while True:
            data = clientsocket.recv(1024)
            if not data:
                break
            else:
                print(pickle.loads(data)) #deserialize message and print it
                for client in clientlst: #broadcast received message to all current client sockets
                    client.sendall(data)
    except (BrokenPipeError, ConnectionResetError):
        print(f"Connection closed: {addr}")

    finally:
        clientlst.remove(clientsocket)
        clientsocket.close()

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

