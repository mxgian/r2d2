#!/usr/bin/python

import pygatt
import time
import logging
import sys
import getopt
import ctypes

from pygatt.backends import BLEBackend, Characteristic, BLEAddressType

command = None
r2_address = 'C1:F0:DE:DC:2F:95'
q5_address = 'DB:01:0F:08:8D:B2'
bb8_address = 'EB:3B:5C:E6:43:46'

address = 'C1:F0:DE:DC:2F:95'
sendbytes = None
debuglogging = False
sleeponexit = True
sequences = []

commandmap = dict([
        ("laugh", [0x0A,0x18,0x00,0x1F,0x00,0x32,0x00,0x00,0x00,0x00,0x00]),
        ("yes", [0x0A,0x17,0x05,0x41,0x00,0x0F]),
        ("no", [0x0A,0x17,0x05,0x3F,0x00,0x10]),
        ("alarm", [0x0A,0x17,0x05,0x17,0x00,0x07]),
        ("angry", [0x0A,0x17,0x05,0x18,0x00,0x08]),
        ("annoyed", [0x0A,0x17,0x05,0x19,0x00,0x09]),
        ("ionblast", [0x0A,0x17,0x05,0x1A,0x00,0x0E]),
        ("sad", [0x0A,0x17,0x05,0x1C,0x00,0x11]),
        ("scared", [0x0A,0x17,0x05,0x1D,0x00,0x13]),
        ("chatty", [0x0A,0x17,0x05,0x17,0x00,0x0A]),
        ("confident", [0x0A,0x17,0x05,0x18,0x00,0x12]),
        ("excited", [0x0A,0x17,0x05,0x19,0x00,0x0C]),
        ("happy", [0x0A,0x17,0x05,0x1A,0x00,0x0D]),
        ("laugh", [0x0A,0x17,0x05,0x1B,0x00,0x0F]),
        ("surprise", [0x0A,0x17,0x05,0x1C,0x00,0x18]),
        ("tripod", [0x0A,0x17,0x0D,0x1D,0x01]),
        ("bipod", [0x0A,0x17,0x0D,0x1C,0x02])
        ])

# The CRC is 256 modulus sum of all the bytes, bitwise inverted
def GenCrc(bytes):
        ret = 0;
        for b in bytes:
                ret += b
                ret = ret % 256

        return ~ret % 256

def BuildPacket(bytes):
        # 0x8D marks the start of a packet
        ret = [0x8D]
        for b in bytes:
                ret.append(b)

        # CRC is always the 2nd to last byte
        ret.append(GenCrc(bytes))

        # 0xD8 marks the end of a packet
        ret.append(0xD8)
        return ret

try:
        opts, args = getopt.getopt(sys.argv[1:], "a:c:dn", ["address=", "command=", "debug", "nosleep"])
except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

for o, a in opts:
        if o in ("-a", "--address"):
                address = a
        elif o in ("-c", "--command"):
                command = a
                if command == "list":
                        for cmdopt in commandmap:
                                print cmdopt
                        sys.exit(0)
                sequences.append(commandmap[a])
        elif o in ("-d", "--debug"):
                debuglogging = True
        elif o in ("-n", "--nosleep"):
                sleeponexit = False
        else:
                assert False, "unhandled option"


if command == None:
        print "A command must be specified.  Use -c list to get a list of commands"
        sys.exit(1)

logging.basicConfig()
if debuglogging == True:
        logging.getLogger('pygatt').setLevel(logging.DEBUG)

adapter = pygatt.GATTToolBackend()

print("init up droid")
adapter.start()
device = adapter.connect(address=address, address_type=BLEAddressType.random)

print("connect up droid")
# 'usetheforce...band' tells the droid we're a controller, I guess.  Prevents disconnection.
device.char_write_handle(0x15, [0x75,0x73,0x65,0x74,0x68,0x65,0x66,0x6F,0x72,0x63,0x65,0x2E,0x2E,0x2E,0x62,0x61,0x6E,0x64], True)

print("wake up droid")
# wake from sleep?  Droid is responsive and front led flashes blue/red
device.char_write_handle(0x1c, [0x8D,0x0A,0x13,0x0D,0x00,0xD5,0xD8], True)

# Turn on holoprojector led, 0xff (max) intensity
device.char_write_handle(0x1c, [0x8D,0x0A,0x1A,0x0E,0x1C,0x00,0x80,0xFF,0x32,0xD8], True)

print("waiting 5 secs before sending command")
time.sleep(5)

for seq in sequences:
        #device.char_write_handle(0x1c, commandmap[command], True)
        device.char_write_handle(0x1c, BuildPacket(seq), True)
        time.sleep(2)

# rotate top to -90 degrees
#device.char_write_handle(0x1c, [0x8D,0x0A,0x17,0x0F,0x1C,0x42,0xB4,0x00,0x00,0xBD,0xD8], True)
#time.sleep(5)

# rotate top to 0 degrees
#device.char_write_handle(0x1c, [0x8D,0x0A,0x17,0x0F,0x1E,0x00,0x00,0x00,0x00,0xB1,0xD8], True)
#time.sleep(5)

if sleeponexit:
        # put the droid to sleep
        device.char_write_handle(0x1c, [0x8D,0x0A,0x13,0x01,0x17,0xCA,0xD8], True)
adapter.stop()