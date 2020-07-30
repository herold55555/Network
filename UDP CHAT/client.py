import socket
import sys
import select

dest_ip = sys.argv[1]
dest_port = int(sys.argv[2])
serverAddressPort = (dest_ip, dest_port)
bufferSize = 2048
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
message = input()
# Send to server using created UDP socket
while not message == 'quit':
     UDPClientSocket.sendto(message.encode(), serverAddressPort)
     ready = select.select([UDPClientSocket], [], [], 1)
     if ready[0]:
          msgFromServer = UDPClientSocket.recvfrom(bufferSize)
          msg = msgFromServer[0].decode("utf-8")
          print(msg)
     message = input()