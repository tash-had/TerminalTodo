import json
import os.path

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = FILE_PATH + "/" + ".config"

def get_config():
    data = None
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            data = {
                "api_key": input("SendGrid API Key: "),
                "sender_email": input("SendGrid Sender Email: "),
                "inbox_addr": input("Nirvana Inbox Address: ")
            }
            json.dump(data, f)
    else:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
    return data

def remove_config_file():
    if os.path.isfile(CONFIG_FILE):
        os.remove(CONFIG_FILE)