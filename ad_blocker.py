from scapy.all import *
from scapy.layers.dns import DNSRR, DNS, UDP, DNSQR, IP
import socket
import datetime

blocked_domains = set()

file = open("/elocal/Anunturi.txt",'r')
rez = open("/elocal/rezultat.txt", 'a')

for line in file:
    ip = line.strip()
    blocked_domains.add(ip)

simple_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
simple_udp.bind(('172.9.0.1', 53))

print("Lista de domain-uri incarcata")

while True:
    request, adresa_sursa = simple_udp.recvfrom(65535)
    # converitm payload-ul in pachet scapy
    packet = DNS(request)
    dns = packet.getlayer(DNS)
    if dns is not None and dns.opcode == 0: # dns QUERY
        print ("got: ")
        print (packet.summary())
        name = str(dns.qd.qname)[2:-2]
        if name in blocked_domains:
            dns_answer = DNSRR(      # DNS Reply
            rrname=dns.qd.qname, # for question
            ttl=330,             # DNS entry Time to Live
            type="A",            
            rclass="IN",
            rdata='0.0.0.0')

            rez.write(f"{datetime.datetime.now()} {dns.qd.qname}\n")
            rez.flush()
        else:
            dns_request = IP(dst="8.8.8.8")/UDP(sport=RandShort(),dport=53)/DNS(rd=1,qd=DNSQR(qname= name,qtype="A"))
            ans = sr1(dns_request, timeout = 3)
            try:
                ip = ans.an[ans.ancount-1].rdata
            except:
                ip = '0.0.0.0'
            print(ip)
            dns_answer = DNSRR(      # DNS Reply
            rrname=dns.qd.qname, # for question
            ttl=330,             # DNS entry Time to Live
            type="A",            
            rclass="IN",
            rdata= ip) 
        dns_response = DNS(
                          id = packet[DNS].id, # DNS replies must have the same ID as requests
                          qr = 1,              # 1 for response, 0 for query 
                          aa = 0,              # Authoritative Answer
                          rcode = 0,           # 0, nicio eroare http://www.networksorcery.com/enp/protocol/dns.htm#Rcode,%20Return%20code
                          qd = packet.qd,      # request-ul original
                          an = dns_answer)     # obiectul de reply
        print('response:')
        print (dns_response.summary())
        simple_udp.sendto(bytes(dns_response), adresa_sursa)
    rez.flush()

simple_udp.close()