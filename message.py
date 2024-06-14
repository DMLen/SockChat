from datetime import datetime
import pickle
import rsa

class Message():
    def __init__(self, id, sender, content):
        self.id = id
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now()
        self.cmd = False #flipped to true only for the command child class.
        self.encrypted = False

    def __str__(self):
        return f"[{self.timestamp.strftime("%d/%m/%Y %H:%M:%S")}] {self.sender}: {self.content}"
    
    def serialize(self): #message can be deserialized with pickle.loads()
        return pickle.dumps(self)
    
    def encrypt(self, publicKey):
        self.content = rsa.encrypt(self.content.encode(), publicKey)
        self.encrypted = True
        
    def decrypt(self, privateKey):
        self.content = rsa.decrypt(self.content, privateKey).decode()
        self.encrypted = False