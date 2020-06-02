import urllib
import os, json

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
OFFLINE_STORE_FILE = FILE_PATH + "/" + ".offline_store"

def no_network_err():
    print("No network connection detected. Will retry on your next 'nin'. To force retry, type 'nin --refresh'")
    exit(0)

def has_network_connection(host="http://google.com"):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def store_for_later(task, note):
    data = {
        "task": task,
        "note": note
    }
    if not os.path.isfile(OFFLINE_STORE_FILE):
        with open(OFFLINE_STORE_FILE, "w") as f:
            data = {
                "store": [
                    data
                ]
            }
            json.dump(data, f)
            f.close()
    else:
        with open(OFFLINE_STORE_FILE, "r+") as f:
            offline_store = json.load(f)
            offline_store["store"].append(data)
            f.seek(0)
            f.truncate()
            json.dump(offline_store, f)
            f.close()            
    return data

def submit_offline_store(inbox_service, forced=False):
    store_lst_len = 0
    if os.path.isfile(OFFLINE_STORE_FILE):
        with open(OFFLINE_STORE_FILE, "r") as f:
            offline_store_lst = json.load(f)["store"]
            store_lst_len = len(offline_store_lst)
            for nin in offline_store_lst:
                added = inbox_service.add_to_inbox(nin["task"], nin["note"], True, True)
                if added == False:
                    no_network_err()
                    exit(1)
        print("OFFLINE SUBMISSION SENT: Submitted", store_lst_len, "items from offline store.")
        os.remove(OFFLINE_STORE_FILE)
    else:
        if forced:
            print("No pending items found.")
            exit(1)

def remove_offline_store():
    if os.path.isfile(OFFLINE_STORE_FILE):
        os.remove(OFFLINE_STORE_FILE)

def store_offline_if_no_network(task, note, already_in_store=False):
    if not has_network_connection():
        if not already_in_store:
            store_for_later(task, note)
        no_network_err()
        exit(1)