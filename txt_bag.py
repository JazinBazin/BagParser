import os
from utilites import mkdir_if_not_exist


def create_txt(messages):
    for message in messages:
        folder = message['folder']
        data = message['data']
        message_file = os.path.join(folder, 'data.txt')
        data_string = __convert_dict_to_str(data)
        mkdir_if_not_exist(message_file)
        with open(message_file, 'a') as message_file_obj:
            message_file_obj.write(data_string + '\n\n\n')


def __convert_dict_to_str(data, indent=0):
    result = ''
    for key, value in data.items():
        if isinstance(value, dict):
            result += ' ' * indent + key + ':\n' + __convert_dict_to_str(value, indent + 4)
        else:
            result += ' ' * indent + key + ': ' + value + '\n'
    return result
