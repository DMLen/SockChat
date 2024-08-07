# SockChat
*A basic socket messenger written in Python.*

A basic socket-based messenger written in Python. Operates off a server-client chatroom model, where multiple clients can connect to one server and all can see messages that are posted. Supports some basic commands, the prefix for which is the hash key (#). Enter "#help" to view some commands!

~~In its current state, messages sent are not secured! Do not send important information via this program!~~

SockChat now has RSA encryption. After an exchange of public keys between the client and server upon initial connection, all messages sent and received are encrypted. I would consider the implementation to be secure , but I still wouldn't send anything confidential over this.


## How to Run?
First, install the RSA library. This is used for encryption.

pip install rsa

**Server**: Edit *server.py* in an editor to view configurable options (currently the IP, port, and debugmode). 
For testing purposes, "localhost" for the IP is fine. Otherwise the IP should be the local IP of your device, and a port forwarding rule should be defined on your router that points to your device!
For port, any value is fine. I recommend leaving it at 5000.
When done, execute the file to start the server. 
Close the program at any time to exit.

**Client**: Execute *client.py*.
You may edit *client.py* in an editor to view configurable options (currently just debugmode)
When the program starts, you'll be asked to input a username, an IP, and a port.
The IP should be the *public-facing* IP address of the server (the one of the router, usually). Alternatively, a local IP will work for a LAN connection if the server is running on the same network. Localhost will work if the server is on the same device.
The port should be whatever port has been forwarded for the server (or whichever port is being used, assuming a LAN connection).
Assuming things were done correctly, you should now be connected to the server!
Type "#exit" at any time to disconnect from the server and close the program.

TODO:
1. Commands executed from server terminal (etc: forcefully disconnect clientsockets)
2. ~~Encryption mode~~ Program now uses RSA encryption
3. Tkinter GUI
