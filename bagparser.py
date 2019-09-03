import os
import sys
import time
import getopt
import rosbag
from PIL import Image

SPACE_BETWEEN_MSGS = '\n\n\n'


def parse_std_msgs_header(header):
    return 'Header:\n' + \
           '    stamp.secs: ' + str(header.stamp.secs) + '\n' + \
           '    stamp.nsecs: ' + str(header.stamp.nsecs) + '\n' + \
           '    seq: ' + str(header.seq) + '\n' + \
           '    frame_id: ' + str(header.frame_id)


def parse_sensor_msgs_region_of_interest(roi):
    return 'roi:\n' + \
           '    x_offset: ' + str(roi.x_offset) + '\n' + \
           '    y_offset: ' + str(roi.y_offset) + '\n' + \
           '    height: ' + str(roi.height) + '\n' + \
           '    width: ' + str(roi.width) + '\n' + \
           '    do_rectify: ' + str(roi.do_rectify)


def parse_sensor_msgs_camera_info(msg, topic_file):
    message = parse_std_msgs_header(msg.header) + '\n' + \
              'height: ' + str(msg.height) + '\n' + \
              'width: ' + str(msg.width) + '\n' + \
              'distortion_model: ' + str(msg.distortion_model) + '\n' + \
              'D: ' + str(list(msg.D)) + '\n' + \
              'K: ' + str(list(msg.K)) + '\n' + \
              'R: ' + str(list(msg.R)) + '\n' + \
              'P: ' + str(list(msg.P)) + '\n' + \
              'binning_x: ' + str(msg.binning_x) + '\n' + \
              'binning_y: ' + str(msg.binning_y) + '\n' + \
              parse_sensor_msgs_region_of_interest(msg.roi)
    topic_file.write(message + SPACE_BETWEEN_MSGS)


def touch(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    with open(path, 'w'):
        os.utime(path, None)


def parse_sensor_msgs_image(msg, topic_file):
    img_file_name = os.path.join('sensor_msgs_images', 'img' + str(msg.header.stamp) + '.jpeg')
    image = Image.frombytes('RGB', (msg.width, msg.height), bytes(msg.data))
    touch(img_file_name)
    image.save(img_file_name, "JPEG")

    message = \
        parse_std_msgs_header(msg.header) + '\n' + \
        'height: ' + str(msg.height) + '\n' + \
        'width: ' + str(msg.width) + '\n' + \
        'encoding: ' + msg.encoding + '\n' + \
        'is_bigendian: ' + str(msg.is_bigendian) + '\n' + \
        'step: ' + str(msg.step) + '\n' + \
        'image: ' + img_file_name

    topic_file.write(message + SPACE_BETWEEN_MSGS)


def parse_sensor_msgs_laser_scan(msg, topic_file):
    message = parse_std_msgs_header(msg.header) + '\n' + \
              'angle_min: ' + str(msg.angle_min) + '\n' + \
              'angle_max: ' + str(msg.angle_max) + '\n' + \
              'angle_increment: ' + str(msg.angle_increment) + '\n' + \
              'time_increment: ' + str(msg.time_increment) + '\n' + \
              'scan_time: ' + str(msg.scan_time) + '\n' + \
              'range_min: ' + str(msg.range_min) + '\n' + \
              'range_max: ' + str(msg.range_max) + '\n' + \
              'ranges: ' + str(list(msg.ranges)) + '\n' + \
              'intensities: ' + str(list(msg.intensities))
    topic_file.write(message + SPACE_BETWEEN_MSGS)


def write_topic(topic_md5, msg, time_msg, topic_file):
    topic_file.write("Date/Time: " + time.strftime('%x %X', time.localtime(time_msg.to_sec())) + '\n')
    topic_parser = msgs_to_parse_functions[topic_md5]
    topic_parser(msg, topic_file)


def parse_bag(bag_file_name, result_folder_name):
    os.mkdir(result_folder_name)
    with rosbag.Bag(bag_file_name, 'r') as bag_file:

        type_and_topic_info = bag_file.get_type_and_topic_info()
        msgs_to_md5 = type_and_topic_info[0]
        topics_to_md5 = {}
        for topic_name, topic_desc in type_and_topic_info[1].items():
            topics_to_md5[topic_name] = msgs_to_md5[topic_desc.msg_type]

        passed_topics = set()
        for topic, msg, time_msg in bag_file.read_messages():
            topic_folder = topic.replace('/', '@')
            topic_file_name = topic_folder + '.txt'
            topic_file_path = os.path.join(result_folder_name, topic_folder, topic_file_name)
            if topic in passed_topics:
                with open(topic_file_path, 'a') as topic_file:
                    write_topic(topics_to_md5[topic], msg, time_msg, topic_file)
            else:
                topic_md5 = topics_to_md5.get(topic)
                if topic_md5:
                    passed_topics.add(topic)
                    touch(topic_file_path)
                    with open(topic_file_path, 'w') as topic_file:
                        write_topic(topic_md5, msg, time_msg, topic_file)
                else:
                    sys.stderr.write(topic + ' parsing not supported\n')


def print_msgs_md5(bag_file_name, output_file_name):
    with rosbag.Bag(bag_file_name, 'r') as bag_file:
        msgs_to_md5 = bag_file.get_type_and_topic_info()[0]
        with open(output_file_name, 'w') as output_file:
            for msg_name, md5 in msgs_to_md5.items():
                output_file.write('Msg: ' + msg_name + '\n' +
                                  'md5: ' + md5 + '\n\n')


msgs_to_parse_functions = \
    {
        '90c7ef2dc6895d81024acba2ac42f369': parse_sensor_msgs_laser_scan,
        '060021388200f6f0f447d0fcd9c64743': parse_sensor_msgs_image,
        'c9a58c1b0b154e0e6da7578cb991d214': parse_sensor_msgs_camera_info
    }

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
        sys.stderr.write(error)
    except Exception as error:
        sys.stderr.write(str(error))
