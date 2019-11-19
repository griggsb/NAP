import socket, threading


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
    def run(self):
        msg = ''
        while True:
            msg = ''
            sendstring = ''
            data = self.csocket.recv(2048)
            msg = data.decode()
            if (len(msg)>0):
                if (msg=="quit"):
                    print("socket closed")
                    self.csocket.close()
                    break
                elif(msg[0]=='$'):
                    if(len(msg) > 1):
                        reqFile = msg[1:]
                        file_to_read = open(reqFile,'r')
                        l = file_to_read.read(2048)
                        while (l):
                            self.csocket.send(l.encode('utf-8'))
                            l = file_to_read.read(2048)
                        print ('Send Successful')
                        file_to_read.close()

        print ("user disconnected...")
LOCALHOST = "127.0.0.2"
PORT = 8081
server = socket.socket()
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
