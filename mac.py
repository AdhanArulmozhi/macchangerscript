import optparse
import re
import subprocess
import scapy.all as scapy
import netifaces

interfaces = netifaces.interfaces()


# To parse the arguments to user via CLI and get the values according to the args.

def get_arg_and_values():
    value = optparse.OptionParser()
    value.add_option("-i", "--interface", dest="interface", help="To choose your network interface")
    value.add_option("-m", "--newmac", dest="newmac", help="To change your MAC address")
    value.add_option("-p", "--resetinterface", dest="resetinterface", help="To reset your MAC address")
    value.add_option("-r", "--randommac", dest="randommac", help="To randomize MAC selection")
    value.add_option("-a", "--ip", dest="ip", help="To send ARP request to the target IP and get the corresponding MAC")
    value.add_option("-V", "--version", dest="version", help="To produce the list of vendors and its version")
    value.add_option("-n", "--nmap", dest="nmapscan", help="To scan and find the list of hosts up and their IP address")
    (values, arguments) = value.parse_args()
    if values.interface and values.newmac:
        if values.interface in interfaces:
            print(f"{values.interface} is a valid network interface")
            change_mac(values.interface, values.newmac)
            just_mac = get_current_mac(values.interface)
            print("current MAC = " + just_mac)
        else:
            print(f"{values.interface} is not a valid network interface. The available network interfaces are:")
            print("\n".join(interfaces))
    if values.randommac:
        if values.randommac in interfaces:
            print(f"{values.randommac} is a valid network interface")
            to_change_random_mac(values.randommac)
        else:
            print(f"{values.interface} is not a valid network interface. The available network interfaces are:")
            print("\n".join(interfaces))
    if values.resetinterface:
        if values.resetinterface in interfaces:
            print(f"{values.resetinterface} is a valid network interface")
            to_reset_mac(values.resetinterface)
        else:
            print(f"{values.interface} is not a valid network interface. The available network interfaces are:")
            print("\n".join(interfaces))
    if values.ip:
        scan(values.ip)
    if values.version:
        to_print_the_version(values.version)
    if values.nmapscan:
        nmap_scan(values.nmapscan)
    return values


# To process the user request with given args and options.

def change_mac(interface, newmac):
    print("Changing the mac address for interface " + interface + " into new mac " + newmac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newmac])
    subprocess.call(["ifconfig", interface, "up"])


# To check the output of the process by printing just the MAC address by regex.

def get_current_mac(interface):
    justmac = subprocess.check_output(["ifconfig", interface])
    print_just_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", justmac.decode('utf-8'))
    if print_just_mac:
        return print_just_mac.group(0)
    else:
        print("Couldn't find mac address.")


# To change the MAC address randomly.

def to_change_random_mac(randommac):
    subprocess.call(["ifconfig", randommac, "down"])
    subprocess.call(["macchanger", randommac, "-r"])
    subprocess.call(["ifconfig", randommac, "up"])


# To Reset the MAC address into its original one.

def to_reset_mac(resetinterface):
    subprocess.call(["ifconfig", resetinterface, "down"])
    subprocess.call(["macchanger", resetinterface, "-p"])
    subprocess.call(["ifconfig", resetinterface, "up"])


# To send arp request to the target ip address.

def scan(ip):
    scapy.arping(ip)


# To check the version of the every official network vendors.

def to_print_the_version(version):
    subprocess.call(["macchanger", version])


# To scan the hosts connected to the same network and get their IP address.

def nmap_scan(nmapscan):
    subprocess.call(["nmap", nmapscan])


# initialization of the program or the functions.

get_arg_and_values()
