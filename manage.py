import os

if __name__ == '__main__':
    print("START")
    # const
    take_off_distance = 10
    txt_file_with_points = "/home/bartek/PycharmProjects/mavlink-test/cords.txt"
    # upload mission
    os.system(f"python3.10 /home/bartek/PycharmProjects/akl_piwo_1/upload_mission.py {txt_file_with_points}")
    # change mode to guide, arm and take off
    os.system(f"python3.10 /home/bartek/PycharmProjects/akl_piwo_1/takeoff.py {take_off_distance}")
    #start mission
    os.system("python3.10 /home/bartek/PycharmProjects/akl_piwo_1/start_mission.py")



