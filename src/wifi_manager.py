from queue import Queue
import socket
import json
import sys

class WifiManager:
    def __init__(self, MainComm):
        self.MainComm = MainComm
        self.ip_addr = RPI_IP
        self.port = PORT
        self.socket = None
        self.msg_queue = Queue()
    
    def connect(self):
        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serverSocket.bind((self.ip_addr, self.port))
            serverSocket.listen(128)
            self.socket, self.pc_addr = sock.accept()
        except socket.error as e:
            print("PC failed to connect ", str(e))
        else:
            print("PC Connected succesfully at: ", self.pc_addr)

    def disconnect(self):
        self.socket.close()
    
    def reconnect(self):
        self.disconnect()
        self.connect()
    
    def listen(self):
        while True:
            try:
                msg = self.socket.recv(PC_MSG_SIZE)
                if not msg:
                    print("PC disconnected, reconnecting")
                    self.reconnect()

                utfmsg = msg.decode('utf-8')
                if (len(utfmsg) <= 1):
                    continue
                    print("Error parsing message")
                print("Message received from PC: ", msg)
                pc_request = json.loads(utfmsg)
                request_type = pc_request["type"]

                if request_type == "NAV":
                    #send to STM
                    self.MainComm.STMManager.msg_queue.put(msg)
                
                elif request_type == "IMAGE":
                    #send to Android
                    self.MainComm.AndroidManager.msg_queue.put(msg)
                
                elif request_type == "COORD" or request_type == "PATH_PLAN":
                    #send to Android for display
                    self.MainComm.AndroidManager.msg_queue.put(msg)
                
                else:
                    print("Received unknown message from PC")
                
            except socket.error as e:
                print("PC SOCKET ERROR: ", str(e))
    
    def send(self):
        while True:
            msg = self.msg_queue.get()
            error = True
            while error:
                try:
                    self.socket.send(msg)
                    print("Write to PC: ", msg.decode('utf-8'))
                except Exception as e:
                    print("Error occured while writing to PC: ", str(e))
                else:
                    error = False

