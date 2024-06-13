from message import Message
import pickle
import socket

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

### EXECUTION


username = input("Enter your username: ")
host = input("Enter host address (IPv4): ")
port = int(input("Enter port number: "))

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))
idcounter = 0

while True:
    content = input("> ")
    if content.startswith(("#")):
        handleCommand(content)
    else:
        msg = Message(idcounter, username, content)
        idcounter += 1

        clientsocket.send(msg.serialize())