import os
import json
from utilites import mkdir_if_not_exist


def create_json(messages):
    for message in messages:
        folder = message['folder']
        data = message['data']
        message_file = os.path.join(folder, 'data.json')
        data_string = json.dumps(data)
        mkdir_if_not_exist(message_file)
        with open(message_file, 'a') as message_file_obj:
            message_file_obj.write(data_string)
