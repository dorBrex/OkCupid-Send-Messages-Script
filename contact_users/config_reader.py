import configparser
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
ini_file = os.path.join(current_folder, 'classes_and_xpaths.ini')


def read_ini(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)

    choose_from_queue = config['CLASS']['CHOOSE_FROM_QUEUE']
    inbox_is_full = config['CLASS']['INBOX_IS_FULL']

    message_box = config['XPATH']['MESSAGE_BOX']
    close_open_conversation = config['XPATH']['CLOSE_OPEN_CONVERSATION']
    close_finished_conversation = config['XPATH']['CLOSE_FINISHED_CONVERSATION']
    delete_liked_user = config['XPATH']['DELETE_LIKED_USER']
    last_user_talk_to_pop_up_messenger = config['XPATH']['LAST_USER_TALK_TO_POP_UP_MESSENGER']
    next_user = config['XPATH']['NEXT_USER']
    return {'choose_from_queue': choose_from_queue, 'inbox_is_full': inbox_is_full, 'message_box': message_box,
            'close_open_conversation': close_open_conversation,
            'close_finished_conversation':close_finished_conversation,
            'delete_liked_user': delete_liked_user,
            'last_user_talk_to_pop_up_messenger': last_user_talk_to_pop_up_messenger, 'next_user': next_user}


config = read_ini(ini_file)
