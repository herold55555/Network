import socket
import sys

from os import listdir
from os.path import isfile, join
import os


def connect_to_server(TCP_IP, TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    return s


def send_file(file_name, socket):
    with open(file_name, 'rb') as file_to_send:
        for data in file_to_send:
            socket.sendall(data)
    socket.close()
    return


def get_file(file_name, socket):
    with open(file_name, 'wb') as file_to_write:
        while True:
            data = socket.recv(1024)
            # print data
            if not data:
                break
            # print data
            file_to_write.write(data)
    file_to_write.close()
    socket.close()
    return


if sys.argv[1] == "0" and len(sys.argv) == 5:
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_IP = sys.argv[2]
    TCP_PORT = int(sys.argv[3])
    Listen_Port = int(sys.argv[4])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    mypath = os.getcwd()
    myfiles = [f for f in sorted(listdir(mypath)) if isfile(join(mypath, f))]
    message = '1' + ' ' + str(Listen_Port) + ' '
    i = 0
    for f in myfiles:
        message += f
        if i < len(myfiles):
            message += ','
        i += 1
    s.sendall(message.encode())
    TCPClientSocket.bind(('0.0.0.0', Listen_Port))
    TCPClientSocket.listen()
    while True:
        # Establish connection with client.
        connection, client_address = TCPClientSocket.accept()
        message = connection.recv(1024)
        send_file(message.decode("utf-8"), connection)

elif sys.argv[1] == "1" and len(sys.argv) == 4:
    BUFFER_SIZE = 2048
    message = '2' + ' ' + input("Search:")
    while not message == "quit":
        TCP_IP = sys.argv[2]
        TCP_PORT = int(sys.argv[3])
        s = connect_to_server(TCP_IP, TCP_PORT)
        s.sendall(message.encode())
        data = s.recv(BUFFER_SIZE)
        if data.decode("utf-8") != "":
            split_data = data.decode("utf-8").split(',')
            i = 1
            for files in split_data:
                file = files.split()[0]
                print(str(i) + ' ' + file)
                i += 1
        choose = input("Choose:")
        try:
            int(choose)
            if int(choose) < 1 or int(choose) > len(split_data):
                message = '2' + ' ' + input("Search:")
                continue
        except:
            message = '2' + ' ' + input("Search:")
            continue
        info = split_data[int(choose) - 1].split()
        file_name = info[0]
        TCP_IP = info[1]
        TCP_PORT = int(info[2])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        sock.sendall(file_name.encode())
        get_file(file_name, sock)
        message = '2' + ' ' + input("Search:")

else:
    print("illegal request")
    sys.exit(0)
