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

#unpack IPv4 packet
def ipv4_packet(data):
    version_header_length = data[0]
    version= version_header_length >> 4 # bitwise operation to extract version
    header_length = (version_header_length & 15) * 4 # bitwise operation to extract header length
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20]) # unpack ipv4 header
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]

# Returns properly formatted IPv4 address
def ipv4(addr):
    print(addr)
    return '.'.join(map(str, addr)) # convert bytes to decimal format and join with '.'

# Unpack ICMP(Internet Control Message Protocol) packet
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4]) # unpack icmp header
    return icmp_type, code, checksum, data[4:]

#unpack TCP segment
def tcp_segment(data):
    (src_port, dest_port, sequence, acknowledgment, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14]) # unpack tcp header
    offset = (offset_reserved_flags >> 12) * 4 # bitwise operation to extract offset
    flag_urg = (offset_reserved_flags & 32) >> 5 # bitwise operation to extract flags
    flag_ack = (offset_reserved_flags & 16) >> 4 # bitwise operation to extract flags
    flag_psh = (offset_reserved_flags & 8) >> 3 # bitwise operation to extract flags
    flag_rst = (offset_reserved_flags & 4) >> 2 # bitwise operation to extract flags
    flag_syn = (offset_reserved_flags & 2) >> 1 # bitwise operation to extract flags
    flag_fin = (offset_reserved_flags & 1) # bitwise operation to extract flags
    return src_port, dest_port, sequence, acknowledgment, offset, data[offset:], flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin
























