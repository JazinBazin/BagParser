import os
import time
from PIL import Image

SPACE_BETWEEN_MSGS = '\n\n\n'


def mkdir_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_message(msgs_file, msg, time_of_msg):
    mkdir_if_not_exist(msgs_file)
    with open(msgs_file, 'a') as msgs_file_obj:
        msgs_file_obj.write("Date/Time: " + time.strftime('%x %X', time.localtime(time_of_msg.to_sec())) + '\n')
        msgs_file_obj.write(msg + SPACE_BETWEEN_MSGS)


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


def parse_sensor_msgs_camera_info(msg, time_of_msg, result_folder):
    msgs_file = os.path.join(result_folder, 'sensor_msgs_camera_info', 'data.txt')
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
    write_message(msgs_file, message, time_of_msg)


def parse_sensor_msgs_image(msg, time_of_msg, result_folder):
    msgs_subdirectory = 'sensor_msgs_images'
    img_file = os.path.join(result_folder, msgs_subdirectory, 'img' + str(msg.header.stamp) + '.jpeg')
    msgs_file = os.path.join(result_folder, msgs_subdirectory, 'data.txt')
    mkdir_if_not_exist(img_file)
    Image.frombytes('RGB', (msg.width, msg.height), bytes(msg.data)).save(img_file, "JPEG")

    message = \
        parse_std_msgs_header(msg.header) + '\n' + \
        'height: ' + str(msg.height) + '\n' + \
        'width: ' + str(msg.width) + '\n' + \
        'encoding: ' + msg.encoding + '\n' + \
        'is_bigendian: ' + str(msg.is_bigendian) + '\n' + \
        'step: ' + str(msg.step) + '\n' + \
        'image: ' + img_file

    write_message(msgs_file, message, time_of_msg)


def parse_sensor_msgs_laser_scan(msg, time_of_msg, result_folder):
    msgs_file = os.path.join(result_folder, 'sensor_msgs_laser_scan', 'data.txt')
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

    write_message(msgs_file, message, time_of_msg)
