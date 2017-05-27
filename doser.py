import codecs
import json
import re

config_file = open("./secrets.json").read()
config = json.loads(config_file)
# print(config)

person_one_pseudo = config["people"][0]["pseudo"]
person_two_pseudo = config["people"][1]["pseudo"]

data = {}
data[person_one_pseudo] = {}
data[person_two_pseudo] = {}
data["other"] = {}

data[person_one_pseudo]["sentences_quantity"] = 0
data[person_two_pseudo]["sentences_quantity"] = 0
data["other"]["sentences_quantity"] = 0

data[person_one_pseudo]["sentences"] = []
data[person_two_pseudo]["sentences"] = []
data["other"]["sentences"] = []

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
            data[person_one_pseudo]["sentences_quantity"] = data[person_one_pseudo]["sentences_quantity"] + 1

            data[person_one_pseudo]["sentences"].append(c)
        elif c.startswith(person_two_pseudo):
            data[person_two_pseudo]["sentences_quantity"] = data[person_two_pseudo]["sentences_quantity"] + 1

            data[person_two_pseudo]["sentences"].append(c)
        else:
            data["other"]["sentences_quantity"] = data["other"]["sentences_quantity"] + 1

            data["other"]["sentences"].append(c)
print(data)
