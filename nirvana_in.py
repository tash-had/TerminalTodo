import sys
import os
import shutil
from send_req import *
from auth import get_login_creds, get_auth_token, AUTHTOKEN_FILE, CREDS_FILE

FILE_NAME = "nirvana_in.py"
commands = {
    "python nirvana_in.py --install": "Add 'nin' as a shell command",
    "nin --help": "Display a list of all commands",
    "nin INBOX_ITEM": "Adds INBOX_ITEM to your Nirvana Inbox",
    "nin --reset": "Resets data stored by NirvanaIn.py",
    "nin --uninstall": "Resets NirvanaIn.py and removes the shell command"
}

def get_shell_profile_path():
    base = os.path.expanduser("~/")
    zshrc = base + ".zshrc"
    if os.path.isfile(zshrc):
        return zshrc
    else:
        return base + ".bash_profile"

def get_current_path():
    return os.path.dirname(os.path.abspath(__file__) + "/" + FILE_NAME)

def get_shell_profile_txt():
    return "alias nin='python " + get_current_path() + "'"

def reset():
    try:
        os.remove(AUTHTOKEN_FILE)
        os.remove(CREDS_FILE)
        shutil.rmtree("__pycache__")
    except OSError:
        pass

def install_shell_cmd():
    with open(get_shell_profile_path(), "a") as f:
        f.write("\n" + get_shell_profile_txt())
    print("'nin' command has been added to your shell. Restart your shell.")
    exit(0)

def uninstall_shell_cmd():
    def _delete_line(file, line):
        f = open(file,"r+")
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != line:
                f.write(i)
        f.truncate()
        f.close()
    _delete_line(get_shell_profile_path(), get_shell_profile_txt())
    reset() 
    print("NirvanaIn.py uninstalled. Restart your shell.")


def add_to_inbox(task):
    try:
        token = get_auth_token(get_login_creds())
        response = make_add_to_inbox_request(token, task)
        results = response["results"][0]
        if "task" not in results:
            print("An error occured.")
            print(results)
            if "error" in results:
                json.dumps(results, indent=4, sort_keys=True)
    except Exception as e:
        print("An error occurred")
        reset()
        show_err = input("See error log? y/n ")
        if (show_err == "y"):
            print(e)


if (len(sys.argv) <= 1):
    print("USAGE: nin INBOX_ITEM")
    print("Use 'nin --help' for a list of commands.")
    exit(1)
else:
    arg = sys.argv[1]
    if arg == "--help":
        print(json.dumps(commands, indent=4, sort_keys=True))
    elif arg == "--reset":
        reset()
    elif arg == "--install":
        install_shell_cmd()
    elif arg == "--uninstall":
        uninstall_shell_cmd()
    else:
        add_to_inbox(arg)
