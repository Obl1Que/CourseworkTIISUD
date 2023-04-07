import random
import string
import os
import json


class logger:
    def __init__(self):
        self.log_c = readJSON("settings_glob.json")["log_c"]
        self.massive = []

    def add(self, _string, _type = "n"):
        self.massive.append(f"[{self.log_c}][{_type}] {_string}")
    def save(self, _path):
        save_log(_path, self.massive)
        self.massive.clear()
        self.log_c += 1
        data = readJSON("settings_glob.json")
        data["log_c"] += 1
        saveJSON("settings_glob.json", data)
def open_log(path):
    try:
        with open(os.path.abspath(path), encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"PATH не найден!\n{e}")
def save_log(path, new_log):
    try:
        with open(os.path.abspath(path), mode="a+", encoding="utf-8") as f:
            for _ in new_log:
                f.write(f"{_}\n")
    except Exception as e:
        print(e)

def readJSON(path):
    with open(os.path.abspath(path), encoding="utf-8") as f:
        return json.load(f)
def saveJSON(path, sdata):
    with open(os.path.abspath(path), mode="w", encoding="utf-8") as f:
        json.dump(sdata, f, indent=4)

def generate_string():
    this_string = ''

    for _ in range(random.randint(1, 100)):
        this_string += random.choice(list(string.ascii_lowercase + '0123456789'))

    return (this_string)

# log = logger()
# log.add("SELECT * FROM users")
# log.add("INSERT INTO users VALUES ('123', 2)")
# log.add("SELECT some_string FROM users")
# log.save("requests.log")