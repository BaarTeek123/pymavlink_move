from pymavlink import mavutil
from sys import argv
from functions import mission_item, get_points_from_txt_file, get_message
from change_mode import change_mode
import os

def upload_mission(connection, mission_items) -> None:
    connection.mav.mission_count_send(connection.target_system, connection.target_component, len(mission_items), 0)
    for waypoint in mission_items:
        connection.mav.mission_item_send(connection.target_system,
                                         connection.target_component,
                                         waypoint.seq,
                                         waypoint.frame,
                                         waypoint.cmd,
                                         waypoint.current,
                                         waypoint.auto_continue,
                                         waypoint.param1,  # hold time
                                         waypoint.param2,  # accept radius
                                         waypoint.param3,  # pass radius
                                         waypoint.param4,  # yaw
                                         waypoint.param5,  # local x (longitude)
                                         waypoint.param6,  # local y (latitude)
                                         waypoint.param7,  # local z (attitude)
                                         waypoint.mission_type)
        get_message(connection, message_type="MISSION_REQUEST")


default_file_path = "/home/bartek/PycharmProjects/mavlink-test/cords.txt"
try:
    file = argv[1]
    cords = get_points_from_txt_file(argv[1])
except FileNotFoundError:
    print("File with coordinates does not exit!")
except IndexError:
    cords = get_points_from_txt_file(default_file_path)

if __name__ == '__main__':

    if os.uname().machine == "x86_64":
        connection = mavutil.mavlink_connection('udpin:localhost:14550')
    else:
        connection = mavutil.mavlink_connection('dev/ttyTHS1')
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

    # set waypoints
    waypoints = [mission_item(i, 0, float(cords[i][0]), float(cords[i][1]), 10) for i in range(len(cords) - 1)]

    for k in waypoints:
        print(k.__dict__)
    upload_mission(connection, waypoints)
    get_message(connection, message_type="MISSION_ACK")
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, float(cords[len(cords) - 1][0]),
                                     float(cords[len(cords) - 1][1]), 0)
