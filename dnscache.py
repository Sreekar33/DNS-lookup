import socket
import sys,os
import bitstring, struct
'''
if os.path.exists(str(os.getcwd())+'/dnstemp.txt'):
	f=open('dnstemp.txt','r')
else :
	f=open('dnstemp.txt','w+') 
for line in f :
	line=line.split(':')
	if(line[0]==str(sys.argv[1])):
		print "Name : " + line[0]
		print "IP address : "+line[1]
		print "got ip from cache"
		sys.exit(0)
'''
addr=('127.0.0.1',53) 
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(sys.argv[1],addr)
data,addr=s.recvfrom(1024)
if data != 'error' :
	print 'Name : ' + sys.argv[1] 
	print 'IP address : ' + data
	print 'got from local server'
	sys.exit(0)
	
else :
	pass



DNS_QUERY_FORMAT = [ 'hex=id', 'bin=flags', 'uintbe:16=qdcount', 'uintbe:16=ancount', 'uintbe:16=nscount', 'uintbe:16=arcount' ] 	
DNS_QUERY = { 'id' : '0x1a2b', 'flags' : '0b0000000100000000' , 'qdcount' : 1, 'ancount' : 0, 'nscount' : 0, 'arcount' : 0}

domain=sys.argv[1]

domain=domain.split('.')
question=[]
j=0;
for i in range (0,len(domain)):
	domain[i]=domain[i].strip()
	size=hex(len(domain[i]))
	if len(size)==3 :
		size='0x0'+size[2:]
	question.append(size)
	DNS_QUERY_FORMAT.append('hex='+'qname' + str( j ) );
	DNS_QUERY['qname'+ str( j ) ] = question[ -1 ];
	j += 1;
	question.append( '0x' + domain[ i ].encode( 'hex' ) );
	DNS_QUERY_FORMAT.append( 'hex=' + 'qname' + str( j ) );
	DNS_QUERY[ 'qname' + str( j ) ] = question[ -1 ];
	j += 1;
	
DNS_QUERY_FORMAT.append('hex=qname'+ str( j ) );
DNS_QUERY['qname' + str( j )] = '0x00';
DNS_QUERY_FORMAT.append( 'uintbe:16=qtype' );
DNS_QUERY[ 'qtype' ] = 1;
DNS_QUERY_FORMAT.append( 'hex=qclass' );
DNS_QUERY[ 'qclass' ] = '0x0001';
data = bitstring.pack( ','.join( DNS_QUERY_FORMAT ), **DNS_QUERY );

IP='8.8.8.8'
port = 53

s.sendto(data.tobytes(),(IP,port))
data,addr=s.recvfrom(1024)
data = bitstring.BitArray( bytes = data )

response = str( data[ 28 : 32 ].hex );
record_count = str( data[ 48 : 64 ].uintbe );
f=open('dnstemp.txt','a')
print "Name = "+ str(sys.argv[1])
if ( response == "0" ):	
	print "IP address: " + str( data[ -32 : -24 ].uintbe ) + "." + str( data[ -24 : -16 ].uintbe ) + "." + str( data[ -16 : -8 ].uintbe ) + "." + str( data[ -8 : ].uintbe )
	'''
	f.write(str(sys.argv[1])+str(':'))
	f.write(str( data[ -32 : -24 ].uintbe ) + "." + str( data[ -24 : -16 ].uintbe ) + "." + str( data[ -16 : -8 ].uintbe ) + "." + str( data[ -8 : ].uintbe )+ '\n')
	f.close()'''
	laddr=('127.0.0.1',53)
	s.sendto("add",laddr)
	s.sendto(str(sys.argv[1])+'|'+str( data[ -32 : -24 ].uintbe ) + "." + str( data[ -24 : -16 ].uintbe ) + "." + str( data[ -16 : -8 ].uintbe ) + "." + str( data[ -8 : ].uintbe ),laddr)
elif (response == "1" ) :
	print "Format error"
	
elif ( response == "2" ):
	print "Server failure"
	
elif ( response == "3" ):
	print "Domain name does not exist"
	
elif ( response == "4" ):
	print "Query request type not supported"
	
elif ( response == "5" ):
	print "Server refused query"
