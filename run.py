import os

from csv import DictReader

from gtts import gTTS

LANGUAGES = {'en', 'fr'}

def load_csv(path='data.csv', delimiter=','):
    with open(path, 'r') as csvfile:
        reader = DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            yield row

def process(row, lang):
    tts = gTTS(row['text_{}'.format(lang)], lang=lang)
    path = os.path.join('output', row['file_id_{}'.format(lang)])
    tts.save(path)


def main():
    for row in load_csv():
        print(row['text_id'])
        for lang in LANGUAGES:
            process(row, lang)


if __name__ == '__main__':
    main()
