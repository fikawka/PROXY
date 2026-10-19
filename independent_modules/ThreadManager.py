import queue
import threading
import time


class ThreadManager(threading.Thread):
    listaThreads = []
    que_add = queue.Queue()
    que_remove = queue.Queue()
    stop_que = queue.Queue()
    def run(self):
        while True:
            while self.que_add.qsize() > 0:
                #print("Adding thread")
                t = self.que_add.get()
                self.listaThreads.append(t)
                t.start()
            while self.que_remove.qsize() > 0:
                try:
                    t = self.que_remove.get()
                    #print("Disconnecting threads")
                    if t.is_alive():
                        t.join()
                    if t in self.listaThreads:
                        self.listaThreads.remove(t)
                except Exception as e:
                    print(e)
            while self.stop_que.qsize() > 0:
                t = self.stop_que.get()
                if t.is_alive():
                    t.join()
            time.sleep(0.001)
    @classmethod
    def addThread(cls, thread: threading.Thread):
        cls.que_add.put(thread)

    @classmethod
    def disconnectPlayerThread(cls, thread: threading.Thread):
        cls.que_remove.put(thread)
    @classmethod
    def stop_thread(cls, thread):
        cls.stop_que.put(thread)





