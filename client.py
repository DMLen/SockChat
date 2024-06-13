from message import Message
from command import Command
from pingtimer import PingTimer
import pickle
import socket
import threading
import time

def displaybanner():
    print("SockChat == CLIENT")

pinger = PingTimer()

def handleCommand(input): #handle commands entered by user, and if neccessary, send them to the server
    command = input.replace("#", "")

    if command == "exit":
        clientsocket.close()
        exit()

    elif command == "help":
        print(helpmsg)

    elif command == "ping":
        cmd = Command(idcounter, username, "ping")
        pinger.start()
        clientsocket.send(cmd.serialize())
    
    else:
        print("Unknown command! Enter \"#help\" to see a list of commands!")

def handleResponse(input): #handle command responses from the server
    command = input.replace("#", "")

    if command == "pong":
        pinger.stop()
        print("Pong! Response received from server!")
        print(f"Elapsed time: {pinger.get()} seconds")




helpmsg = """Commands:
#help - Displays this message
#exit - Exits the program
#ping - Pings the server"""

def handleMessage(): #also handle receiving messages from the server
    while True:
        data = clientsocket.recv(1024)
        if not data:
            break
        msg = pickle.loads(data)

        if msg.cmd == True: #if the input data is a special response from the server, handle it appropriately
            handleResponse(msg.content)
        else:
            print(f"> {msg}")

### EXECUTION

username = input("Enter your username: ")
host = input("Enter host address (IPv4): ")
port = int(input("Enter port number: "))

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))
idcounter = 0

receive_thread = threading.Thread(target=handleMessage)
receive_thread.start()

while True:
    content = input("")
    if content.startswith(("#")):
        handleCommand(content)
    else:
        msg = Message(idcounter, username, content)
        idcounter += 1
        clientsocket.send(msg.serialize())