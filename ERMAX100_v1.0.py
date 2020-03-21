import argparse
import serial,os

parser = argparse.ArgumentParser(usage='ERMAX100.py <EPROM> <file> <port>', description='This script sends data to ERMAX100 EPROM Emulator over serial port, requires python 3.8 and pyserial "pip install pyserial"')

parser.add_argument('eprom_arg', metavar='EPROM', type=str, nargs=1, help='Specify EPROM Type: 2716..27512')
parser.add_argument('file_arg', metavar='file', type=str, nargs=1, help='Binary data file')
parser.add_argument('port_arg', metavar='port', type=str, nargs=1, help='Serial port to use, eg COM1 in Windows or "/dev/ttyUSB0" in Linux')

# ver 1.0 kris@mygeekyhobby.com

args = parser.parse_args()

try:
	binary_data = open(args.file_arg[0], 'rb').read()
except:
	print("Failed to open the file")
	exit()

if args.eprom_arg[0] == "2716":
	mem_type = b'\x01'
	if len(binary_data) > 2048:
		print("File size is {} is large for this type of memory".format(len(binary_data))) 
		exit()
elif args.eprom_arg[0] == "2732":
	mem_type = b'\x02'
	if len(binary_data) > 4096:
		print("File size is {} is large for this type of memory".format(len(binary_data)))
		exit()
elif args.eprom_arg[0] == "2764":
	mem_type = b'\x03'
	if len(binary_data) > 8192:
		print("File size is {} is large for this type of memory".format(len(binary_data)))
		exit()
elif args.eprom_arg[0] == "27128":
	mem_type = b'\x04'
	if len(binary_data) > 16384:
		print("File size is {} is large for this type of memory".format(len(binary_data)))
		exit()
elif args.eprom_arg[0] == "27256":
	mem_type = b'\x05'
	if len(binary_data) > 32768:
		print("File size is {} is large for this type of memory".format(len(binary_data)))
		exit()
elif args.eprom_arg[0] == "27512":
	mem_type = b'\x06'
	if len(binary_data) > 65536:
		print("File size is {} is large for this type of memory".format(len(binary_data)))
		exit()
else:
	print("Unsupported memory type: {}".format(args.eprom_arg[0]))
	exit()

try:
        ser = serial.Serial(args.port_arg[0],57600)
except:
        print("Failed to open port, verify port name")
        exit()

print("Sending: {} bytes over serial port {}, emulating: {} EPROM".format(str(len(binary_data)),args.port_arg[0],args.eprom_arg[0]))

sync_byte = b'\x55'
is_one = b'\x01' 

out_data = sync_byte + mem_type + is_one + binary_data

try:
	ser.write(out_data)
	print("Sent: OK!")
except:
	Print("Failed to send")
	
ser.close()
exit()
