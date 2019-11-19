import socket, threading
global ufiles
global users
users = {}
ufiles = {}

countusers = 0
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
            print(msg)
            if(len(msg)>0):
                if msg[0]=='^':
                    sp = ''
                    sp = msg[1:].split(", ")
                    print ("User '" + sp[0]+"' has joined")
                    users[sp[1]] = [sp[0],sp[2]]
                    ufiles[sp[1]] = []
                    print('user registered')
                elif msg=="quit":
                    self.csocket.close()
                    del users[sp[1]]
                    del ufiles[sp[1]]
                    break
                elif msg[0]=='@':
                    sp3 = msg[1:]
                    previous = ''
                    sendstring = ''
                    for key, value in ufiles.items():
                        print (''+key)
                        print(value)
                    for key, value in ufiles.items():
                        it = 0
                        while it < len(value):
                            if ((it+2)%2 == 1):
                                if (value[it].find(sp3)>-1):
                                    sendstring = sendstring+previous+", "+key+", " + users[key][1]+", "
                            previous = value[it]
                            it +=1
                    self.csocket.sendall(sendstring.encode('utf-8'))
                else:
                    print('files registered')
                    files = []
                    sp2 = msg.split(",\n")
                    i = 0
                    while i < len(sp2):
                            print(sp2[i])
                            files.append(sp2[i])
                            i += 1
                    x=0
                    ufiles[sp[1]] = files
        print ("user '", sp[0], "' disconnected...")
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket()
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
