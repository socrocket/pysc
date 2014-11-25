import threading
from Queue import Queue

class Thread(threading.Thread):
    queues = []

    def __init__(self):
        super(Thread, self).__init__()
        self.queue = Queue()
        Thread.queues.append(self.queue)

    def run(self):
        # invoke whatever
        pass

    def stop(self):
        Thread.queues.remove(self.queue)
