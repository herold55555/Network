# first of all import the socket library
import socket
import sys

# next create a socket object
TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dict_iport_files = dict()
list_of_iports = list()


def mission1(the_message, ip):
    msg = the_message.decode("utf-8")
    my_split = msg.split()
    my_iport = ip + ',' + my_split[0]
    if my_iport not in list_of_iports:
        list_of_iports.append(my_iport)
    if my_iport not in dict_iport_files:
        dict_iport_files[my_iport] = ""
    files = my_split[1].split(',')
    for file in files:
        dict_iport_files[my_iport] += file
        dict_iport_files[my_iport] += ' '


def mission2(the_message, sock):
    msg = the_message.decode("utf-8")
    messages_to_send = list()
    mess = ""
    i = 0
    for my_iport in list_of_iports:
        files = dict_iport_files[my_iport]
        ip = my_iport.split(',')[0]
        port = my_iport.split(',')[1]
        list_of_files = files.split()
        for file in list_of_files:
            if msg in file:
                information = file + ' ' + ip + ' ' + port
                messages_to_send.append(information)
    if len(messages_to_send) == 0:
        mess = ""
    else:
        for mes in messages_to_send:
            mess += mes
            if i < len(messages_to_send) - 1:
                mess += ','
            else:
                mess += '\n'
            i += 1
    sock.sendall(mess.encode())


# switch function to activate the right function
def switch_number(argument, the_message, sock, ip):
    if int(argument) == 1:
        mission1(the_message, ip)
    elif int(argument) == 2:
        mission2(the_message, sock)


port = int(sys.argv[1])
server_ip = '0.0.0.0'
TCPServerSocket.bind((server_ip, port))
TCPServerSocket.listen(1)

while True:
    # Establish connection with client.
    connection, client_address = TCPServerSocket.accept()
    message = connection.recv(4096)
    if message:
        # split it with space
        splitList = message.upper().split()
        theMessage = message[2:]
        ip = client_address[0]

        try:
            # check if it's legal request
            int(splitList[0])
            if int(splitList[0]) > 2 or int(splitList[0]) < 0:
                continue
            switch_number(splitList[0], theMessage, connection, ip)
        except:
            myMsg = "Illegal request"
            connection.sendall(myMsg.encode())
        finally:
            connection.close()
    else:
        connection.close()
        continue
