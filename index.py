import os
import adbutils
import re
import hashlib
import json
import time

os.system("adb start-server")
input("Connect your devices and press enter")

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
d = adb.device()
RESOURCE_FOLDER = "/sdcard/Android/data/com.epidgames.trickcalrevive/files"

errors = []


def to_obj(path: str):
    global errors
    print(path)
    obj = {}
    ls_data = d.shell(f"ls -1F {path}")
    file_folder_list = ls_data.split("\n")
    if file_folder_list == [""]:
        return {}
    file_list = filter(lambda x: x[-1] != "/", file_folder_list)
    folder_list = filter(lambda x: x[-1] == "/", file_folder_list)
    for i in file_list:
        print(f"{path}/{i.replace('\\ ',' ')}")
        try:
            obj[i] = hashlib.md5(
                d.sync.read_bytes(f"{path}/{i.replace('\\ ',' ')}")
            ).hexdigest()
        except:
            errors.append(f"{path}/{i.replace('\\ ',' ')}")
    for i in folder_list:
        obj[i] = to_obj(f"{path}/{i[:-1].replace('\\ ',' ')}")
    return obj


with open(f"./dumps/{time.time()}.json", "w") as f:
    json.dump(to_obj(RESOURCE_FOLDER), f)
print(errors)
