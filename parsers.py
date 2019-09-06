import os
from PIL import Image
from utilites import mkdir_if_not_exist


def parse_std_msgs_header(header):
    return {
        'stamp.secs': str(header.stamp.secs),
        'stamp.nsecs': str(header.stamp.nsecs),
        'seq': str(header.seq),
        'frame_id': str(header.frame_id)
    }


def parse_sensor_msgs_region_of_interest(roi):
    return {
        'x_offset': str(roi.x_offset),
        'y_offset': str(roi.y_offset),
        'height': str(roi.height),
        'width': str(roi.width),
        'do_rectify': str(roi.do_rectify)
    }


def parse_geometry_msgs_quaternion(quaternion):
    return {
        'x': str(quaternion.x),
        'y': str(quaternion.y),
        'z': str(quaternion.z),
        'w': str(quaternion.w),
    }


def parse_geometry_msgs_vector3(vector3):
    return {
        'x': str(vector3.x),
        'y': str(vector3.y),
        'z': str(vector3.z),
    }


def parse_sensor_msgs_camera_info(msg, msg_date_time, result_folder):
    return {
        'folder': os.path.join(result_folder, 'sensor_msgs_camera_info'),
        'data': {
            'date_time': msg_date_time,
            'header': parse_std_msgs_header(msg.header),
            'height': str(msg.height),
            'width': str(msg.width),
            'distortion_model': str(msg.distortion_model),
            'D': str(list(msg.D)),
            'K': str(list(msg.K)),
            'R': str(list(msg.R)),
            'P': str(list(msg.P)),
            'binning_x': str(msg.binning_x),
            'binning_y': str(msg.binning_y),
            'roi': parse_sensor_msgs_region_of_interest(msg.roi)
        }
    }


def parse_sensor_msgs_image(msg, msg_date_time, result_folder):
    data_folder = os.path.join(result_folder, 'sensor_msgs_image')
    img_name = 'img' + str(msg.header.stamp) + '.jpeg'
    img_file = os.path.join(data_folder, img_name)
    mkdir_if_not_exist(img_file)
    Image.frombytes('RGB', (msg.width, msg.height), bytes(msg.data)).save(img_file, "JPEG")

    return {
        'folder': data_folder,
        'data': {
            'date_time': msg_date_time,
            'header': parse_std_msgs_header(msg.header),
            'height': str(msg.height),
            'width': str(msg.width),
            'encoding': str(msg.encoding),
            'is_bigendian': str(msg.is_bigendian),
            'step': str(msg.step),
            '__data': img_name
        }
    }


def parse_sensor_msgs_laser_scan(msg, msg_date_time, result_folder):
    return {
        'folder': os.path.join(result_folder, 'sensor_msgs_laser_scan'),
        'data': {
            'date_time': msg_date_time,
            'header': parse_std_msgs_header(msg.header),
            'angle_min': str(msg.angle_min),
            'angle_max': str(msg.angle_max),
            'angle_increment': str(msg.angle_increment),
            'time_increment': str(msg.time_increment),
            'scan_time': str(msg.scan_time),
            'range_min': str(msg.range_min),
            'range_max': str(msg.range_max),
            'ranges': str(list(msg.ranges)),
            'intensities': str(list(msg.intensities))
        }
    }


def parse_sensor_msgs_imu(msg, msg_date_time, result_folder):
    return {
        'folder': os.path.join(result_folder, 'sensor_msgs_imu'),
        'data': {
            'date_time': msg_date_time,
            'header': parse_std_msgs_header(msg.header),
            'orientation': parse_geometry_msgs_quaternion(msg.orientation),
            'orientation_covariance': str(list(msg.orientation_covariance)),
            'angular_velocity': parse_geometry_msgs_vector3(msg.angular_velocity),
            'angular_velocity_covariance': str(list(msg.angular_velocity_covariance)),
            'linear_acceleration': parse_geometry_msgs_vector3(msg.linear_acceleration),
            'linear_acceleration_covariance': str(list(msg.linear_acceleration_covariance)),
        }
    }


def parse_sensor_msgs_magnetic_field(msg, msg_date_time, result_folder):
    return {
        'folder': os.path.join(result_folder, 'sensor_msgs_magnetic_field'),
        'data': {
            'date_time': msg_date_time,
            'header': parse_std_msgs_header(msg.header),
            'magnetic_field': parse_geometry_msgs_vector3(msg.magnetic_field),
            'magnetic_field_covariance': str(list(msg.magnetic_field_covariance)),
        }
    }


parse_functions = {
    '90c7ef2dc6895d81024acba2ac42f369': parse_sensor_msgs_laser_scan,
    '060021388200f6f0f447d0fcd9c64743': parse_sensor_msgs_image,
    'c9a58c1b0b154e0e6da7578cb991d214': parse_sensor_msgs_camera_info,
    '6a62c6daae103f4ff57a132d6f95cec2': parse_sensor_msgs_imu,
    '2f3b0b43eed0c9501de0fa3ff89a45aa': parse_sensor_msgs_magnetic_field,
}
