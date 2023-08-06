from quarchpy.device import *
from quarchpy.user_interface import user_interface

import time
import os
import subprocess

myDevice = quarchDevice("USB::QTL1743-03-392")
print(myDevice.sendCommand("source:4:bounce:length 10 mS").strip())
def hello():
    while True:
        procse = subprocess.Popen(["wmic","diskdrive","list","full"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = procse.communicate()
        my_times = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
        for item in my_times:
            response = myDevice.sendCommand("source:4:bounce:length " + item +  " mS").strip()
            if response != "OK":
                print("response was : " + response)
                if response == "":
                    print("Response was empty?")
                else:
                    print("Response was not empty")

        setup_simple_hotplug(25, 6)


def setup_simple_hotplug(delay_time, step_count):

    # Run through all 6 timed sources on the module
    for steps in range(1, 6):
        # Calculate the next source delay. Additional sources are set to the last value used
        if steps <= step_count:
            next_delay = (steps - 1) * delay_time
            response = myDevice.sendCommand("source:" + str(steps) + ":delay " + str(next_delay)).strip()
            if response != "OK":
                print("response was : " + response)
                if response == "":
                    print("Response was empty?")
                else:
                    print("Response was not empty")



hello()