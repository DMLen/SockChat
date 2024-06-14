from datetime import datetime
from message import Message
import pickle


class Command(Message):
    def __init__(self, id, sender, content):
        super().__init__(id, sender, content)
        self.cmd = True
        self.payload = None

    def addPayload(self, obj):
        self.payload = obj
    
