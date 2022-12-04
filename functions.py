from pymavlink import mavutil
from math import nan


def get_message(connection: mavutil.mavudp, message_type: str = "COMMAND_ACK", just_print: bool = True,
                is_blocking: bool = True) -> None or str:
    print(connection.recv_match(type=message_type, blocking=is_blocking))
    if not just_print:
        return connection.recv_match(type=message_type, blocking=is_blocking)


def get_points_from_txt_file(filepath: str) -> list:
    with open(filepath) as file:
        cords = file.read().splitlines()
    print(cords)
    for i in range(len(cords)):
        cords[i] = tuple(cords[i].split())
    return cords


def check_position(current_pos, dest_pos):
    # current pos (lat, lon, z)
    if '.' in str(current_pos[0]):
        current_pos[0] = int(float(current_pos[0]) * 10 ** 8)
    if '.' in str(current_pos[1]):
        current_pos[1] = int(float(current_pos[1]) * 10 ** 8)
    if '.' in str(dest_pos[0]):
        dest_pos[0] = int(float(dest_pos[0]) * 10 ** 8)
    if '.' in str(dest_pos[1]):
        dest_pos[1] = int(float(dest_pos[1]) * 10 ** 8)
    if (int(current_pos[0]) < 1.05 * int(current_pos[0]) and  int(dest_pos[0]) > 0.95 * int(dest_pos[0])) and (int(current_pos[1]) < 1.05 * int(dest_pos[1]) and int(current_pos[1]) > 0.95 * int(dest_pos[1])) and  abs(current_pos) < 0.3:
        return True

    # if (lat < 1.1 * int(
    #         float(last_point_cords[0]) * 10 ** 8 and lat < 0.9 * int(float(last_point_cords[0]) * 10 ** 8))) and
    #     (lon < 1.1 * int(
    #         float(last_point_cords[1]) * 10 ** 8 and lon < 0.9 * int(float(last_point_cords[1]) * 10 ** 8)))
    #     and abs(z) < 0.5:
    print("Destination achieved")


class mission_item:
    def __init__(self, id, current, latitude, longitude, attitude):
        #	Global (WGS84) coordinate frame (scaled) + altitude relative to the home position.
        #	1st value (x): latitude in degrees*1E7,
        #	2nd value (y): longitude in degrees*1E7,
        #	3rd value z: positive altitude with 0 being at the altitude of the home position.
        # self.target_system = connection.target_system
        # self.target_component = connection.target_component
        self.seq = id
        self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        self.cmd = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT  # Navigate to waypoint.
        self.current = current
        self.auto_continue = 1  # 0 -> false == pause mission after the item completes; 1 -> true,
        self.param1 = 0.0
        self.param2 = 2.0
        self.param3 = 20.0
        self.param4 = nan
        self.param5 = latitude
        self.param6 = longitude
        self.param7 = attitude
        self.mission_type = 0  # https://mavlink.io/en/messages/common.html#MAV_MISSION_TYPE

# def set_target_in_meters(connection: mavutil.mavudp, x: int = 0, y: int = 0, z: int = 0):
#     """x > 0 --> forward (North)
#     y > 0 --> right (East)
#     z > 0 --> down"""
#     connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, connection.target_system,
#                                                                                       connection.target_component,
#                                                                                       mavutil.mavlink.MAV_FRAME_LOCAL_NED,
#                                                                                       int(0b110111111000),
#                                                                                       x, y, z,
#                                                                                       0, 0, 0,
#                                                                                       0, 0, 0,
#                                                                                       0, 0))
#
#
# def set_target_geo(connection: mavutil.mavudp, latitude: float, longitude: float):
#     connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, connection.target_system,
#                                                                                        connection.target_component,
#                                                                                        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
#                                                                                        int(0b110111111000),
#                                                                                        int(latitude * 10 ** 7),
#                                                                                        int(longitude * 10 ** 7), 0,
#                                                                                        0, 0, 0,
#                                                                                        0, 0, 0,
#                                                                                        0, 0))
