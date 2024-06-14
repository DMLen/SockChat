from message import Message
from command import Command
import pickle
import socket
import threading
import rsa

### CONFIG VARIABLES ###

host = 'localhost' #192.168.0.200
port = 5000   

#portforwarding note: for port forwarding, the host ip should be the ip of the device running this code.
#make sure you have a port forwarding rule set up on the router to forward the port to this device!
#to connect, clients will have to input the PUBLIC IP of your router!

### END CONFIG ###

def displaybanner():
    banner = f"""   SockChat == SERVER
Running on host: {host}
Running on port: {port}\n"""
    print(banner)

serverPubKey, serverPrivKey = rsa.newkeys(1024)

clientlst = [] #list of current client sockets for broadcasting

keydict = {} #dictionary to store public keys of clients

def handleClient(clientsocket):
    try:
        while True:
            data = clientsocket.recv(1024)
            if not data:
                break
            else:
                msg = pickle.loads(data)
                if msg.cmd == True:
                    handleUserCommand(msg, clientsocket) #handle user commands on the serverside
                else:
                    if msg.encrypted == True: #if the message is encrypted, decrypt it
                        print(f"Debug: Encrypted message received: {msg}")
                        msg.decrypt(serverPrivKey) #decrypt it with the server's priv key
                        print(f"Debug: Decrypted message: {msg}")


                    print(f"> {addr} {msg}") #deserialize message and print it to local console
                    
                    #send message as broadcast to all current client sockets
                    #make sure it is uniquely encrypted for each client!

                    for client in clientlst:
                        broadcast = Message(msg.id, msg.sender, msg.content)
                        broadcast.timestamp = msg.timestamp
                        broadcast.encrypt(keydict[client])
                        client.sendall(broadcast.serialize())



    except (BrokenPipeError, ConnectionResetError):
        print(f"Connection closed: {addr}")

    except Exception as err: #try catch general other errors, such as deserialization error or receiving misformatted data
        print(f"An error occurred: {err}")

    finally:
        clientlst.remove(clientsocket)
        clientsocket.close()

def handleUserCommand(input, clientsocket): #handle commands received from clients
    parts = input.content.replace("#", "").split(' ', 1)  # split input into command and arguments
    command = parts[0]
    args = parts[1] if len(parts) > 1 else None  # if there are arguments, assign them to args

    if command == "ping":
        cmd = Command(0, "server", "pong")
        clientsocket.send(cmd.serialize())

    elif command == "notifynamechange": #notify all other users of namechange
        oldname, newname = args.split(' ', 1)
        print(f"User {oldname} has changed their name to {newname}!")

        msg = Message(0, "server", f"{oldname} has changed their username to {newname}")
        for client in clientlst:
            client.send(msg.serialize())

    elif command == "handshake": #receive public key from client and store it in keydict
        clientPubKey = pickle.loads(input.payload)
        print(f"Debug: Key {clientPubKey} received from client!")
        keydict[clientsocket] = clientPubKey
        print(f"Debug: Keydict: {keydict}")

        cmd = Command(0, "server", "handshakeresponse")
        cmd.addPayload(pickle.dumps(serverPubKey))
        clientsocket.send(cmd.serialize())

    elif command == "encryptiontest": #send encrypted message to client
        print(f"{addr} requested an encrypted message! Sending...")
        msg = Message(0, "server <Private>", "This is an encrypted message! If you can read this, it appears to be working. Nobody else can see this message.")
        msg.encrypt(keydict[clientsocket])
        clientsocket.send(msg.serialize())
    
    else:
        print(f"Unknown command received from {addr}! This should never be displayed!")

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

