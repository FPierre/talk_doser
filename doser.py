import codecs
import re

class Doser:
    def __init__(self, file_name, people, stopwords, swearwords):
        self.file_name = file_name
        self.stopwords = stopwords
        self.swearwords = swearwords

        self.data = {}
        self.data["words"] = {}
        self.data["swearwords"] = {}
        self.data["dates"] = {}

        for person in people:
            pseudo = person["pseudo"]
            self.data[pseudo] = {}
            self.data[pseudo]["sentences"] = []

    def parse(self):
        with codecs.open(self.file_name, "r", "utf-8") as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]

            for line in lines:
                if len(line) == 0:
                    continue

                if self.extract_date_time(line):
                    continue

                line_without_date_time = line[20:]

                for pseudo in self.data:
                    # Expects that a sentence begin with a person pseudo
                    if line_without_date_time.startswith(pseudo):
                        pseudo_length = len(pseudo) + 2
                        line_without_pseudo = line_without_date_time[pseudo_length:]

                        self.data[pseudo]["sentences"].append(line_without_pseudo)

                        self.extract_words(pseudo, line_without_pseudo)

                        continue

    def tokenize(self, text):
        # TODO: tokenize instead
        words = re.sub("[^\w]", " ",  text).split()
        words = [w.lower() for w in words]

        return words

    # def stem(self, word):
    #     regexp = r'^(.*?)(é|er|era|erait|erais|eront|ation|ait|)?$'
    #     stem, suffix = re.findall(regexp, word)[0]
    #
    #     return stem

        # for suffix in ["ait", "ation", "é", "er", "era", "erait", "eront"]:
        #     if word.endswith(suffix):
        #         return word[:-len(suffix)]

        # return word

    def extract_date_time(self, line):
        date_time = re.match(r"^(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}) - ", line)

        if not date_time:
            return False

        date = date_time.group(1)
        time = date_time.group(2)

        if date in self.data["dates"]:
            self.data["dates"][date] = self.data["dates"][date] + 1
        else:
            self.data["dates"][date] = 1

    def extract_words(self, pseudo, line):
        # TODO: remove dd/mm/YYYY, hh:mm - pseudo: <Fichier omis>
        words = self.tokenize(line)
        filtered_words = []

        for word in words:
            # word = self.stem(word)

            if word in self.stopwords or not word.isalpha() or len(word) <= 1:
                continue

            if word in self.data["words"]:
                self.data["words"][word]["count"] = self.data["words"][word]["count"] + 1
            else:
                self.data["words"][word] = {}
                self.data["words"][word]["people"] = {}
                self.data["words"][word]["count"] = 1

            if pseudo in self.data["words"][word]["people"]:
                self.data["words"][word]["people"][pseudo] = self.data["words"][word]["people"][pseudo] + 1
            else:
                self.data["words"][word]["people"][pseudo] = 1

            if word in self.swearwords:
                if word in self.data["swearwords"]:
                    self.data["swearwords"][word]["count"] = self.data["swearwords"][word]["count"] + 1
                else:
                    self.data["swearwords"][word] = {}
                    self.data["swearwords"][word]["people"] = {}
                    self.data["swearwords"][word]["count"] = 1

                if pseudo in self.data["swearwords"][word]["people"]:
                    self.data["swearwords"][word]["people"][pseudo] = self.data["swearwords"][word]["people"][pseudo] + 1
                else:
                    self.data["swearwords"][word]["people"][pseudo] = 1

    def export(self):
        # sorted_words = [{ k: self.data["words"][k] } for k in sorted(self.data["words"], key = self.data["words"].get, reverse = True)]
        # sorted_words = sorted(self.data["words"].items(), key = lambda k: k[1]["count"], reverse = True)
        # self.data["words"] = sorted_words
        # print(sorted_words)
        # print(sorted_words[0])
        # print(sorted_words[0][1])
        # print({ sorted_words[0][0]: sorted_words[0][1] })
        # print(type(sorted_words[0]))
        # print(dict((y, x) for x, y in sorted_words[0]))
        # print(dict(map(reversed, sorted_words[0])))

        # sorted_dates = [{ k: self.data["dates"][k] } for k in sorted(self.data["dates"], key = self.data["dates"].get, reverse = True)]
        # self.data["dates"] = sorted_dates

        # print(self.data["words"])

        return self.data
