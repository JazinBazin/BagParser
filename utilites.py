import rosbag


def print_msgs_md5(bag_file_name, output_file_name):
    """Prints all message types and their md5, that exists in bag_file, to output_file"""
    with rosbag.Bag(bag_file_name, 'r') as bag_file:
        msgs_to_md5 = bag_file.get_type_and_topic_info()[0]
        with open(output_file_name, 'w') as output_file:
            for msg_name, md5 in msgs_to_md5.items():
                output_file.write('Msg: ' + msg_name + '\n' +
                                  'md5: ' + md5 + '\n\n')
