from functions import get_message
from pymavlink import mavutil


def start_mission(connection):
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)


if __name__ == '__main__':
    connection = mavutil.mavlink_connection('udpin:localhost:14550')
    connection.wait_heartbeat()
    msg = get_message(connection, message_type="LOCAL_POSITION_NED", just_print=False)
    if not connection.motors_armed():
        raise Exception("Mission can not be start. Firstly remember to arm.")
    elif round(abs(msg.__dict__['z']), 3) < 0.2:
        raise Exception("The height is too low. Check if You have already took off.")
    start_mission(connection)
    get_message(connection)
