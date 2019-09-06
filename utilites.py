import os
import time
import rosbag


def get_msg_local_date_time(msg_time):
    return time.strftime('%x %X', time.localtime(msg_time.to_sec()))


def mkdir_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def print_msgs_md5(bag_file_name, output_file_name):
    """Prints to output_file all message types and their md5, that exists in bag_file"""
    with rosbag.Bag(bag_file_name, 'r') as bag_file:
        msgs_to_md5 = bag_file.get_type_and_topic_info()[0]
        with open(output_file_name, 'w') as output_file:
            for msg_name, md5 in msgs_to_md5.items():
                output_file.write('Msg: ' + msg_name + '\n' +
                                  'md5: ' + md5 + '\n\n')
