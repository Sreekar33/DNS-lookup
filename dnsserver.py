import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind(('127.0.0.1',53))

dic = {}
while True:
	data,addr=s.recvfrom(1024)
	if(data=="add"):
		data,addr=s.recvfrom(1024)
		data=data.split('|')
		dic[data[0]]=data[1];
	else:
		try:
			con=dic[data]
			s.sendto(con,addr)
		except KeyError:
			s.sendto("error",addr)
			
