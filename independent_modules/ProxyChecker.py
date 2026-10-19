import multiprocessing
import queue
from concurrent.futures import ThreadPoolExecutor
from os import path

import socks
from socks import PROXY_TYPE_SOCKS5


class ProxyChecker:
    instance = None
    def __init__(self):
        self.process = multiprocessing.Process(target=self.startThreads, )
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.file_data = None
            self.proxies = []
            if path.isfile("config/proxies_socks5.txt"):
                self.proxies_unchecked = queue.Queue()
                self.loadProxies()
                print("Sprawdzanie proxies...")
                self.process.start()
                print(self.proxies)
            else:
                print("Nie znaleziono pliku (proxies_socks5).txt).. Tworzenie")
                try:
                    f = open("config/proxies_socks5.txt", "x")

                except Exception as e:
                    print(e)
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    def getProxyCount(self):
        return len(self.proxies)
    def checkProxies(self):
        process = multiprocessing.Process(target=self.startThreads,)
        process.start()
    def startThreads(self):
        with ThreadPoolExecutor(max_workers=32) as executor:
            for i in range(32):
                executor.submit(self.checkProxy)

        return len(self.proxies)
    def checkProxy(self):
        self.proxies.clear()
        if (self.proxies_unchecked.qsize()) == 0:
            self.loadProxies()
            if self.proxies_unchecked.qsize() == 0:
                return
        while self.proxies_unchecked.qsize() > 0:
            data = self.proxies_unchecked.get()
            self.proxies_unchecked.task_done()
            proxy = data.split(":")
            ip = proxy[0]
            port = int(proxy[1])
            s = socks.socksocket()
            s.settimeout(2)
            s.set_proxy(proxy_type=PROXY_TYPE_SOCKS5, addr=ip, port=port )
            try:
                s.connect(("www.google.com", 80))
                self.proxies.append(f"{ip}:{port}")
            except Exception as e:
                pass

    def loadProxies(self):
        with open("config/proxies_socks5.txt", "r") as f:
          self.file_data = f.read()
          if self.proxies_unchecked.qsize() > 0:
              for i in range(self.proxies_unchecked.qsize()):
                  self.proxies_unchecked.get()
                  self.proxies_unchecked.task_done()

          for line in self.file_data.split("\n"):
              self.proxies_unchecked.put(line)





