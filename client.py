from message import Message
import pickle
import socket
import threading

def displaybanner():
    print("SockChat == CLIENT")

def handleCommand(input):
    command = input.replace("#", "")

    if command == "exit":
        clientsocket.close()
        exit()

    elif command == "help":
        print(helpmsg)
    
    else:
        print("Unknown command! Enter \"#help\" to see a list of commands!")

helpmsg = """Commands:
#help - Displays this message
#exit - Exits the program"""

def handleMessage(): #also handle receiving messages from the server
    while True:
        data = clientsocket.recv(1024)
        if not data:
            break
        msg = pickle.loads(data)
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