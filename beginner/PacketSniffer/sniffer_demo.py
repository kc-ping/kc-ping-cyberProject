import socket
import struct
import textwrap 

def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) # create a raw socket to capture all packets, sock_raw requires admin privileges, af_packet is used to capture link layer packets
    while True:
       raw_data, addr= conn.recvfrom(65536) # receive packetss
       dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data) # unpack ethernet frame
       print('\nEthernet Frame:')
       
       print('Destination MAC:', dest_mac)
       print('Source MAC:', src_mac)
       print('Ethernet Protocol:', eth_proto)
       print('Data:', data)

# Unpack Ethernet frame
def ethernet_frame(data):
    dest_mac,src_mac, proto = struct.unpack('! 6s 6s H', data[:14]) # converting mac header to readable format for humans
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:] #htons make data human readable

# return properly formatted MAC address (AA:BB:CC:DD:EE:FF)
def get_mac_addr(bytes_addr):
    bytes_str= map('{:02x}'.format, bytes_addr) # convert bytes to hex format and join with ':'
    print(bytes_str)
    return ':'.join(bytes_str).upper()


























