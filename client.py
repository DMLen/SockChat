from message import Message
from command import Command
from pingtimer import PingTimer
import pickle
import socket
import threading
import rsa

def displaybanner():
    print("SockChat == CLIENT\n")

pinger = PingTimer()
encryptionmode = False
idcounter = 0

def changeUsername(new_username):
    global username
    username = new_username

def keyExchange():
    cmd = Command(idcounter, username, "handshake")
    cmd.addPayload( pickle.dumps(clientPubKey) )
    clientsocket.send(cmd.serialize())
    print(f"Debug: Client public key sent to server!")

def handleCommand(input): #handle commands entered by user, and if neccessary, send them to the server
    parts = input.replace("#", "").split(' ', 1)  # split input into command and arguments
    command = parts[0]
    args = parts[1] if len(parts) > 1 else None  # if there are arguments, assign them to args
    global idcounter
    idcounter += 1

    if command == "exit":
        clientsocket.close()
        exit()

    elif command == "help":
        print(helpmsg)

    elif command == "ping":
        cmd = Command(idcounter, username, "ping")
        pinger.start()
        clientsocket.send(cmd.serialize())

    elif command == "changename":
        args = args.strip()
        if args is not None and args not in ["server", ""]:
            oldname = username
            changeUsername(args)
            cmd = Command(idcounter, username, f"notifynamechange {oldname} {args}")
            clientsocket.send(cmd.serialize())
        else:
            print("Please provide a valid username.")

    elif command == "encryptiontest":
        print("Prompting server to send an encrypted message...")
        cmd = Command(idcounter, username, "encryptiontest")
        clientsocket.send(cmd.serialize())
    
    else:
        print("Unknown command! Enter \"#help\" to see a list of commands!")

def handleResponse(input): #handle command responses from the server
    command = input.content.replace("#", "")

    if command == "pong":
        pinger.stop()
        print("Pong! Response received from server!")
        print(f"Elapsed time: {pinger.get()} ms")

    elif command == "handshakeresponse":
        global serverPubKey
        serverPubKey = pickle.loads(input.payload)
        print(f"Debug: Server public key received!")
        global encryptionmode
        encryptionmode = True
        print(f"Debug: Encryption mode {encryptionmode}")


    else:
        print(f"Unknown command received from server! This should never be displayed! Command: {command}")




helpmsg = """Commands:
#help - Displays this message
#exit - Exits the program
#ping - Pings the server
#changename <name> - Changes your username (Will be broadcast to all users)
#encryptiontest - Prompt the server to send an encrypted message. Only you will receive the message."""

def handleMessage(): #also handle receiving messages from the server
    while True:
        data = clientsocket.recv(1024)
        if not data:
            break
        msg = pickle.loads(data)

        if msg.cmd == True: #if the input data is a special response from the server, handle it appropriately
            handleResponse(msg)
        else:
            if msg.encrypted == True:
                print(f"Debug: Encrypted message received: {msg}")
                msg.decrypt(clientPrivKey)
                print(f"Debug: Decrypted message: {msg}")   
            print(f"> {msg}")

clientPubKey, clientPrivKey = rsa.newkeys(1024)
serverPubKey = None #public key of the server. will be received after the handshake is completed.

### EXECUTION

displaybanner()

while True:
    username = input("Enter your username: ")
    username = username.strip()
    if username in ["server", ""]:
        print("Invalid username!")
    else:
        break

host = input("Enter host address (IPv4): ")
port = int(input("Enter port number: "))
print("\n")

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))

receive_thread = threading.Thread(target=handleMessage)
receive_thread.start()

keyExchange()

print("Commands can be viewed by entering \"#help\"!\n")

while True:
    content = input("")
    if content.startswith(("#")):
        handleCommand(content)
    else:
        msg = Message(idcounter, username, content)
        idcounter += 1

        if encryptionmode == True:
            msg.encrypt(serverPubKey)
            msg.encrypted = True
            clientsocket.send(msg.serialize())
        
        else:
            clientsocket.send(msg.serialize())
