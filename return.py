from pymavlink import mavutil
import os

def set_return(connection):
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)


if __name__ == '__main__':
    if os.uname().machine == "x86_64":
        connection = mavutil.mavlink_connection('udpin:localhost:14550')
    else:
        connection = mavutil.mavlink_connection('dev/ttyTHS1')
    print(f"Connection established.\nSystem: {connection.target_system}\nComponent: {connection.target_component}")
    set_return(connection)
