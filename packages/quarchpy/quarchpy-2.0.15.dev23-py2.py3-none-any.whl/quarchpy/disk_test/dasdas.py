from quarchpy import *

mydev = quarchDevice("usb::QTL1743-03-392")

while True:
    print("Delay " + mydev.sendCommand("source:4:delay 50 mS"))
    print("length " + mydev.sendCommand("source:4:bounce:length 10 mS"))
    print("Period " + mydev.sendCommand("source:4:bounce:period 500 uS"))
    print("Duty " + mydev.sendCommand("source:4:bounce:duty 50"))
    print("power up " + mydev.sendCommand("run pow up"))
    print("power down " + mydev.sendCommand("run pow down"))
