from bluetooth import *
import sys

if sys.version < '3':
    input = raw_input

addr = None


print("Searching all nearby bluetooth devices for the SL4a service")


# search for the SL4A service
uuid = '457807c0-4897-11df-9879-0800200c9a66'
service_matches = find_service( uuid = uuid)

if len(service_matches) == 0:
    print("couldn't find the SL4A service")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock = BluetoothSocket( RFCOMM )
sock.connect((host, port))

print("connected.")
try:
    while True:
        # data = sock.recv(1024)
        # if len(data) == 0: break
        # print("received %s" % data)
        # print('--------------------')
        print('Enter data: ', end="")
        data = input()
        sock.send("Data: %s" % data)
        print('Sent message')
except IOError:
    pass

print("disconnected")

sock.close()
print("all done")