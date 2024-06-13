# SockChat
*A basic socket messenger written in Python.*

A very basic socket-based messenger written in Python. Operates off a server-client chatroom model, where multiple clients can connect to one server and all can see messages that are posted. Supports some basic commands, the prefix for which is the hash key (#). Enter "#help" to view some commands!

In its current state, messages sent are not secured! Do not send important information via this program!

## How to Run?
**Server**: Edit *server.py* in an editor to view configurable options (currently the IP and port). 
For testing purposes, "localhost" for the IP is fine. Otherwise the IP should be the local IP of your device, and a port forwarding rule should be defined your router that points to your device!
For port, any value is fine. I recommend leaving it at 5000.
When done, execute the file to start the server. 
Close the program at any time to exit.

**Client**: Execute *client.py*.
When the program starts, you'll be asked to input a username, an IP, and a port.
The IP should be the *public* IP address of the server. That is, the IP of the router.
The port should be whatever port has been forwarded for the server.
Assuming things were done correctly, you should now be connected to the server!
Type "#exit" at any time to disconnect from the server and close the program.

TODO:
1. Commands executed from server terminal (etc: forcefully disconnect clientsockets)
2. Encryption mode
3. Tkinter GUI
