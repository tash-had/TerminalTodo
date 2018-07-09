import time
import requests
import uuid
import json


def make_login_request(u, p):
    url = "https://www.nirvanahq.com/api"

    querystring = {"api": "rest"}
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" + \
        "Content-Disposition: form-data; name=\"method\"\r\n\r\nauth.new\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" + \
        "Content-Disposition: form-data; name=\"u\"\r\n\r\n" + u + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" + \
        "Content-Disposition: form-data; name=\"p\"\r\n\r\n" + \
        p + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Cache-Control': "no-cache"
    }
    response = requests.request(
        "POST", url, data=payload, headers=headers, params=querystring)
    return json.loads(response.text)


def make_add_to_inbox_request(token, task, note):
    url = "https://focus.nirvanahq.com/api/"
    timestamp = str(int(time.time()))
    querystring = {
        "api": "json",
        "requestid": str(uuid.uuid4()),
        "clienttime": timestamp,
        "authtoken": token,
        "appid": "n2desktop",
        "appversion": "1525880921"
    }

    payload = [
        {
            "method": "task.save",
            "id": str(uuid.uuid4()),
            "name": task,
            "_name": timestamp,
            "note": note, 
            "_note": timestamp
        }
    ] 

    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache"
    }

    response = requests.request(
        "POST", url, data=json.dumps(payload), headers=headers, params=querystring)
    return json.loads(response.text)
