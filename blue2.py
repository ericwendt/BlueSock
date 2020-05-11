import bluetooth
import time
from colorama import init
from colorama import Fore
import sys
import threading
import os


init()

# for windows
if os.name == 'nt':
    _ = os.system('cls')

# for mac and linux(here, os.name is 'posix')
else:
    _ = os.system('clear')

print("looking for nearby devices...")
nearby_devices = bluetooth.discover_devices(lookup_names = True,
flush_cache = True, duration = 1)

print("\nfound", len(nearby_devices), "devices\n")

devices = []

for mac, name in nearby_devices:
    print(Fore.GREEN, len(devices), end=' ')
    print(Fore.RED, end='')
    print (str(mac), name)



    device = {'mac': str(mac), 'name': name}
    devices.append(device)


    # services = bluetooth.find_service(address = mac)
    # for service in services:
    #     print(Fore.GREEN, 'name:', Fore.YELLOW, service['name'], Fore.GREEN, 'protocol:', Fore.YELLOW,
    #      service['protocol'], Fore.GREEN, 'provider:', Fore.YELLOW,
    #      service['provider'], Fore.GREEN, 'port:',  Fore.YELLOW, service['port'],
    #       Fore.GREEN, 'profiles:',  Fore.YELLOW, service['profiles'],
    #       Fore.GREEN, 'service-classes:',  Fore.YELLOW, service['service-classes'])




print(Fore.YELLOW)
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

while True:

    inp = input(Fore.GREEN + 'Enter command (help) \n')
    if inp.split(' ')[0] == 'con':


        mac = ''
        device = ''
        protocol = ''
        port = ''

        # user specified device
        if len(inp.split(' ')) > 1:
            mac_index = int(inp.split(' ')[1])

            if mac_index >= len(devices):
                print('Invalid mac index')
                continue

            device = devices[mac_index]

        else:
            mac_index = int(input('select mac\n'))

            if mac_index >= len(devices):
                print('Invalid mac index')
                continue

            device = devices[mac_index]


        device['ports'] = []
        device['profiles'] = []
        device['service-classes'] = []

        mac = device['mac']
        services = bluetooth.find_service(address = mac)

        # user specified port
        if len(inp.split(' ')) > 2:
            port = int(inp.split(' ')[2])

        else:
            port = int(input('select port\n'))

        # print('mac', mac, 'port', port)
        try:
            sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            sock.connect((mac, port))


            print(Fore.BLUE, '\nconnected to device, enter command', Fore.RED)
            while True:
                # sock.send('pwd')

                # print(sock.recv(1024).decode('utf-8'), '$', end='')
                inp2 = input('')

                if inp2 == 'quit':
                    break

                sock.send(inp2)
                data = sock.recv(6000)

                print(Fore.YELLOW, data.decode('utf-8'), Fore.RED)


            print(Fore.RED, '\nshell exited')

        except:
            print(Fore.RED, 'connection failed')
    elif inp.split(' ')[0] == 'info':

        mac = ''
        device = ''
        protocol = ''
        port = ''

        # user specified device
        if len(inp.split(' ')) > 1:
            mac_index = int(inp.split(' ')[1])

            if mac_index >= len(devices):
                print('Invalid mac index')
                continue

            device = devices[mac_index]

        else:
            mac_index = int(input('select mac\n'))

            if mac_index >= len(devices):
                print('Invalid mac index')
                continue

            device = devices[mac_index]


        device['ports'] = []
        device['profiles'] = []
        device['service-classes'] = []

        print(Fore.RED, 'listing services:')
        mac = device['mac']
        services = bluetooth.find_service(address = mac)

        count = 0
        for service in services:
            count += 1

            if count == 1:
                continue

            print(Fore.GREEN, 'name:', Fore.YELLOW, service['name'].decode('utf-8'), Fore.GREEN, '\tprotocol:', Fore.YELLOW,
             service['protocol'], Fore.GREEN, '\tprovider:', Fore.YELLOW,
             service['provider'], Fore.GREEN, '\tport:',  Fore.YELLOW, service['port'])


            device['protocol'] = service['protocol']
            device['ports'].append(service['port'])
            device['provider'] = service['provider']
            device['profiles'].append(service['profiles'])
            device['service-classes'].append(service['service-classes'])

    elif inp == 'quit':
        sock.close()
        sys.exit()

    elif inp.split(' ')[0] == 'list':
        print()

        nearby_devices = bluetooth.discover_devices(lookup_names = True,
        flush_cache = True, duration = 1)

        devices = []

        for mac, name in nearby_devices:
            print(Fore.GREEN, len(devices), end=' ')
            print(Fore.RED, end='')
            print (str(mac), name)



            device = {'mac': str(mac), 'name': name}
            devices.append(device)



    elif inp == 'help':
        print(Fore.YELLOW, '\nhelp - lists commands')
        print('quit - quits CLI')
        print('con {mac index} {port} - connec to a device')
        print('info {mac index} - lists information about device')
        print('list - finds/updates bluetooth devices')

        print()






#
