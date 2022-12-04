import os
from sys import argv
from functions import get_message, check_position
from pymavlink import mavutil
# from upload_mission import cords
from time import sleep

os.environ["MAVLINK20"] = '1'
if __name__ == '__main__':
    if os.uname().machine == "x86_64":
        connection = mavutil.mavlink_connection('udpin:localhost:14550')
    else:
        connection = mavutil.mavlink_connection('dev/ttyTHS1')

    try:
        is_come_back = bool(argv[1])
    except IndexError:
        print("Variable 'is_come_back' is set to default False.")
        is_come_back = False
    except ValueError:
        print("Invalid type of value. Variable distance is set to 10.")
        is_come_back = False
    finally:
        print("START")
        # const
        take_off_distance = 10
        txt_file_with_points = "./cords.txt"
        speed = 100  # :)))
        # upload mission
        os.system(f"python3.10 /home/bartek/PycharmProjects/akl_piwo_1/upload_mission.py {txt_file_with_points}")
        # change mode to guide, arm and take off
        os.system(f"python3.10 /home/bartek/PycharmProjects/akl_piwo_1/takeoff.py {take_off_distance}")
        # change speed
        os.system(f"python3.10 /home/bartek/PycharmProjects/akl_piwo_1/set_speed.py {speed}")
        # start mission
        os.system("python3.10 /home/bartek/PycharmProjects/akl_piwo_1/start_mission.py")
        print("2.0", mavutil.mavlink20())


        # check if is landed  -->  TO DO
        # if is_come_back:
        #     os.system("python3.10 /home/bartek/PycharmProjects/akl_piwo_1/return.py")
        #
        # connection = mavutil.mavlink_connection('udpin:localhost:14550')
        # connection.wait_heartbeat()
        # dest_cords = (float(cords[len(cords)-1][0]), float(cords[len(cords)-1][1]), 0)
        # while True:
        #     global_pos = get_message(connection, message_type="GLOBAL_POSITION_INT", just_print=False)
        #     local_pos = get_message(connection, message_type="LOCAL_POSITION_NED", just_print=False)
        #     current_pos = (global_pos.__dict__['lat'], global_pos.__dict__['lat'], local_pos.__dict__['z'])
        #     if check_position(current_pos, dest_cords):
        #         sleep(10)
        #         print("Destination achieved.")
        #         if is_come_back:
        #             print("Destination achieved. It's time to come back!")
        #             os.system("python3.10 /home/bartek/PycharmProjects/akl_piwo_1/return.py")
        #
        #         # if (lat < 1.1*int(float(last_point_cords[0])*10**8 and lat < 0.9*int(float(last_point_cords[0])*10**8))) and
        #     #     (lon < 1.1*int(float(last_point_cords[1])*10**8 and lon < 0.9*int(float(last_point_cords[1])*10**8)))
        #     #             and abs(z) < 0.5:
        #         print("Destination achieved")
        #     # if (round(abs(msg.__dict__['x']), 3) > 1)
        #     #     and (round(abs(msg.__dict__['z']), 3) > 1) and (round(abs(msg.__dict__['z']), 3) > 1):





