import os

from pymavlink import mavutil
from functions import get_message
from sys import argv


def change_mode(connection: mavutil.mavudp, mode: str = "GUIDED") -> None:
    if mode not in connection.mode_mapping():
        raise Exception(f'Unknown mode : {format(mode)}\nTry:', list(connection.mode_mapping().keys()))

    # Get mode ID
    mode_id = connection.mode_mapping()[mode]

    # master.set_mode(mode_id) or:
    connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)


if __name__ == "__main__":
    # establish connection
    if os.uname().machine == "x86_64":
        connection = mavutil.mavlink_connection('udpin:localhost:14550')
    else:
        connection = mavutil.mavlink_connection('dev/ttyTHS1')


    connection.wait_heartbeat()
    print(f"Connection established.\nSystem: {connection.target_system}\nComponent: {connection.target_component}")
    try:
        mode = argv[1]
    except:
        mode = "GUIDED"
    finally:
        change_mode(connection, mode=mode)
        get_message(connection)
