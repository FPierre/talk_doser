import codecs
import json
import nltk
from nltk.corpus import stopwords
import re

def filter_stopwords(text, stopword_list):
    # TODO: tokenize instead
    # words = [w.lower() for w in text]
    words = re.sub("[^\w]", " ",  text).split()
    # print(words)

    # filtered_words = []
    #
    # for word in words:
    #     # Only add words that are not in the French stopwords list, are alphabetic, and are more than 1 character
    #     if word not in stopword_list and word.isalpha() and len(word) > 1:
    #         # Add word to filter_words list if it meets the above conditions
    #         filtered_words.append(word)
    #
    # filtered_words.sort()
    #
    # print(filtered_words)
    # return filtered_words
    return words

# get French stopwords from the nltk kit
def get_stopswords():
    # Create a list of all French stopwords
    # raw_stopword_list = stopwords.words('french')
    stopword_list = stopwords.words('french')
    # Make to decode the French stopwords as unicode objects rather than ascii
    # stopword_list = [word.decode('utf8') for word in raw_stopword_list]

    return stopword_list

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

data["words"] = {}

french_stopwords = get_stopswords()
# print(french_stopwords)

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

        for pseudo in data:
            # Expects that a sentence begin with a person pseudo
            if c.startswith(pseudo):
                z = len(pseudo) + 2
                c = c[z:]
                # data[pseudo]["sentences"].append(c)
                # print(c)

                stps = filter_stopwords(c, french_stopwords)
                # print(stps)

                for stp in stps:
                    if stp in data["words"]:
                        data["words"][stp] = data["words"][stp] + 1
                    else:
                        data["words"][stp] = 1

                # data[pseudo]["sentences"].append(c)

                continue

s = [{ k: data["words"][k] } for k in sorted(data["words"], key = data["words"].get, reverse = True)]

# for k, v in s:
#     k, v

data["words"] = s

# print(json.dumps(data["words"]))
# print(data["words"])

print(json.dumps(data))
