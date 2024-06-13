from datetime import datetime
import pickle

class Message():
    def __init__(self, id, sender, content):
        self.id = id
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now() 

    def __str__(self):
        return f"[{self.timestamp.strftime("%d/%m/%Y %H:%M:%S")}] {self.sender}: {self.content}"
    
    def serialize(self): #message can be deserialized with pickle.loads()
        return pickle.dumps(self)