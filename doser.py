import codecs
import re

class Doser:
    def __init__(self, file_name, people, stopwords):
        self.file_name = file_name
        self.stopwords = stopwords

        self.data = {}
        self.data["words"] = {}
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
                if 'str' in line:
                    break

                self.parse_date_time(line)

                line_without_date_time = line[20:]

                for pseudo in self.data:
                    # Expects that a sentence begin with a person pseudo
                    if line_without_date_time.startswith(pseudo):
                        pseudo_length = len(pseudo) + 2
                        line_without_pseudo = line_without_date_time[pseudo_length:]

                        self.data[pseudo]["sentences"].append(line_without_pseudo)

                        words = self.filter_stopwords(line_without_pseudo)

                        for word in words:
                            if word in self.data["words"]:
                                self.data["words"][word] = self.data["words"][word] + 1
                            else:
                                self.data["words"][word] = 1

                        continue

    def filter_stopwords(self, text):
        # TODO: remove dd/mm/YYYY, hh:mm - pseudo: <Fichier omis>
        # TODO: tokenize instead
        words = re.sub("[^\w]", " ",  text).split()
        words = [w.lower() for w in words]

        filtered_words = []

        for word in words:
            # Only add words that are not in the French stopwords list, are alphabetic, and are more than 1 character
            if word not in self.stopwords and word.isalpha() and len(word) > 1:
                filtered_words.append(word)

        filtered_words.sort()

        return filtered_words

    def parse_date_time(self, line):
        date_time = re.match(r"^(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}) - ", line)
        date = date_time.group(1)
        time = date_time.group(2)

        if date in self.data["dates"]:
            self.data["dates"][date] = self.data["dates"][date] + 1
        else:
            self.data["dates"][date] = 1

    def export(self):
        sorted_words = [{ k: self.data["words"][k] } for k in sorted(self.data["words"], key = self.data["words"].get, reverse = True)]
        self.data["words"] = sorted_words

        sorted_dates = [{ k: self.data["dates"][k] } for k in sorted(self.data["dates"], key = self.data["dates"].get, reverse = True)]
        self.data["dates"] = sorted_dates

        return self.data
