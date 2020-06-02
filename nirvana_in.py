import sys
import os
import shutil
import json

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import get_config, remove_config_file
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
        config = get_config()
        api_key, sender_email, inbox_addr = config["api_key"], config["sender_email"], config["inbox_addr"]
    
        message = Mail(
            from_email=sender_email,
            to_emails=inbox_addr,
            subject=task,
            plain_text_content=note)

        if not from_offline_store:
            store_offline_if_no_network(task, note)

        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            if response is None or str(response.status_code)[0] != "2":
                print("An error occured.")
                print("STATUS CODE", response.status_code)
                print("BODY", response.body)
                print("HEADERS", response.headers)
                return False
            elif not from_offline_store:
                    submit_offline_store(self)
            return True
        except Exception as e:
            if not suppress_error:
                print("An error occurred. If the issue persists, try nin --reset")
                show_err = input("See error log? y/n ")
                if (show_err == "y"):
                    print(e)
            return False

class NirvanaInService:
    def get_shell_profile_path(self):
        base = os.path.expanduser("~/")
        shell_config = ""

        custom_shell = input("Are you using a shell other than bash or zsh as your default shell? y/n/idk ")
        is_custom_shell = custom_shell == "y"

        if is_custom_shell:
            print("Enter the full path to the config file of your default shell (ie. '.zshrc', '.bash_profile'")
            shell_config = input("Shell config file path: ")
        else:
            shell_config = base + ".zshrc"
            # if zshrc doesn't exist, default to bash_profile
            if not os.path.isfile(shell_config):
                shell_config = base + ".bash_profile"
    
        return shell_config

    def get_current_path(self):
        return os.path.dirname(os.path.abspath(__file__) + "/" + FILE_NAME)

    def get_shell_profile_txt(self):
        return "alias nin='python " + self.get_current_path() + "'"

    def reset(self, force=False):
        try:
            continue_reset = "y"
            if not force:
                continue_reset = input("WARNING: Resetting will remove your sendgrid api key, sendgrid sender email and nirvana inbox address from storage. Continue? y/n ")
            if continue_reset == "y":
                remove_config_file()
            shutil.rmtree("__pycache__")
        except OSError:
            pass

    def install_shell_cmd(self):
        with open(self.get_shell_profile_path(), "a") as f:
            f.write("\n" + self.get_shell_profile_txt())
        print("'nin' command has been added to your shell.")

    def uninstall_shell_cmd(self):
        def _delete_line(file, prefix):
            f = open(file, "r+")
            d = f.readlines()
            f.seek(0)

            for i in d:
                if not i.startswith(prefix):
                    f.write(i)
            f.truncate()
            f.close()
        _delete_line(self.get_shell_profile_path(), "alias nin")
        self.reset(force=True)
        remove_offline_store()
        print("NirvanaIn.py uninstalled. Restart your shell.")

if (len(sys.argv) <= 1):
    print("usage: nin INBOX_ITEM")
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
        print("Starting setup...")
        # Call get_sendgrid_config to trigger get_config in config.py (which requests user input for data)
        get_config()
        print("Install completed. Restart your shell.")
        exit(0)
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



