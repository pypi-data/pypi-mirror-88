#
# from quarchpy.disk_test.driveTestCore import is_tool
#
# print (is_tool("fio"))

# Import QPS functions
from quarchpy import qpsInterface, isQpsRunning, startLocalQps, GetQpsModuleSelection, quarchDevice, quarchQPS, requiredQuarchpyVersion
# OS allows us access to path data
import os, time

# Connect to the localhost QPS instance - you can also specify host='127.0.0.1' and port=*************************************??????? for remote control.
# This is used to access the basic functions, allowing us to scan for devices.  This step can be skipped if you already know the ID
# string of the device you want to connect to
myQps = qpsInterface()

# convert module to quarch module
myQuarchDevice = quarchDevice("USB:QTL1999-06-001", ConType="QPS")
# Create the device connection, as a QPS connected device
myQpsDevice = quarchQPS(myQuarchDevice)
myQpsDevice.openConnection()

print(myQpsDevice.sendCommand("record:averaging 32k"))
print(myQpsDevice.sendCommand("version"))

# # Start a stream, using the local folder of the script and a time-stamp file name in this example
# filePath = os.path.dirname(os.path.realpath(__file__))
# fileName = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
# myStream = myQpsDevice.startStream(filePath + fileName)
# print(myQpsDevice.sendCommand("run power down"))
# time.sleep(1)
# for x in range(1):
#     time.sleep(0.5)
#     myStream.addAnnotation("hi" + str(x))
#
# print(myQpsDevice.sendCommand("run power up"))
#
# time.sleep(2)
#
# for x in range(1):
#     time.sleep(0.5)
#     myStream.addAnnotation("hi." + str(x))
#
# time.sleep(5)
#
# print(myStream.get_stats())
#
# myStream.addAnnotation("new 1 - Waiting 1 second after this to get stats")
#
# time.sleep(1)
#
# print(myStream.get_stats())
#
#
# myStream.stopStream()

