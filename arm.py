from pymavlink import mavutil
from functions import get_message
from change_mode import change_mode


def arm(connection: mavutil.mavudp) -> None:
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)


if __name__ == "__main__":
    # establish connection
    connection = mavutil.mavlink_connection('udpin:localhost:14550')
    connection.wait_heartbeat()
    print(f"Connection established.\nSystem: {connection.target_system}\nComponent: {connection.target_component}")
    while True:
        msg = connection.recv_match(type='HEARTBEAT', blocking=False)
        if msg:
            mode = mavutil.mode_string_v10(msg)
            if mode != "GUIDED":
                change_mode(connection, mode="GUIDED")
            break
    arm(connection)
    get_message(connection)




