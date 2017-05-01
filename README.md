# DNS-lookup

Implementation of the DNS client
DNS client sends a UDP message to the DNS server it sends in the form of questions which
can also be done with tcp but to reduce the overhead while sending large data it prefers UDP socket.
The message contains the header that contain information abot the flags and type of query it asks
and number of questions it is sending and the server returns the packet changing the opcode as
response and fill the answer section in the UDP packet, by parsing the UDP packet sent from the
server we get the DNS address.
In case of cache the DNS client first checks fot the domain name in the local system if it
finds the answer for the query then it returns it or else it performs the same operation as explained
above.
Studies performed : The query the is send is encoded in different ways the falgs in binary format the
question i.e domain in hex format and ip in binary format
usage : python dns.py domain_name
usage : python dnscache.py domain_name
