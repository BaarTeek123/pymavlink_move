from pymavlink import mavutil
from functions import get_message
from change_mode import change_mode
from arm import arm
from sys import argv


def take_off(connection: mavutil.mavudp, distance: int = 10) -> None:
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, distance)


if __name__ == "__main__":
    try:
        distance = int(argv[1])
    except IndexError:
        distance = 10
    except ValueError:
        print("Invalid type of value. Variable distance is set to 10.")
        distance = 10

    # establish connection
    connection = mavutil.mavlink_connection('udpin:localhost:14550')
    connection.wait_heartbeat()
    print(f"Connection established.\nSystem: {connection.target_system}\nComponent: {connection.target_component}")

    # change mode
    while True:
        msg = connection.recv_match(type='HEARTBEAT', blocking=False)
        if msg:
            mode = mavutil.mode_string_v10(msg)
            if mode != "GUIDED":
                change_mode(connection, mode="GUIDED")
            if mode == "GUIDED":
                break

    # arm
    print("---Arming---")
    arm(connection)
    get_message(connection)
    connection.motors_armed_wait()
    print('---Armed!---')

    msg = get_message(connection, message_type="LOCAL_POSITION_NED", just_print=False)
    # take off
    if connection.motors_armed() and not (round(abs(msg.__dict__['z']), 3) > 0.2):
        print("Taking off")
        take_off(connection, distance)
        get_message(connection)
    else:
        raise Exception("Motors are not armed or is already in the air.")

    while True:
        msg = connection.recv_match(type='LOCAL_POSITION_NED', blocking=False)
        if msg:
            if round(abs(msg.__dict__['z']), 3) > 0.95 * distance:
                break

    print(f"Took off. Current height {round(abs(msg.__dict__['z']), 3)}")
