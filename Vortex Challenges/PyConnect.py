import socket
import sys
import struct

#intiate our variables for NULL string and unassigned integer
response = ''
int_sum = 0

#create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding target server and port to socket
server_address = ('vortex.labs.overthewire.org', 5842)
sock.connect(server_address)

#receive 4 bytes from server
for x in range(4):
	response = response + sock.recv(4) 
	
#unpack bytes response
unpacked_int = struct.unpack('iiii', response)

#convert bytes to integers
for x in range(4):
	int_sum = int_sum + unpacked_int[x]
	
#send integers back to  server and receive a password
sock.sendall(struct.pack('<Q', int_sum))

#Stored received password from server
response_password = sock.recv(4096)

print(response_password)