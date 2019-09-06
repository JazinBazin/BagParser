import os
import xml.etree.ElementTree as ET
from utilites import mkdir_if_not_exist


def create_xml(messages):
    for message in messages:
        folder = message['folder']
        data = message['data']
        messages_file = os.path.join(folder, 'data.xml')
        if os.path.isfile(messages_file):
            tree = ET.parse(messages_file)
            root = tree.getroot()
            __append_data_to_root(root, data)
            tree.write(messages_file)
        else:
            root = ET.Element('data')
            __append_data_to_root(root, data)
            tree = ET.ElementTree(root)
            mkdir_if_not_exist(messages_file)
            tree.write(messages_file)


def __append_data_to_root(root, data):
    message = ET.SubElement(root, 'message')
    __create_xml_r(message, data)


def __create_xml_r(parent, data):
    for key, value in data.items():
        if key.startswith('__'):
            sub_element = ET.SubElement(parent, key[2:], attrib={'value': value})
        else:
            sub_element = ET.SubElement(parent, key)
            if isinstance(value, dict):
                __create_xml_r(sub_element, value)
            else:
                sub_element.text = str(value)
