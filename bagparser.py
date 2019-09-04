import os
import sys
import getopt
import rosbag
from parsers import \
    parse_sensor_msgs_laser_scan, \
    parse_sensor_msgs_image, \
    parse_sensor_msgs_camera_info

msgs_md5_to_parse_functions = \
    {
        '90c7ef2dc6895d81024acba2ac42f369': parse_sensor_msgs_laser_scan,
        '060021388200f6f0f447d0fcd9c64743': parse_sensor_msgs_image,
        'c9a58c1b0b154e0e6da7578cb991d214': parse_sensor_msgs_camera_info
    }


def parse_bag(bag_file_name, result_folder_name):
    os.mkdir(result_folder_name)
    with rosbag.Bag(bag_file_name, 'r') as bag_file:
        # create dict from topic name to message md5
        type_and_topic_info = bag_file.get_type_and_topic_info()
        msgs_to_md5 = type_and_topic_info[0]
        topics_to_msgs_md5 = {}
        for topic_name, topic_desc in type_and_topic_info[1].items():
            topics_to_msgs_md5[topic_name] = msgs_to_md5[topic_desc.msg_type]
        # parse messages
        for topic, msg, time_msg in bag_file.read_messages():
            # get topic msg md5
            topic_msg_md5 = topics_to_msgs_md5.get(topic)
            # if parse function exists
            if topic_msg_md5:
                msgs_md5_to_parse_functions[topic_msg_md5](msg, time_msg, result_folder_name)
            else:
                sys.stderr.write(topic + ' parsing not supported\n')


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file=", "folder="])
        for opt, arg in opts:
            if opt == '--file':
                file_name = arg
            elif opt == '--folder':
                folder_name = arg
        parse_bag(file_name, folder_name)
    except getopt.GetoptError as error:
        sys.stderr.write(str(error))
    except Exception as error:
        sys.stderr.write(str(error))
