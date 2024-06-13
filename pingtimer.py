import time

class PingTimer():
    def __init__(self):
        self.t1 = None
        self.t2 = None
        
    def start(self):
        self.t1 = time.time()

    def stop(self):
        self.t2 = time.time()

    def get(self):
        timeDiff = self.t2-self.t1
        return int(round(timeDiff * 1000))
    
