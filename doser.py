import codecs
import json
import re

config_file = open("./secrets.json").read()
config = json.loads(config_file)
# print(config)

person_one_pseudo = config["people"][0]["pseudo"]
person_two_pseudo = config["people"][1]["pseudo"]

gl = {}
gl[person_one_pseudo] = {}
gl[person_two_pseudo] = {}
gl["other"] = {}

gl[person_one_pseudo]["sentences"] = 0
gl[person_two_pseudo]["sentences"] = 0
gl["other"]["sentences"] = 0

with codecs.open(config["file"], "r", "utf-8") as f:
    lines = f.readlines()
    # Removes whitespace characters
    lines = [x.strip() for x in lines]

    for line in lines:
        # print(line)

        if 'str' in line:
            break

        t = re.match(r"^(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}) - ", line)
        date = t.group(1)
        time = t.group(2)
        # print(date)

        c = line[20:]
        # print(c)

        if c.startswith(person_one_pseudo):
            gl[person_one_pseudo]["sentences"] = gl[person_one_pseudo]["sentences"] + 1
        elif c.startswith(person_two_pseudo):
            gl[person_two_pseudo]["sentences"] = gl[person_two_pseudo]["sentences"] + 1
        else:
            gl["other"]["sentences"] = gl["other"]["sentences"] + 1

print(gl)
