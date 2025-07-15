
import time
from NatNetClient import NatNetClient
from util import quaternion_to_euler

positions = {}
rotations = {}


# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receive_rigid_body_frame(id, position, rotation_quaternion):
    print("I am running!")
    # Position and rotation received
    positions[id] = position
    # The rotation is in quaternion. We need to convert it to euler angles
    rotx, roty, rotz = quaternion_to_euler(rotation_quaternion)
    # Store the roll pitch and yaw angles
    rotations[id] = (rotx, roty, rotz)

def receive_new_frame(data_dict):
    pass

if __name__ == "__main__":
    clientAddress = "192.168.1.217"
    optitrackServerAddress = "192.168.1.10"
    robot_id = 69

    # This will create a new NatNet client
    streaming_client = NatNetClient()
    streaming_client.set_client_address(clientAddress)
    streaming_client.set_server_address(optitrackServerAddress)
    streaming_client.set_use_multicast(False)
    # Configure the streaming client to call our rigid body handler on the emulator to send data out.
    streaming_client.new_frame_listener = receive_new_frame
    streaming_client.rigid_body_listener = receive_rigid_body_frame
    streaming_client.set_print_level(2)
    # Start up the streaming client now that the callbacks are set up.
    # This will run perpetually, and operate on a separate thread.
    is_running = streaming_client.run()
    while is_running:
        time.sleep(1)
        print("running")
        if robot_id in positions:
            print("position print!")
            # last position
            print('Last position', positions[robot_id], ' rotation', rotations[robot_id])
        if streaming_client.connected() is False:
             print("no connection")

        
