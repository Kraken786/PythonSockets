import socket
import threading
import time
#socket.gethostbyname(socket.gethostname())
PORT = 9999
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER , PORT)
FORMAT = 'utf-8'
server = socket.socket()
server.bind(ADDR)

def handleSend(client,c):
    msg="connected"
    msg=msg.encode(FORMAT)
    client.send(msg)
    connected = True
    try:
        while connected:
            while len(c):
                if c[0] == "bye":
                    connected = False
                    break
                msg = c[0]
                msg = msg.encode(FORMAT)
                client.send(msg)
                c.pop(0)
    except:
        print("Connection Closed")

def handleReceive(client,c):
    try:
        while True:
            msg = client.recv(64).decode(FORMAT)
            if msg == "bye":
                break
            c.append(msg)
        stop(client)
    except:
        print("Connection Closed")

def handle1(client,addr, c1, c2):
    print(f"{addr} Connected1!")
    t1 = threading.Thread(target=handleSend,args=(client,c2))
    t2 = threading.Thread(target=handleReceive,args=(client,c1))
    t1.start()
    t2.start()

def handle2(client, addr,c1, c2):
    print(f"{addr} Connected2!")
    t1 = threading.Thread(target=handleSend,args=(client,c1))
    t2 = threading.Thread(target=handleReceive,args=(client,c2))
    t1.start()
    t2.start()

def stop(client):
    if client == clients[0]:
        clients[0].shutdown(socket.SHUT_RDWR)
        clients[0].close()
        msg="bye"
        msg= msg.encode(FORMAT)
        clients[1].send(msg)
        time.sleep(2)
        clients[1].shutdown(socket.SHUT_RDWR)
        clients[1].close()
    else:
        clients[1].shutdown(socket.SHUT_RDWR)
        clients[1].close()
        msg="bye"
        msg= msg.encode(FORMAT)
        clients[0].send(msg)
        time.sleep(2)
        clients[0].shutdown(socket.SHUT_RDWR)
        clients[0].close()

def start():
    server.listen()
    print("Server started!")
    run = True
    while run:
        c1=[]
        c2=[]
        client1 , addr1 = server.accept()
        client2 , addr2 = server.accept()
        global clients
        clients = [client1,client2]
        thread1 = threading.Thread(target=handle1,args=(client1,addr1,c1,c2))
        thread2 = threading.Thread(target=handle2,args=(client2,addr2,c1,c2))
        thread1.start()
        thread2.start()
        print(f"Active Connections :-{threading.activeCount() - 1}")

print(f"Server is Starting on {ADDR}...")
start()