#!/usr/bin/env python3
""" log parser
    Accepts a filename on the command line.  The file is a linux-like log file
    from a system you are debugging.  Mixed in among the various statements are
    messages indicating the state of the device.  They look like:
        Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON
    The device state message has many possible values, but this program only
    cares about three: ON, OFF, and ERR.

    Your program will parse the given log file and print out a report giving
    how long the device was ON, and the time stamp of any ERR conditions.
"""

import sys
import re
import datetime

log_line_pattern = r'^(\w{3}\s\d{2} \d{2}:\d{2}:\d{2}):\d{3} \[\d+\] dut: Device State: (\w+)'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Incorrect arguments.  Please supply a file name')
        exit()

    is_on = False
    current_start = None
    total_time = 0

    with open(sys.argv[1]) as f:
        for line in f:
            parsed_line = re.findall(log_line_pattern, line)
            if len(parsed_line) > 0:
                if parsed_line[0][1] == 'ERR':
                    print(f'ERR: {parsed_line[0]}')
                else:
                    current_timestamp = datetime.datetime.strptime(parsed_line[0][0], '%b %d %H:%M:%S')
                    if parsed_line[0][1] == 'ON':
                        if not is_on:
                            is_on = True
                            current_start = current_timestamp
                    if parsed_line[0][1] == 'OFF':
                        if is_on:
                            is_on = False
                            total_time += (current_timestamp - current_start).total_seconds()
    
    print(f'On for: {total_time}')

    #print("There are no unit tests for logparse.")
