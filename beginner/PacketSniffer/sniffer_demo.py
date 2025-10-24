import socket
import struct
import textwrap

from sympy import ff 

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '

def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) # create a raw socket to capture all packets, sock_raw requires admin privileges, af_packet is used to capture link layer packets
    while True:
       raw_data, _ = conn.recvfrom(65536) # receive packets
       dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data) # unpack ethernet frame
       print('\nEthernet Frame:')
       print(TAB_1 + 'Destination: {}, Source: {}, Protocol: {}'.format(dest_mac, src_mac, eth_proto))
       print(DATA_TAB_1 + 'Destination MAC:', dest_mac)
       print(DATA_TAB_1 + 'Source MAC:', src_mac)
       print(DATA_TAB_1 + 'Ethernet Protocol:', eth_proto)
       print(DATA_TAB_1 + 'Data:', data)
       # if eth_proto == 8: # IPv4
       #     version, header_length, ttl, proto, src, target, data = ipv4_packet(data)
       if eth_proto == 8: # IPv4
           (version, header_length, ttl, proto, src, target, data) = ipv4_packet(data)
           print('\t- IPv4 Packet:')
           print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {}'.format(version, header_length, ttl))
           print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(proto, src, target))
           if proto == 1: # ICMP
               (icmp_type, code, checksum, data) = icmp_packet(data)
               print(TAB_3 + 'Type: {}, Code: {}, Checksum: {}'.format(icmp_type, code, checksum))
           elif proto == 6: # TCP
               (src_port, dest_port, sequence, acknowledgment, offset, data, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin) = tcp_segment(data)
               print(TAB_3 + 'Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
               print(TAB_3 + 'Sequence: {}, Acknowledgment: {}'.format(sequence, acknowledgment))
               print(TAB_3 + 'Offset: {}, Flags: URG={}, ACK={}, PSH={}, RST={}, SYN={}, FIN={}'.format(offset, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
           elif proto == 17: # UDP
               (src_port, dest_port, size, data) = udp_segment(data)
               print(TAB_3 + 'Source Port: {}, Destination Port: {}, Size: {}'.format(src_port, dest_port, size))
               print(DATA_TAB_2 + 'Data:')
               print(format_multi_line(DATA_TAB_3, data))
           else:#other
                print(DATA_TAB_2 + 'Data:')
                print(format_multi_line(DATA_TAB_3, data))

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
    # Fix: convert each byte to integer before joining
    # return '.'.join(str(b) for b in addr)
    # Alternatively, using struct.unpack:
    # return '.'.join(map(str, struct.unpack('!BBBB', addr)))
    return '.'.join(str(b) for b in addr)

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

# Unpack UDP segment
def udp_segment(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8]) # unpack udp header
    return src_port, dest_port, size, data[8:]

# Format multi-line data
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
    if len(string) <= size:
        return prefix + string
    lines = []
    for i in range(0, len(string), size):
        lines.append(prefix + string[i:i+size])
    return '\n'.join(lines)
























