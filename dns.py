import socket
import sys
import bitstring, struct

ip='127.0.0.1'

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
'''
def getflags(flags):
	byte1 = bytes(flags[:1])
	byte2 = bytes(flags[1:2])
	rflags = ''
	QR = '1'
	for bit in range(1,5):
		OPCODE += str(ord(byte1)&(1<<bit))
		
	AA = '1'
	
	TC = '0'
	
	RD = '0'
	
	RA = '0'
	
	Z ='000'
	
	RCODE = '0000'
	
	return int(QR+OPCODE+AA+TC+RD,2).to_bytes(1,byteorder='big')+int(RA+Z+RCODE,2).to_bytes(1,byteorder='big')
	
def buildresponse(data):
	TransactionID = data[:2]
	TID =''
	for byte in TransactionID:
		TID +=hex(byte)[2:]
		
	Flags = getflags(data[2:4])
	
	QDCOUNT = b'\x00\x01'
'''
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
print "Name = "+ str(sys.argv[1])
if ( response == "0" ):	
	print "IP address: " + str( data[ -32 : -24 ].uintbe ) + "." + str( data[ -24 : -16 ].uintbe ) + "." + str( data[ -16 : -8 ].uintbe ) + "." + str( data[ -8 : ].uintbe ) ;
elif ( response == "1" ):
	print "Format error";
	
elif ( response == "2" ):
	print "Server failure";
	
elif ( response == "3" ):
	print "Domain name does not exist.";
	
elif ( response == "4" ):
	print "Query request type not supported.";
	
elif ( response == "5" ):
	print "Server refused query.\n";



