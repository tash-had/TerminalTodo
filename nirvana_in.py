import sys
import os
import shutil
import json

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import get_config, create_config_file, remove_config_file, get_shell_profile_path, config_file_exists
from network_error_handler import remove_offline_store, store_offline_if_no_network, submit_offline_store


commands = {
    "python nirvana_in.py --install": "Add 'nin' as a shell command",
    "nin --help": "Display a list of all commands",
    "nin INBOX_ITEM": "Adds INBOX_ITEM to your Nirvana Inbox",
    "nin INBOX_ITEM // NOTE": "Adds an inbox item with a note",
    "nin --refresh": "Submits all inbox items that were added offline",
    "nin --reset": "Resets data stored by NirvanaIn.py",
    "nin --uninstall": "Resets NirvanaIn.py and removes the shell command"
}

FILE_NAME = "nirvana_in.py"

class InboxService:
    def __init__(self, nin_service):
        self.nin_service = nin_service

    def add_to_inbox(self, task, note, suppress_error=False, from_offline_store=False):
        config = get_config()
        api_key, sender_email, inbox_addr = config["api_key"], config["sender_email"], config["inbox_addr"]

        # sendgrid won't send emails with no content. if note is empty, make it a single space.
        note = " " if (note is None or len(note) == 0) else note
        message = Mail(
            from_email=sender_email,
            to_emails=inbox_addr,
            subject=task,
            plain_text_content=note)
        
        # Terminate if no network connection (and keep task/note in offline store if it isn't already there)
        store_offline_if_no_network(task, note, from_offline_store)
        
        if not from_offline_store:
            # If this submission is not from the offline store, submit the items remaining in our offline store.
            submit_offline_store(self)

        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            if response is None or str(response.status_code)[0] != "2":
                print("An error occured.")
                print("STATUS CODE", response.status_code)
                print("BODY", response.body)
                print("HEADERS", response.headers)
                return False
    
            return True
        except Exception as e:
            if not suppress_error:
                print("An error occurred. If the issue persists, try nin --reset")
                show_err = input("See error log? y/n ")
                if (show_err == "y"):
                    print(e)
            return False

class NirvanaInService:
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
        shell_profile_path = get_shell_profile_path()

        with open(shell_profile_path, "a") as f:
            f.write("\n" + self.get_shell_profile_txt())
        print("'nin' command has been added to your shell.")

    def uninstall_shell_cmd(self, uninstalled_msg=True):
        def _delete_line(file, prefix):
            f = open(file, "r+")
            d = f.readlines()
            f.seek(0)

            for i in d:
                if not i.startswith(prefix):
                    f.write(i)
            f.truncate()
            f.close()
        
        if config_file_exists():
            # if the config file doesn't exist, calling get_shell_profile_path will trigger the setup process.
            # don't wanna go thru a setup during unintallation
            # so we'll just remove the shell command during installation.
            _delete_line(get_shell_profile_path(), "alias nin")
            self.reset(force=True)
        remove_offline_store()

        if uninstalled_msg:
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
        # uninstall if it already exists
        nin_service.uninstall_shell_cmd(uninstalled_msg=False)
        print("Starting setup...")
        create_config_file()
        nin_service.install_shell_cmd()
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



