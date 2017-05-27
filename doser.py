import codecs
import json
import re

config_file = open("./secrets.json").read()
config = json.loads(config_file)

person_one_pseudo = config["people"][0]["pseudo"]
person_two_pseudo = config["people"][1]["pseudo"]

data = {}
data[person_one_pseudo] = {}
data[person_two_pseudo] = {}
data["other"] = {}

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

        for person in data:
            if c.startswith(person):
                z = len(person) + 2
                c = c[z:]
                data[person]["sentences"].append(c)

print(data)
