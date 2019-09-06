import os
import sys
import getopt
import rosbag
from utilites import get_msg_local_date_time
from parsers import parse_functions
from json_bag import create_json
from txt_bag import create_txt
from xml_bag import create_xml


def message_generator(bag_file, topic_to_msg_md5, result_folder_name):
    for topic, msg, time_msg in bag_file.read_messages():
        topic_msg_md5 = topic_to_msg_md5[topic]
        parse_function = parse_functions.get(topic_msg_md5)
        if parse_function:
            local_date_time = get_msg_local_date_time(time_msg)
            yield parse_function(msg, local_date_time, result_folder_name)
        else:
            sys.stderr.write(topic + ' parsing not supported\n')


def get_topic_to_msg_md5_dict(bag_file):
    type_and_topic_info = bag_file.get_type_and_topic_info()
    msg_to_md5 = type_and_topic_info[0]
    topic_to_msg_md5 = {}
    for topic_name, topic_desc in type_and_topic_info[1].items():
        topic_to_msg_md5[topic_name] = msg_to_md5[topic_desc.msg_type]
    return topic_to_msg_md5


def parse_bag(bag_file_name, result_folder_name, parse_format):
    os.mkdir(result_folder_name)
    with rosbag.Bag(bag_file_name, 'r') as bag_file:
        topic_to_msg_md5 = get_topic_to_msg_md5_dict(bag_file)
        messages = message_generator(bag_file, topic_to_msg_md5, result_folder_name)
        if parse_format == 'txt':
            create_txt(messages)
        elif parse_format == 'xml':
            create_xml(messages)
        elif parse_format == 'json':
            create_json(messages)
        else:
            sys.stderr.write('invalid format')


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file=", "folder=", "format="])
        file_name = None
        folder_name = None
        parse_format = 'txt'
        for opt, arg in opts:
            if opt == '--file':
                file_name = arg
            elif opt == '--folder':
                folder_name = arg
            elif opt == '--format':
                parse_format = arg
        if not (file_name and folder_name):
            sys.stderr.write('file and folder options are required')
        else:
            parse_bag(file_name, folder_name, parse_format)
    except getopt.GetoptError as error:
        sys.stderr.write(str(error))
    except Exception as error:
        sys.stderr.write(str(error))

    # print_msgs_md5('bag_files/FLY_1.bag', 'msg_md5.txt')

    # with rosbag.Bag('bag_files/FLY_1.bag', 'r') as bag_file:
    #     for topic, msg, time_msg in bag_file.read_messages():
    #         print(topic)
