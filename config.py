import json
import os.path

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = FILE_PATH + "/" + ".config"
MAIN_FILE_NAME = "nirvana_in.py"

def get_config():
    data = None
    if not config_file_exists():
        print("Could not locate your config file.")
        create_config_file()
    else:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
    return data

def config_file_exists():
    return os.path.isfile(CONFIG_FILE)

def create_config_file():
    print("Creating a new config file.")
    shell_config_path = get_shell_profile_path(check_config=False) # set check_config to false to avoid infinite loop
    with open(CONFIG_FILE, "w") as f:
        data = {
            "shell_config_path": shell_config_path,
            "api_key": input("SendGrid API Key: "),
            "sender_email": input("SendGrid Sender Email: "),
            "inbox_addr": input("Nirvana Inbox Address: ")
        }
        json.dump(data, f)

def get_shell_profile_path(check_config=True):
    if check_config:
        config = get_config()
        if "shell_config_path" in config:
            return config["shell_config_path"]
        else:
            # remove config file if it exists 
            remove_config_file()
    
    base = os.path.expanduser("~/")
    shell_config = ""

    custom_shell = input("Are you using a shell other than bash or zsh as your default shell? y/n/idk ")
    is_custom_shell = custom_shell == "y"

    if is_custom_shell:
        print("Enter the full path to the configuration file of your default shell (ie. '.zshrc', '.bash_profile'")
        shell_config = input("Shell config file path: ")
    else:
        shell_config = base + ".zshrc"
        # if zshrc doesn't exist, default to bash_profile
        if not os.path.isfile(shell_config):
            shell_config = base + ".bash_profile"

    return shell_config

def remove_config_file():
    if os.path.isfile(CONFIG_FILE):
        os.remove(CONFIG_FILE)