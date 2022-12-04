from functions import get_message
from pymavlink import mavutil
from sys import argv
import os


if __name__ == '__main__':
    if os.uname().machine == "x86_64":
        connection = mavutil.mavlink_connection('udpin:localhost:14550')
    else:
        connection = mavutil.mavlink_connection('dev/ttyTHS1')
    try:
        message_type = argv[1]
    except:
        message_type = "COMMAND_ACK"
    while True:
        msg = get_message(connection, message_type=message_type, just_print=False)

