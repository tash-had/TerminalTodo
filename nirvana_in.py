import sys
import os
import shutil
from send_req import *
from auth import get_login_creds, get_auth_token, AUTHTOKEN_FILE, CREDS_FILE
from network_error_handler import remove_offline_store, store_offline_if_no_network, submit_offline_store

FILE_NAME = "nirvana_in.py"

commands = {
    "python nirvana_in.py --install": "Add 'nin' as a shell command",
    "nin --help": "Display a list of all commands",
    "nin INBOX_ITEM": "Adds INBOX_ITEM to your Nirvana Inbox",
    "nin INBOX_ITEM // NOTE": "Adds an inbox item with a note",
    "nin --refresh": "Submits all inbox items that were added offline",
    "nin --reset": "Resets data stored by NirvanaIn.py",
    "nin --uninstall": "Resets NirvanaIn.py and removes the shell command"
}

class InboxService:
    def __init__(self, nin_service):
        self.nin_service = nin_service

    def add_to_inbox(self, task, note, suppress_error=False, from_offline_store=False):
        try:
            store_offline_if_no_network(task, note)
            token = get_auth_token(get_login_creds())
            response = make_add_to_inbox_request(token, task, note)
            results = response["results"][0]
            if "task" not in results:
                print("An error occured.")
                print(results)
                if "error" in results:
                    json.dumps(results, indent=4, sort_keys=True)
                return False
            elif not from_offline_store:
                    submit_offline_store(self)
            return True
        except Exception as e:
            if not suppress_error:
                print("An error occurred")
                self.nin_service.reset()
                show_err = input("See error log? y/n ")
                if (show_err == "y"):
                    print(e)
            return False

class NirvanaInService:
    def get_shell_profile_path(self):
        base = os.path.expanduser("~/")
        zshrc = base + ".zshrc"
        if os.path.isfile(zshrc):
            return zshrc
        else:
            return base + ".bash_profile"


    def get_current_path(self):
        return os.path.dirname(os.path.abspath(__file__) + "/" + FILE_NAME)


    def get_shell_profile_txt(self):
        return "alias nin='python " + self.get_current_path() + "'"


    def reset(self):
        try:
            if os.path.isfile(AUTHTOKEN_FILE):
                os.remove(AUTHTOKEN_FILE)
            if os.path.isfile(CREDS_FILE):
                os.remove(CREDS_FILE)
            shutil.rmtree("__pycache__")
        except OSError:
            pass


    def install_shell_cmd(self):
        with open(self.get_shell_profile_path(), "a") as f:
            f.write("\n" + self.get_shell_profile_txt())
        print("'nin' command has been added to your shell. Restart your shell.")
        exit(0)


    def uninstall_shell_cmd(self):
        def _delete_line(file, line):
            f = open(file, "r+")
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i != line:
                    f.write(i)
            f.truncate()
            f.close()
        _delete_line(self.get_shell_profile_path(), self.get_shell_profile_txt())
        self.reset()
        remove_offline_store()
        print("NirvanaIn.py uninstalled. Restart your shell.")


if (len(sys.argv) <= 1):
    print("USAGE: nin INBOX_ITEM")
    print("Use 'nin --help' for a list of commands.")
    exit(1)
else:
    nin_service = NirvanaInService()
    inbox_service = InboxService(nin_service)

    arg = sys.argv[1]
    if arg == "--help":
        print(json.dumps(commands, indent=4, sort_keys=True))
    elif arg == "--reset":
        nin_service.reset()
    elif arg == "--install":
        nin_service.install_shell_cmd()
    elif arg == "--uninstall":
        nin_service.uninstall_shell_cmd()
    elif arg == "--refresh":
        submit_offline_store(inbox_service, True)
    elif len(arg) > 2 and arg[0:2] == "--":
        print("Invalid 'nin' command. Type 'nin --help' for a list of commands")
    else:
        task = arg
        note = ""
        record_as_note = False
        for i in range(2, len(sys.argv)):
            word = sys.argv[i]
            if word == "//":
                record_as_note = True
            elif record_as_note:
                note += " " 
                note += word
            else:
                task += " "
                task += word
        inbox_service.add_to_inbox(task, note)



