from functions import get_message
from pymavlink import mavutil
from sys import argv

if __name__ == '__main__':

    connection = mavutil.mavlink_connection('udpin:localhost:14550')
    connection.wait_heartbeat()
    try:
        message_type = argv[1]
    except:
        message_type = "COMMAND_ACK"
    while True:
        msg = get_message(connection, message_type=message_type, just_print=False)

