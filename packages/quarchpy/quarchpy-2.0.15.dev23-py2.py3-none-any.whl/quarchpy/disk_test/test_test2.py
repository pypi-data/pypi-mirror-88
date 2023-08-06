import inspect
from abc import ABC

import time
import sys
import os
import logging

from disk_test import base_test
from quarchpy.disk_test.dtsGlobals import dtsGlobals
from quarchpy.disk_test.base_test import BaseTest, IdGenerator
from quarchpy.disk_test.driveTestCore import comms, myHostInfo, specifyQuarchModule, DiskStatusCheck, checkDriveState, \
    get_quarch_modules_qps
from quarchpy.device.quarchQPS import quarchStream
from quarchpy.disk_test.hostInformation import HostInformation
from quarchpy.qps.qpsFuncs import isQpsRunning

"""
> On init, check qps open and request QPS open if none existent
> On start, check qps is open 

"""


class PowerMarginingTest(BaseTest, ABC):
    def __init__(self):
        super(PowerMarginingTest, self).__init__()

        self.my_host_info = HostInformation()

        # Declare custom variables for the test
        self.cv_repeats = self.declare_custom_variable(custom_name="repeats", default_value=1,
                                                       description="Number of times to repeat each hotplug")
        self.cv_ontime = self.declare_custom_variable(custom_name="onTime", default_value=15,
                                                      description="Time to wait for drive to enumerate on host")
        self.cv_offtime = self.declare_custom_variable(custom_name="offTime", default_value=10,
                                                       description="Time to wait for host to remove drive")
        self.cv_power_change_percent = self.declare_custom_variable(custom_name="power change %", default_value=10,
                                                                    description="Number of % to change power")
        self.cv_num_of_increments = self.declare_custom_variable(custom_name="numberOfIncrements", default_value=5,
                                                                 description="Number of increments used for power change")
        self.cv_settling_time = self.declare_custom_variable(custom_name="Settling Time", default_value=5,
                                                             description="Wait time after drive enumeration for power analysis")
        self.cv_linkspeed = self.declare_custom_variable(custom_name="linkspeed", default_value="auto",
                                                         description="Value to compare drive's link speed, GB/s",
                                                         accepted_vals=['2.5GT/s', '5GT/s', '8GT/s', '16GT/s', '32GT/s',
                                                                        'auto'])
        self.cv_landwidth = self.declare_custom_variable(custom_name="lanewidth", default_value="auto",
                                                         description="Value to compare drive's lane width",
                                                         accepted_vals=['x1', 'x2', 'x4', 'x8', 'x16', 'x32', 'auto'])
        self.cv_averaging = self.declare_custom_variable(custom_name="QPS averaging rate", default_value="16k",
                                                         description="Sampling rate for QPS to record power",
                                                         accepted_vals=['32k', '16k', '8k', '4k', '2k', '1k', '512'])

        # Declare additional variables that may not be visible to the user by default
        # Should custom variables have a custom unit, like "ms"?  This may be easier than parsing strings
        self.cv_drivename = self.declare_custom_variable(custom_name="driveName", default_value="drive1",
                                                         var_purpose="internal")
        self.cv_quarchname = self.declare_custom_variable(custom_name="quarchName", default_value="module1",
                                                          var_purpose="internal")

        self.mode = "sas"
        self.voltage_rail = ""

        self.quarch_stream = None
        # Request QPS start if not already open
        self.request_qps()

    def check_prerequisites(self, document_mode=False):
        # need the standard imports
        super(PowerMarginingTest, self).check_prerequisites()

    def start_test(self, document_mode=False):

        #############################
        # CLASS - SETUP /
        #############################

        # Had to move this here as init is now called without a document mode parameter
        self._set_documentation_mode(document_mode)
        self.test_id.reset()
        if not self.request_qps():
            return

        #############################
        # TEST - SETUP
        #############################

        # Start object
        self.test_point(self.test_id.gen_next_id(), test_description="Setting up required test resources")
        self.test_id.up_tier(singular=True)

        self.cv_quarchname.custom_value = self.select_quarch_module(use_qps=True)

        if not self.cv_quarchname.custom_value:
            self.comms.send_stop_test(reason="No Quarch Module Selected")
            return

        self.cv_drivename.custom_value = self.select_drive()

        if not self.cv_drivename.custom_value:
            self.comms.send_stop_test(reason="No Drive Selected")
            return

        # Requires a change to ensure the power isn't set too high for whatever device we're using
        power_setting_12v = 12000
        current_power_12v = 12000
        minimum_power_12v = power_setting_12v - (
                (int(power_setting_12v) / 100) * int(self.cv_power_change_percent.custom_value))
        power_decrement_12v = float(power_setting_12v - minimum_power_12v) / float(
            self.cv_num_of_increments.custom_value)

        logging.info(power_decrement_12v)
        logging.info(minimum_power_12v)

        output_mode_default_voltage = 5000
        current_o_m_voltage = 5000
        self.voltage_rail = "5V"

        if "pcie" in str(self.cv_drivename.custom_value.drive_type).lower():
            self.mode = "pcie"
            output_mode_default_voltage = 3300
            current_o_m_voltage = 3300
            self.voltage_rail = "3V3"

        minimum_o_m_voltage = output_mode_default_voltage - ((int(output_mode_default_voltage) / 100) *
                                                     int(self.cv_power_change_percent.custom_value))

        o_m_power_decrement = float(output_mode_default_voltage - minimum_o_m_voltage) / float(self.cv_num_of_increments.custom_value)

        ##############################
        # TEST - Core
        ##############################

        # ID 1.0
        self.test_id.down_tier(singular=True, description="Beginning Tests core")

        self._reset_device(module=self.cv_quarchname.custom_value)

        time.sleep(3)

        self.test_point(function=self._add_quarch_command,
                        function_args={"command": "run:power down",
                                       "quarch_device": self.cv_quarchname.custom_value})
        self.test_point(function=self._add_quarch_command,
                        function_args={"command": "record:averaging " + str(self.cv_averaging),
                                       "quarch_device": self.cv_quarchname.custom_value})

        self._start_quarch_stream()

        try:

            for loop in range(0, int(self.cv_repeats.custom_value)):
                self.test_id.up_tier(description="Power Margining Example, cycle " + str(int(loop + 1)) + " of " +
                                                 str(self.cv_repeats.custom_value))

                self.test_point(self.test_id.gen_next_id(),
                                function_description="Resetting module voltages",
                                function=self._reset_module_voltages,
                                function_args={})

                self.test_point(self.test_id.gen_next_id(), test_description="Power Margining 12v rail")
                for increment in range(0, int(self.cv_num_of_increments.custom_value) + 1):

                    current_power_12v = int(current_power_12v) - int(power_decrement_12v)

                    logging.info("current power = " + str(current_power_12v))

                    if increment == 0:
                        current_power_12v = power_setting_12v

                    self.test_id.up_tier(description="Power Margining, 12v:" + str(current_power_12v))

                    # Debug Item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "run:power down",
                                                   "quarch_device": self.cv_quarchname.custom_value})

                    # Wait and check for drive
                    enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                                has_return=True,
                                                function_description="Polling system for indication of drive removal",
                                                function_args={'enumeration': False,
                                                               "drive": self.cv_drivename.custom_value,
                                                               "ontime": self.cv_ontime.custom_value,
                                                               "offtime": self.cv_offtime.custom_value})

                    state = self.check_point(self.test_id.gen_next_id(),
                                             description="Checking device not enumerated when powered down",
                                             function=DiskStatusCheck,
                                             function_args={"driveId": self.cv_drivename.custom_value,
                                                            'expectedState': False},
                                             has_return=True)

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Added QPS annotation showing device state",
                                    function=self._add_qps_comment,
                                    function_args={"state": state, "check_power_on": False})

                    # debug item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "sig:12v:volt " + str(current_power_12v),
                                                   "quarch_device": self.cv_quarchname.custom_value})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Start of power up cycle",
                                    function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "start"})

                    # Debug Item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "run:power up",
                                                   "quarch_device": self.cv_quarchname.custom_value})

                    # Wait and check for drive
                    enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                                has_return=True,
                                                function_description="Polling system for indication of drive insertion",
                                                function_args={'enumeration': True,
                                                               "drive": self.cv_drivename.custom_value,
                                                               "ontime": self.cv_ontime.custom_value,
                                                               "offtime": self.cv_offtime.custom_value})
                    # ID = 1.1.4

                    state = self.check_point(self.test_id.gen_next_id(),
                                             description="Checking device enumerated after power up, 12V: {0}".format(str(current_power_12v)),
                                             function=DiskStatusCheck, has_return=True,
                                             function_args={"driveId": self.cv_drivename.custom_value,
                                                            'expectedState': True})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Added QPS annotation showing device state",
                                    function=self._add_qps_comment,
                                    function_args={"state": state, "check_power_on": True})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Waiting {0} seconds for drive to settle after enumeration".format(
                                                          self.cv_settling_time), function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "settling"})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Adding end of cycle annotation",
                                    function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "end"})

                    self.test_id.down_tier()

                self.test_point(self.test_id.gen_next_id(), function_description="Resetting module voltages",
                                function=self._reset_module_voltages, function_args={})

                self.test_point(self.test_id.gen_next_id(),
                                test_description="Power Margining {0} rail".format(self.voltage_rail))

                for increment in range(0, int(self.cv_num_of_increments.custom_value) + 1):

                    current_o_m_voltage = int(current_o_m_voltage) - int(o_m_power_decrement)
                    
                    logging.info("current voltage = " + str(current_o_m_voltage))

                    if increment == 0:
                        current_power_12v = power_setting_12v
                        current_o_m_voltage = output_mode_default_voltage

                    self.test_id.up_tier(description="Power Margining {0}: {1}".format(self.voltage_rail,
                                                                                       current_o_m_voltage))

                    # Debug Item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "run:power down",
                                                   "quarch_device": self.cv_quarchname.custom_value})
                    # Wait and check for drive
                    enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                                has_return=True,
                                                function_description="Polling system for indication of drive removal",
                                                function_args={'enumeration': False,
                                                               "drive": self.cv_drivename.custom_value,
                                                               "ontime": self.cv_ontime.custom_value,
                                                               "offtime": self.cv_offtime.custom_value})

                    state = self.check_point(self.test_id.gen_next_id(),
                                             description="Checking device not enumerated when powered down",
                                             function=DiskStatusCheck,
                                             function_args={"driveId": self.cv_drivename.custom_value,
                                                            'expectedState': False},
                                             has_return=True)

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Added QPS annotation showing device state",
                                    function=self._add_qps_comment,
                                    function_args={"state": state, "check_power_on": False})

                    # debug item
                    if self.mode is "sas":
                        self.test_point(function=self._add_quarch_command,
                                        function_args={"command": "sig:5v:volt " + str(current_o_m_voltage),
                                                       "quarch_device": self.cv_quarchname.custom_value})
                    else:
                        self.test_point(function=self._add_quarch_command,
                                        function_args={"command": "sig:3v3:volt " + str(current_o_m_voltage),
                                                       "quarch_device": self.cv_quarchname.custom_value})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Start of power up cycle",
                                    function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "start"})

                    # Debug Item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "run:power up",
                                                   "quarch_device": self.cv_quarchname.custom_value})

                    # Wait and check for drive
                    enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                                has_return=True,
                                                function_description="Polling system for indication of drive insertion",
                                                function_args={'enumeration': True,
                                                               "drive": self.cv_drivename.custom_value,
                                                               "ontime": self.cv_ontime.custom_value,
                                                               "offtime": self.cv_offtime.custom_value})
                    # ID = 1.1.4
                    state = self.check_point(self.test_id.gen_next_id(),
                                             description="Checking device enumerated after power up, {0}: {1}".format(
                                                        self.voltage_rail, current_o_m_voltage),
                                             function=DiskStatusCheck, has_return=True,
                                             function_args={"driveId": self.cv_drivename.custom_value,
                                                            'expectedState': True})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Added QPS annotation showing device state",
                                    function=self._add_qps_comment,
                                    function_args={"state": state, "check_power_on": True})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Waiting {0} seconds for drive to settle after enumeration".format(
                                                          self.cv_settling_time), function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "settling"})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Adding end of cycle annotation",
                                    function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "end"})

                    self.test_id.down_tier()

                self.test_point(self.test_id.gen_next_id(), function_description="Resetting module voltages",
                                function=self._reset_module_voltages, function_args={})

                self.test_point(self.test_id.gen_next_id(), test_description="Power Margining 12v and {0} rails".format(
                                                                              self.voltage_rail))

                for increment in range(0, int(self.cv_num_of_increments.custom_value) + 1):

                    current_power_12v = int(current_power_12v) - int(power_decrement_12v)

                    logging.info("current power = " + str(current_power_12v))
                    logging.info("current voltage = " + str(current_o_m_voltage))

                    if increment == 0:
                        current_power_12v = power_setting_12v
                        current_o_m_voltage = output_mode_default_voltage

                    self.test_id.up_tier(description="Power Margining 12v:{0}, {1}:{2}".format(current_power_12v,
                                                                                               self.voltage_rail,
                                                                                               current_o_m_voltage))

                    # Debug Item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "run:power down",
                                                   "quarch_device": self.cv_quarchname.custom_value})
                    # Wait and check for drive
                    enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                                has_return=True,
                                                function_description="Polling system for indication of drive removal",
                                                function_args={'enumeration': False,
                                                               "drive": self.cv_drivename.custom_value,
                                                               "ontime": self.cv_ontime.custom_value,
                                                               "offtime": self.cv_offtime.custom_value})

                    state = self.check_point(self.test_id.gen_next_id(),
                                             description="Checking device not enumerated when powered down",
                                             function=DiskStatusCheck,
                                             function_args={"driveId": self.cv_drivename.custom_value,
                                                            'expectedState': False},
                                             has_return=True)

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Added QPS annotation showing device state",
                                    function=self._add_qps_comment,
                                    function_args={"state": state, "check_power_on": False})

                    # debug item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "sig:12v:volt " + str(current_power_12v),
                                                   "quarch_device": self.cv_quarchname.custom_value})
                    if self.mode is "sas":
                        self.test_point(function=self._add_quarch_command,
                                        function_args={"command": "sig:5v:volt " + str(current_o_m_voltage),
                                                       "quarch_device": self.cv_quarchname.custom_value})
                    else:
                        self.test_point(function=self._add_quarch_command,
                                        function_args={"command": "sig:3v3:volt " + str(current_o_m_voltage),
                                                       "quarch_device": self.cv_quarchname.custom_value})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Start of power up cycle",
                                    function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "start"})

                    # Debug Item
                    self.test_point(function=self._add_quarch_command,
                                    function_args={"command": "run:power up",
                                                   "quarch_device": self.cv_quarchname.custom_value})

                    # Wait and check for drive
                    enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                                has_return=True,
                                                function_description="Polling system for indication of drive insertion",
                                                function_args={'enumeration': True,
                                                               "drive": self.cv_drivename.custom_value,
                                                               "ontime": self.cv_ontime.custom_value,
                                                               "offtime": self.cv_offtime.custom_value})

                    # ID = 1.1.4
                    state = self.check_point(self.test_id.gen_next_id(),
                                             description="Checking device enumerated after power up 12v: {0}, {1}: {2}".format(
                                                          current_power_12v, self.voltage_rail, current_o_m_voltage),
                                             function=DiskStatusCheck, has_return=True,
                                             function_args={"driveId": self.cv_drivename.custom_value,
                                                            'expectedState': True})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Added QPS annotation showing device state",
                                    function=self._add_qps_comment,
                                    function_args={"state": state, "check_power_on": True})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Waiting {0} seconds for drive to settle after enumeration".format(
                                                          self.cv_settling_time), function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "settling"})

                    self.test_point(self.test_id.gen_next_id(),
                                    function_description="Adding end of cycle annotation",
                                    function=self._add_qps_annotation,
                                    function_args={"parent_id": self.test_id.return_parent_id(), "type": "end"})

                    self.test_id.down_tier()

                self.test_id.down_tier()

        except Exception as e:
            print(e)

        self._end_quarch_stream()
        self._reset_device(module=self.cv_quarchname.custom_value)

    def _reset_module_voltages(self):
        self.test_point(function=self._add_quarch_command,
                        function_args={"command": "sig:12v:volt 12000",
                                       "quarch_device": self.cv_quarchname.custom_value})

        if self.mode == "pcie":
            self.test_point(function=self._add_quarch_command,
                            function_args={"command": "sig:3v3:volt 3300",
                                           "quarch_device": self.cv_quarchname.custom_value})
        else:
            self.test_point(function=self._add_quarch_command,
                            function_args={"command": "sig:5v:volt 5000",
                                           "quarch_device": self.cv_quarchname.custom_value})


    def _start_quarch_stream(self):
        # Begin Stream
        file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
        time.sleep(3)
        if not self.document_mode:
            self.quarch_stream = self.cv_quarchname.custom_value.startStream(dtsGlobals.qcs_dir + file_name)
        else:
            self.quarch_stream = None

    def _end_quarch_stream(self):
        if not self.document_mode:
            self.quarch_stream.stopStream()
        else:
            return

    def _add_qps_comment(self, state, check_power_on):
        desc = ""
        y_pos = 100
        # Colour shows red if fail, green if pass?
        colour = "green" if state else "red"
        on_state = "on" if state else "off"
        off_state = "off" if state else "on"

        if check_power_on:
            desc = "Checking device powered on\nDevice State : " + str(on_state)
            y_pos = 70
        else:
            desc = "Checking power off,\rDevice State : " + str(off_state)
            y_pos = 50

        # will need to change to assign colours.
        self.quarch_stream.addComment(title=desc, yPos=y_pos)

    def _add_qps_annotation(self, parent_id, type):
        start_annotation = "START:" + str(parent_id)
        end_annotation = "END:" + str(parent_id)
        settling_time_annotation = "ST:" + str(parent_id)
        # will need to change to assign colours.
        if "start" in str(type):
            self.quarch_stream.addAnnotation(title=start_annotation)
        if "end" in str(type):
            self.quarch_stream.addAnnotation(title=end_annotation)
        if "settling" in str(type):
            time.sleep(int(self.cv_settling_time.custom_value))
            self.quarch_stream.addAnnotation(title=settling_time_annotation)

    def _add_qps_stats(self, parent_id):
        start_annotation = "START:" + str(parent_id)
        end_annotation = "END:" + str(parent_id)
        settling_time_annotation = "ST:" + str(parent_id)

        stats = self.quarch_stream.get_stats()

        index = stats.index[stats['Text'] == settling_time_annotation].tolist()
        value = str(stats['current 12V Max'].loc[index[0]])

        self.comms.sendMsgToGUI(self.comms.create_request_log(time.time(), "Debug", "Max Inrush 12V Current : " + value,
                                                              sys._getframe().f_code.co_name, uId=""))
