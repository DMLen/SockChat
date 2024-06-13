from datetime import datetime
import pickle

class Command():
    def __init__(self, id, sender, content):
        self.id = id
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now()
        self.cmd = True 

    def __str__(self):
        return f"[{self.timestamp.strftime("%d/%m/%Y %H:%M:%S")}] {self.sender} sends command: {self.content}"
    
    def serialize(self):
        return pickle.dumps(self)