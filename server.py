import socket
from  threading import Thread
import time, random

SERVER = None
IP_ADDRESS = '127.0.0.1'
PORT = 8000

CLIENTS = {}
flashNumberList =[ i  for i in range(1, 91)]
playersJoined = False

def handleClient():
    global CLIENTS
    global flashNumberList
    global playersJoined

    while True:
        try:
            if(len(list(CLIENTS.keys())) >=2):
                if(not playersJoined):
                    playersJoined = True
                    time.sleep(1)

                if(len(flashNumberList) > 0):
                    randomNumber = random.choice(flashNumberList)
                    currentName = None
                    try:
                        for cName in CLIENTS:
                            currentName = cName
                            cSocket = CLIENTS[cName]["player_socket"]
                            cSocket.send(str(randomNumber).encode())

                        flashNumberList.remove(int(randomNumber))
                    except:
                        del CLIENTS[currentName]
                    time.sleep(3)
        except:
            pass

def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()

        CLIENTS[player_name] = {}
        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["address"] = addr
        CLIENTS[player_name]["player_name"] = player_name

        print(f"Connection established with {player_name} : {addr}")

def setup():
    print("\n\t\t\t\t\t*** Welcome To Tambola Game ***\n")

    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    thread = Thread(target = handleClient, args=())
    thread.start()

    acceptConnections()
setup()

