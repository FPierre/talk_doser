import codecs
import nltk
from nltk.corpus import stopwords
import re

class Doser:
    def __init__(self, file_name, people):
        self.file_name = file_name
        self.french_stopwords = self.get_stopswords()
        self.data = {}
        self.data["words"] = {}
        self.data["other"] = {}
        self.data["other"]["sentences"] = []

        for person in people:
            pseudo = person["pseudo"]
            self.data[pseudo] = {}
            self.data[pseudo]["sentences"] = []

    def filter_stopwords(self, text):
        # TODO: remove dd/mm/YYYY, hh:mm - pseudo: <Fichier omis>
        # TODO: tokenize instead
        # words = [w.lower() for w in text]
        words = re.sub("[^\w]", " ",  text).split()
        # print(words)

        filtered_words = []
        stopword_list = [
            "Fichier",
            "omis",
            "a",
            "à",
            "ai",
            "aller",
            "Alors",
            "as",
            "au",
            "aussi",
            "avais",
            "bon",
            "Bon",
            "ça",
            "ce",
            "contre",
            "dans",
            "de",
            "De",
            "Déjà",
            "des",
            "dire",
            "Dit",
            "dont",
            "du",
            "elle",
            "Elle",
            "elles",
            "en",
            "En",
            "est",
            "et",
            "Et",
            "fait",
            "faut",
            "ha",
            "Hé",
            "il",
            "j",
            "je",
            "Je",
            "l",
            "la",
            "La",
            "là",
            "le",
            "les",
            "Les",
            "lui",
            "ma",
            "mais",
            "Mais",
            "me",
            "même",
            "moi",
            "mon",
            "Non",
            "Ok",
            "on",
            "On",
            "par",
            "pas",
            "plus",
            "pour",
            "Pour",
            "qu",
            "quand",
            "que",
            "quelle",
            "qui",
            "qui",
            "quoi",
            "sais",
            "si",
            "suis",
            "sur",
            "te",
            "toi",
            "trop",
            "tu",
            "Tu",
            "un",
            "une",
            "va",
            "vais",
            "veux",
            "vous",
        ]

        for word in words:
            # Only add words that are not in the French stopwords list, are alphabetic, and are more than 1 character
            if word not in stopword_list and word.isalpha() and len(word) > 1:
                # Add word to filter_words list if it meets the above conditions
                filtered_words.append(word)

        filtered_words.sort()
        #
        # print(filtered_words)
        # return filtered_words
        return filtered_words

    def get_stopswords(self):
        # Create a list of all French stopwords
        # raw_stopword_list = stopwords.words('french')
        stopword_list = stopwords.words('french')
        # Make to decode the French stopwords as unicode objects rather than ascii
        # stopword_list = [word.decode('utf8') for word in raw_stopword_list]

        return stopword_list

    def parse(self):
        with codecs.open(self.file_name, "r", "utf-8") as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]

            for line in lines:
                # print(line)

                if 'str' in line:
                    break

                date_time = re.match(r"^(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}) - ", line)
                date = date_time.group(1)
                time = date_time.group(2)
                # print(date)

                line_without_date_time = line[20:]

                for pseudo in self.data:
                    # Expects that a sentence begin with a person pseudo
                    if line_without_date_time.startswith(pseudo):
                        pseudo_length = len(pseudo) + 2
                        line_without_pseudo = line_without_date_time[pseudo_length:]
                        # data[pseudo]["sentences"].append(line_without_pseudo)
                        # print(line_without_pseudo)

                        words = self.filter_stopwords(line_without_pseudo)
                        # print(words)

                        for word in words:
                            if word in self.data["words"]:
                                self.data["words"][word] = self.data["words"][word] + 1
                            else:
                                self.data["words"][word] = 1

                        # data[pseudo]["sentences"].append(line_without_pseudo)

                        continue

    def export(self):
        sorted_words = [{ k: self.data["words"][k] } for k in sorted(self.data["words"], key = self.data["words"].get, reverse = True)]
        self.data["words"] = sorted_words

        return self.data
