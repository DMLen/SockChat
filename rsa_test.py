from message import Message
import rsa

msg = Message(1, "Alice", "Hello, Bob!")

print(msg)

clientPubKey, clientPrivKey = rsa.newkeys(1024)
msg.encrypt(clientPubKey)
print(msg)

msg.decrypt(clientPrivKey)
print(msg)
