import socket, threading
import time                  # Import socket module
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

            # Create a socket object
s = socket.socket()
s2 = socket.socket()
IDlist = []

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
    def run(self):
        msgs = ''
        sendstrings = ''
        datas = self.csocket.recv(2048)
        message = datas.decode()
        msgs = message.split(' ')

        if (len(msgs)>0):
            print('hi')
            if (msgs[0]=='quit'):
                print("socket closed")
                self.csocket.close()
            elif(msgs[0]=='retr'):
                reqFile = msgs[1]
                file_to_read = open(reqFile,"rb")
                l = file_to_read.read()
                while (l):
                    self.csocket.send(l)
                    l = file_to_read.read()
                print ('Send Successful')
                file_to_read.close()

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        LOCALHOST = "127.0.0.3"
        PORT = 8082
        server = socket.socket()
        server.bind((LOCALHOST, PORT))
        while True:
             server.listen(1)
             clientsock, clientAddress = server.accept()
             newthread = ClientThread(clientAddress, clientsock)
             newthread.start()


def connection_click(host, port):
    global s
    s.connect((host,int(port)))
    print('connected to server')
    sendString = "^" + e3.get() + ", " + e4.get() + ", " + variable.get()
    s.sendall(sendString.encode('utf-8'))
    filename='filelist.txt'
    f = open(filename,'rb')
    l = f.read(1024)
    time.sleep(1)
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()


def disconnection_click():
    global s
    s.send(bytes("quit",'utf-8'))
    s.close()
    print("disconnected from server")
    s = socket.socket()

def search_click():
    global s
    global tv
    global IDlist
    s.send(bytes("@"+ e6.get(),'utf-8'))
    data = s.recv(2048)
    y = 0
    while y < len(IDlist):
        tv.delete(IDlist[y])
        y+=1
    IDlist = []

    while True:
        msg = data.decode()
        info = msg.split(', ')
        if not data:
            break
        i = 0
        while i < len(info):
            if((i+1)%3==0):
               IDlist.append(tv.insert('','end',text=info[i],values=(info[i-1],info[i-2])))
            i +=1
        break

def go_click():
    global T
    global s2
    line = []

    T.config(state=NORMAL)
    T.insert(END,">>"+e5.get()+"\n")
    line = e5.get().split(" ")
    if line[0] == "connect":
        try:
            s2.connect((line[1],int(line[2])))
            T.insert(END,"Connected to "+line[1]+":"+line[2]+"\n")
        except Exception as e:
            T.insert(END,"failure to connect: " + str(e) + "\n")
    if line[0] == "quit":
        try:
            s2.send(bytes(line[0],'utf-8'))
            s2.close
            T.insert(END,"Disconnected from server\n")
        except Exception as e:
            T.insert(END,"failure to disconnect: "+str(e)+"\n")

    if line[0] == "retr":
            s2.send(bytes(line[0]+' '+line[1],'utf-8'))
            filename=line[1]
            f = open(filename,"w")
            data = s2.recv(1024).decode()
            f.write(data)
            f.close()
            print('file retrieved')


master = Tk()
master.title("nap p2p network")
Label(master, text="server hostname").grid(row=0)
Label(master, text="port").grid(row=0, column=2)
Label(master, text="username").grid(row=1)
Label(master, text="hostname").grid(row=1,column=2)
Label(master, text="speed").grid(row=1, column=4)
Label(master, text="command").grid(row=6, column=0)
Label(master, text="keyword").grid(row=4, column=0)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e4.insert(END,"127.0.0.3:8082")
e5 = Entry(master, width = 50)
e6 = Entry(master, width = 50)
e1.grid(row=0, column=1)
e2.grid(row=0, column=3)
e3.grid(row=1, column=1)
e4.grid(row=1, column=3)
e5.grid(row=6, column=1, columnspan=3)
e6.grid(row=4, column=1, columnspan=3)

T = Text(master, height=10, width=70)
T.grid(row=7, columnspan=6)
T.config(state=DISABLED)

Button(master, text='Connect', command =(lambda: connection_click(e1.get(),e2.get()))).grid(row=0, column=5, sticky=W, pady=4)
Button(master, text='Disconnect', command =(lambda: disconnection_click())).grid(row=0, column=6, sticky=W, pady=4)
Button(master, text='Search', command =(lambda: search_click())).grid(row=4, column=5, sticky=W, pady=4)
Button(master, text='Go', command =(lambda: go_click())).grid(row=6, column=5, sticky=W, pady=4)

variable = StringVar(master)
variable.set("None") # default value
w = OptionMenu(master, variable,"Ethernet","Ethernet","Modem","T1","T3")
w.grid(row=1, column=5)

tv = Treeview(master)
tv['columns'] = ('hostname', 'filename')
tv.heading("#0", text='Speed', anchor='w')
tv.column("#0", anchor="w")
tv.heading('hostname', text='host name')
tv.column('hostname', anchor='center', width=100)
tv.heading('filename', text='file name')
tv.column('filename', anchor='center', width=100)
tv.grid(row=5,columnspan=6)
master.treeview = tv
master.grid_rowconfigure(5, weight = 1)

newthread = ServerThread()
newthread.start()

mainloop()
print("GUI closed")

