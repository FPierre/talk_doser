import codecs
import datetime
import re

class Doser2:
    def __init__(self, talk, people, stopwords, swearwords):
        self.talk = talk
        self.stopwords = stopwords
        self.swearwords = swearwords
        self.talk_line_number = 0
        self.data = {
            'talk': [],
            'dates': {},
            'days': {
                'Monday': 0,
                'Tuesday': 0,
                'Wednesday': 0,
                'Thursday': 0,
                'Friday': 0,
                'Saturday': 0,
                'Sunday': 0
            },
            'people': {},
            'swearwords': {},
            'words': []
        }

        for person in people:
            pseudo = person['pseudo']

            self.data['people'][pseudo] = {
                'pronounced_words': 0,
                'pronounced_swearwords': 0
            }

    def talk_lines(self):
        with codecs.open(self.talk, 'r', 'utf-8') as f:
            return [x.strip() for x in f.readlines()]

    def parse(self):
        for line in self.talk_lines():
            if len(line) == 0:
                continue

            if self.extract_date_time(line):
                continue

            line_without_date_time = line[20:]

            self.data['talk'].append({
                'line': line_without_date_time,
                'line_number': self.talk_line_number
            })

            self.talk_line_number += 1

            for pseudo in self.data['people']:
                # Expects that a sentence begin with a person pseudo
                if line_without_date_time.startswith(pseudo):
                    pseudo_length = len(pseudo) + 2
                    line_without_pseudo = line_without_date_time[pseudo_length:]

                    self.extract_words(pseudo, line_without_pseudo, self.talk_line_number)

                    continue

    def tokenize(self, text):
        # TODO: tokenize instead
        words = re.sub('[^\w]', ' ',  text).split()
        words = [w.lower() for w in words]

        return words

    def extract_date_time(self, line):
        date_time = re.match(r'^(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}) - ', line)

        if not date_time:
            return False

        date = date_time.group(1)
        time = date_time.group(2)

        self.extract_day(date)

        if date in self.data['dates']:
            self.data['dates'][date] = self.data['dates'][date] + 1
        else:
            self.data['dates'][date] = 1

    def extract_words(self, pseudo, line, talk_line_number):
        # TODO: remove dd/mm/YYYY, hh:mm - pseudo: <Fichier omis>
        words = self.tokenize(line)
        filtered_words = []

        for word in words:
            if word in self.stopwords or not word.isalpha() or len(word) <= 1:
                continue

            self.extract_stopword(pseudo, word, self.talk_line_number)
            # self.extract_swearword(pseudo, word)

    def extract_day(self, date):
        day = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%A')
        self.data['days'][day] = self.data['days'][day] + 1

    def extract_swearword(self, pseudo, word):
        if word in self.swearwords:
            if word in self.data['swearwords']:
                self.data['swearwords'][word]['count'] = self.data['swearwords'][word]['count'] + 1
            else:
                self.data['swearwords'][word] = {
                    'people': {},
                    'count': 1
                }

            if pseudo in self.data['swearwords'][word]['people']:
                self.data['swearwords'][word]['people'][pseudo] = self.data['swearwords'][word]['people'][pseudo] + 1
            else:
                self.data['swearwords'][word]['people'][pseudo] = 1

            self.data['people'][pseudo]['pronounced_swearwords'] = self.data['people'][pseudo]['pronounced_swearwords'] + 1

    def extract_stopword(self, pseudo, word, talk_line_number):
        word_match = next((l for l in self.data['words'] if l['word'] == word), None)

        if word_match == None:
            self.data['words'].append({
                'word': word,
                'count': 1,
                'people': []
            })

            # self.data['people'][pseudo]['pronounced_words'] = self.data['people'][pseudo]['pronounced_words'] + 1
        else:
            word_match['count'] += 1
            # word_match['people']['line_numbers'].append(talk_line_number)

            people_match = next((l for l in word_match['people'] if l['pseudo'] == pseudo), None)

            if people_match == None:
                word_match['people'].append({
                    'pseudo': pseudo,
                    'count': 1,
                    'line_numbers': [talk_line_number]
                })
            else:
                people_match['count'] += 1



        # if word in self.data['words']:
        #     word.count += 1
        #     # self.data['words'][word]['count'] += 1
        #     # word.people.
        #
        #     # self.data['words'][word]['count'] = self.data['words'][word]['count'] + 1
        #     # self.data['words'][word]['people']['line_numbers'].append(talk_line_number)
        # else:
        #     self.data['words'].append({
        #         'word': word,
        #         'count': 1,
        #         'people': [
        #             { 'line_numbers': [talk_line_number] }
        #         ]
        #     })


        # if pseudo in self.data['words'][word]['people']:
        #     self.data['words'][word]['people'][pseudo] = self.data['words'][word]['people'][pseudo] + 1
        # else:
        #     self.data['words'][word]['people'][pseudo] = 1
        #
        # self.data['people'][pseudo]['pronounced_words'] = self.data['people'][pseudo]['pronounced_words'] + 1

    # def sort_dates(self):
        # sorted_dates = [{ k: self.data['dates'][k] } for k in sorted(self.data['dates'], key = self.data['dates'].get, reverse = True)]
        # self.data['dates'] = sorted_dates

    def sort_words(self):
        sorted_words = [{ k: self.data['words'][k] } for k in sorted(self.data['words'], key = self.data['words'].get, reverse = True)]

        self.data['words'] = sorted_words

    # def sort_swearwords(self):

    def export(self):
        # self.sort_words()
        # print(sorted_words[0])
        # print(sorted_words[0][1])
        # print({ sorted_words[0][0]: sorted_words[0][1] })
        # print(type(sorted_words[0]))
        # print(dict((y, x) for x, y in sorted_words[0]))
        # print(dict(map(reversed, sorted_words[0])))
        # print(self.data['words'])
        return self.data
