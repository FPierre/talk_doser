import codecs
import datetime
import re

class Doser:
    def __init__(self, talk, people, stop_words, swear_words):
        self.talk = talk
        self.stop_words = stop_words
        self.swear_words = swear_words
        self.talk_line_number = 0
        self.data = {
            'talk': {
                'words_count': 0,
                'lines': []
            },
            'dates': [],
            'days': {
                'Monday': 0,
                'Tuesday': 0,
                'Wednesday': 0,
                'Thursday': 0,
                'Friday': 0,
                'Saturday': 0,
                'Sunday': 0
            },
            'people': [],
            'swear_words': [],
            'words': []
        }

        for person in people:
            pseudo = person['pseudo']

            self.data['people'].append({
                'pseudo': pseudo,
                'pronounced_words': 0,
                'pronounced_swear_words': 0
            })

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

            self.data['talk']['lines'].append({
                'line': line_without_date_time,
                'line_number': self.talk_line_number
            })

            self.talk_line_number += 1

            for person in self.data['people']:
                pseudo = person['pseudo']

                # Expects that a sentence begin with a person pseudo
                if line_without_date_time.startswith(pseudo):
                    pseudo_length = len(pseudo) + 2
                    line_without_pseudo = line_without_date_time[pseudo_length:]

                    self.extract_words(pseudo, line_without_pseudo, self.talk_line_number)

                    continue

    def tokenize(self, text):
        # TODO: tokenize instead
        words = re.sub('[^\w]', ' ',  text).split()
        return [w.lower() for w in words]

    def extract_date_time(self, line):
        date_time_line = re.match(r'^(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}) - ', line)

        if not date_time_line:
            return False

        date_line = date_time_line.group(1)
        time_line = date_time_line.group(2)

        self.extract_day(date_line)

        date_line_match = next((d for d in self.data['dates'] if d['date'] == date_line), None)

        if date_line_match == None:
            self.data['dates'].append({
                'date': date_line,
                'count': 1
            })
        else:
            date_line_match['count'] += 1

    def extract_words(self, pseudo, line, talk_line_number):
        # TODO: remove dd/mm/YYYY, hh:mm - pseudo: <Fichier omis>
        words = self.tokenize(line)
        filtered_words = []

        for word in words:
            if word in self.stop_words or not word.isalpha() or len(word) <= 1:
                continue

            self.data['talk']['words_count'] += 1

            people_match = next((p for p in self.data['people'] if p['pseudo'] == pseudo), None)

            if people_match == None:
                print('ko')
            else:
                people_match['pronounced_words'] += 1

            self.extract_stopword(pseudo, word, self.talk_line_number)
            self.extract_swearword(pseudo, word)

    def extract_day(self, date):
        day = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%A')
        self.data['days'][day] += 1

    def extract_swearword(self, pseudo, word):
        if word in self.swear_words:
            if word in self.data['swear_words']:
                self.data['swear_words'][word]['count'] += 1
            else:
                self.data['swear_words'][word] = {
                    'people': [],
                    'count': 1
                }

            if pseudo in self.data['swear_words'][word]['people']:
                self.data['swear_words'][word]['people'][pseudo] += 1
            else:
                self.data['swear_words'][word]['people'][pseudo] = 1

            people_match = next((p for p in self.data['people'] if p['pseudo'] == pseudo), None)

            if people_match == None:
                print('ko')
            else:
                people_match['pronounced_swear_words'] += 1

    def extract_stopword(self, pseudo, word, talk_line_number):
        word_match = next((l for l in self.data['words'] if l['word'] == word), None)

        if word_match == None:
            self.data['words'].append({
                'word': word,
                'count': 1,
                'people': [
                    {
                        'pseudo': pseudo,
                        'count': 1,
                        'line_numbers': [talk_line_number]
                    }
                ]
            })
        else:
            word_match['count'] += 1
            # word_match['people']['line_numbers'].append(talk_line_number)

            people_match = next((p for p in word_match['people'] if p['pseudo'] == pseudo), None)

            if people_match == None:
                word_match['people'].append({
                    'pseudo': pseudo,
                    'count': 1,
                    'line_numbers': [talk_line_number]
                })
            else:
                people_match['count'] += 1

    # def sort_dates(self):
        # sorted_dates = [{ k: self.data['dates'][k] } for k in sorted(self.data['dates'], key = self.data['dates'].get, reverse = True)]
        # self.data['dates'] = sorted_dates

    def sort_words(self):
        sorted_words = [{ k: self.data['words'][k] } for k in sorted(self.data['words'], key = self.data['words'].get, reverse = True)]

        self.data['words'] = sorted_words

    # def sort_swear_words(self):

    def export(self):
        return self.data
