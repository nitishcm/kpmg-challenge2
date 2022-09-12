import boto3.ec2
import requests
import json

dict = {}



def get_metadata(key):
    r = get_value(key)
    # check if multiple values in resp
    if r.status_code == 200 and r.text.__str__().find("\n") > 0:
        resparr = r.text.split("\n")
        for val in resparr:
            if val.find("/") > 0:
                get_metadata(key + val)
            else:
                resp = get_value(key + val)
                dict[key + val] = resp.text.__str__()
    else:
        if r.text.__str__().find("/") > 0:
            get_metadata(key + r.text.__str__())
        else:
            resp = get_value(key + r.text)
            if resp.status_code == 200:
                dict[key + r.text] = resp.text.__str__()

            else:
                dict[key] = r.text.__str__()


def get_value(key):
    base_url = "http://localhost:1338/latest/meta-data/" + key
    session = requests.Session()
    r = requests.get(base_url, timeout=(2, 5))
    return r


get_metadata("")
print(json.dumps(dict))
