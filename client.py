import socket
import threading
import os
import time

PORT = 9999
FORMAT = 'utf-8'
SERVER = '192.168.56.1'
ADDR = (SERVER , PORT)

def init():
    print("1. Chat")
    print("2. Quit")
    temp = input("Enter Your Choice :-")
    if temp == "2":
        return False
    else:
        return True

def searching():
    while True:
        os.system('cls')
        print("Searching for clients . . .")
        time.sleep(2)
        if stop_search:
            print("connected")
            break

def receiving(client):
    client.recv(64).decode(FORMAT)
    global stop_search
    stop_search = True
    thread.join()

def receive(client):
    global stop_search
    try:
        while stop_search:
            msg = client.recv(64).decode(FORMAT)
            if msg == "bye":
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                print(msg)
                stop_search = False
                break
            print(msg)
    except:
        print("Connection closed by you!")

def send(client):
    try:
        while True:
            msg=input()
            if msg == "bye":
                msg=msg.encode(FORMAT)
                client.send(msg)
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                break
            msg=msg.encode(FORMAT)
            client.send(msg)
    except:
        print("Connection closed by other client!")
        

start = init()
os.system('cls')
while start:
    client = socket.socket()
    client.connect(ADDR)
    stop_search = False
    thread = threading.Thread(target=searching)
    thread.start()
    receiving(client)
    thread1 = threading.Thread(target=receive,args=(client,))
    thread2 = threading.Thread(target=send,args=(client,))
    thread1.start()
    thread2.start()
    while thread1.is_alive() and thread2.is_alive():
        continue
    if thread1.is_alive() == False or thread2.is_alive() == False:
        if thread1.is_alive() == False:
            thread2.join(1)
        else:
            thread1.join(1)
    start = init()

print("BYE!!!")