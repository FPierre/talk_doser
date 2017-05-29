import codecs
import re

class Doser:
    def __init__(self, file_name, people):
        self.file_name = file_name
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
        words = re.sub("[^\w]", " ",  text).split()
        words = [w.lower() for w in words]
        # print(words)

        filtered_words = []
        stopword_list = [
            "a",
            "à",
            "ai",
            "aller",
            "alors",
            "as",
            "au",
            "auras",
            "aussi",
            "autre",
            "avais",
            "avez",
            "bas",
            "bon",
            "ça",
            "ce",
            "celle",
            "cette",
            "contre",
            "dans",
            "de",
            "déjà",
            "des",
            "devant",
            "dire",
            "dit",
            "doit",
            "dont",
            "du",
            "elle",
            "elles",
            "en",
            "encore",
            "es",
            "est",
            "et",
            "étaient",
            "étais",
            "être",
            "eu",
            "faire",
            "fait",
            "faut",
            "fichier",
            "fois",
            "ha",
            "hé",
            "https",
            "il",
            "j",
            "je",
            "jpg",
            "l",
            "la",
            "là",
            "le",
            "les",
            "leur",
            "lui",
            "ma",
            "mais",
            "me",
            "même",
            "mis",
            "moi",
            "mon",
            "Non",
            "ok",
            "omis",
            "on",
            "ou",
            "par",
            "parce",
            "pars",
            "pas",
            "peut",
            "plein",
            "plus",
            "pour",
            "qu",
            "quand",
            "que",
            "quelle",
            "qui",
            "quoi",
            "sais",
            "sans",
            "se",
            "sert",
            "si",
            "sont",
            "suis",
            "sur",
            "te",
            "toi",
            "ton",
            "tout",
            "trop",
            "tu",
            "un",
            "une",
            "va",
            "vais",
            "valait",
            "vers",
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
