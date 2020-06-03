import urllib
import os, json
from config import FILE_PATH

OFFLINE_STORE_FILE = FILE_PATH + "/" + ".offline_store"

ERR_MSG_SUFFIX = "Will retry on your next 'nin'. To force retry, type 'nin --refresh'. If issue persists, try 'nin --reset'."
NETWORK_CONN_ERR_MSG = "No network connection detected. " + ERR_MSG_SUFFIX
HTTP_REQ_ERR_MSG = "An error has occured with the HTTP request. " + ERR_MSG_SUFFIX
GENERAL_ERR_MSG = "An error has occured. " + ERR_MSG_SUFFIX

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
                inbox_service.add_to_inbox(nin["task"], nin["note"], True)
        print("OFFLINE SUBMISSION SENT: Submitted", store_lst_len, "items from offline store.")
        os.remove(OFFLINE_STORE_FILE)
    else:
        if forced:
            print("No pending items found.")
            exit(1)

def remove_offline_store():
    if os.path.isfile(OFFLINE_STORE_FILE):
        os.remove(OFFLINE_STORE_FILE)

def handle_err(task, note, response_status=None, save_offline=True, force=False):
    terminate = False
    
    if force:
        print(GENERAL_ERR_MSG)
        terminate = True
    elif response_status is not None:
        if str(response_status)[0] != "2":
            print(HTTP_REQ_ERR_MSG)
            terminate = True
    elif not has_network_connection():
        print(NETWORK_CONN_ERR_MSG)
        terminate = True
    
    if terminate:
        if save_offline:
            store_for_later(task, note)
        exit(1)