from pymavlink import mavutil


def set_return(connection):
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)


if __name__ == '__main__':
    connection = mavutil.mavlink_connection('udpin:localhost:14550')
    connection.wait_heartbeat()
    print(f"Connection established.\nSystem: {connection.target_system}\nComponent: {connection.target_component}")
    set_return(connection)
