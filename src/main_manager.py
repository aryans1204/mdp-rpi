from threading import Thread
from android_manager import AndroidManager
from wifi_manager import WifiManager

class MainComm:
    def __init__(self):
        self.AndroidManager = AndroidManager(self)
        self.WifiManager = WifiManager(self)
        #TODO STMManager
    
    def connect(self):
        #self.AndroidManager.connect()
        self.WifiManager.connect()
        self.AndroidManager.connect()
    
    def disconnect(self):
        self.AndroidManager.disconnect()
        self.WifiManager.disconnect()
    
    def startComm(self):
        print("Starting threads for communication")
        print("Hello")
        self.connect()

        tAndroidSend = Thread(target=self.AndroidManager.send, name="tAndroidSend")
        tPCSend = Thread(target=self.WifiManager.send, name="tPCSend")

        tAndroidListen = Thread(target=self.AndroidManager.listen, name="tAndroidListen")
        tPCListen = Thread(target=self.WifiManager.listen, name="tPCListen")

        tAndroidSend.start()
        tPCSend.start()

        tAndroidListen.start()
        tPCListen.start()
        print("All threads started")
        tAndroidSend.join()
        tPCSend.join()
        tAndroidListen.join()
        tPCListen.join()

        print("[MainComm] finisheed communication execution")
        self.disconnect()

mainComm = MainComm()
mainComm.startComm()
