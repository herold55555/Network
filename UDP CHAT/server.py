# first of all import the socket library
import socket
import sys

# next create a socket object
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
userList = []
socketList = []
userDict = {}
usersUpdate = {}

# save all the messages that we have to send when the client wants update
def broadcast(message, connection):
    # we save it in a dictionary
    for clients in socketList:
        if clients != connection:
            if len(usersUpdate[clients]) > 0:
                usersUpdate[clients] += "\n"
            usersUpdate[clients] += message

# send the messages in the dictionary with the right socket
def update(sock):
    # mySplit = usersUpdate[sock].split('#')
    if len(usersUpdate[sock]) > 0:
        UDPServerSocket.sendto(usersUpdate[sock].encode(), sock)
        usersUpdate[sock] = ""


def mission1(message, sock):
    if message.decode("utf-8") in userList:
        myMsg = "Illegal request"
        UDPServerSocket.sendto(myMsg, sock)
    elif userList.__len__() > 0 and sock in userDict:
        myMsg = "Illegal request"
        UDPServerSocket.sendto(myMsg, sock)
    else:
        myMsg = message.decode("utf-8") + " has joined"
        users = ""
        usersUpdate[sock] = ""
        #if there are other users
        if userList.__len__() > 0:
	    # save the messages to send
            broadcast(myMsg, sock)
	    # send the list of users to the client
            for i in range(len(userList)):
                users += userList[i]
                if i < (len(userList) - 1):
                    users += ", "
            UDPServerSocket.sendto(users.encode(), sock)
        userDict[sock] = message.decode("utf-8")
        userList.append(message.decode("utf-8"))


def mission2(message, sock):
    if sock in userDict:
        myMsg = userDict[sock] + " : " + message.decode("utf-8")
	# save in the dictionary of the other users the messages that we want to send
        if userList.__len__() > 1:
            broadcast(myMsg, sock)
	    #send to the client the message that we save to his dictonary
            update(sock)


def mission3(message, sock):
    if sock in userDict:
	#save message to tell everyone that the user change his name
        myMsg = userDict[sock] + " changed his name to " + message.decode("utf-8")
	# if there are other users
        if userList.__len__() > 1:
            broadcast(myMsg, sock)
            update(sock)
	#remove the old name and append the new to our list
        userList.remove(userDict[sock])
        userList.append(message.decode("utf-8"))
        userDict[sock] = message.decode("utf-8")


def mission4(sock):
    if sock in userDict:
        myMsg = userDict[sock] + " has left the group"
        if userList.__len__() > 1:
            broadcast(myMsg, sock)
	#remove the users from all the lists and dictonary that we have
        userList.remove(userDict[sock])
        socketList.remove(sock)
        userDict.pop(sock)


def mission5(sock):
    # we send all the messages that we have to send
    if sock in userDict:
        update(sock)

# switch function to activate the right function 
def switch_number(argument, message, sock):
    if int(argument) == 1:
        mission1(message, sock)
    elif int(argument) == 2:
        mission2(message, sock)
    elif int(argument) == 3:
        mission3(message, sock)
    elif int(argument) == 4:
        mission4(sock)
    else:
        mission5(sock)


# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = int(sys.argv[1])
server_ip = '0.0.0.0'

UDPServerSocket.bind((server_ip, port))
while True:
    # Establish connection with client.
    bytesAddressPair = UDPServerSocket.recvfrom(4096)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    #if this is a new client
    if not address in socketList:
        socketList.append(address)
    #if we received something
    if message:
	#split it with space
        splitList = message.upper().split()
        theMessage = message[2:]
        try:
            #check if it's legal request
            int(splitList[0])
            if int(splitList[0]) > 5 or int(splitList[0]) < 0:
                myMsg = "Illegal request"
                UDPServerSocket.sendto(myMsg.encode(), address)
            elif int(splitList[0]) > 1 and address not in userDict:
                myMsg = "Illegal request"
                UDPServerSocket.sendto(myMsg.encode(), address)
            switch_number(splitList[0], theMessage, address)
        except:
            myMsg = "Illegal request"
            UDPServerSocket.sendto(myMsg.encode(), address)
    else:
        continue

