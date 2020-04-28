import os

from csv import DictReader

from gtts import gTTS

from pydub import AudioSegment

LANGUAGES = {'en', 'fr'}


def load_csv(path='data.csv', delimiter=','):
    with open(path, 'r') as csvfile:
        reader = DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            yield row


def process(row, lang):
    """text-to-speech to mp3 files in preprocessing folder"""
    tts = gTTS(row['text_{}'.format(lang)], lang=lang, lang_check=True)
    file_id = row['file_id_{}'.format(lang)]
    path = os.path.join('preprocess1', 'pre_' + file_id)
    tts.save(path)
    return path, file_id


def convert(path, file_id):
    """Convert to wav"""
    f = AudioSegment.from_mp3(path)
    f = f.set_channels(1)
    path = os.path.join('preprocess2', file_id)
    f.export(path, format='wav')
    return path, file_id


def standardize(path, file_id):
    """Standardize to voiceXML standard with `sox`"""
    output = os.path.join('output', file_id)
    cmd = ' '.join(['sox', path, '--rate 8k', '--bits 16', '--channels 1', '--encoding signed-integer', output])
    os.system(cmd)


def main():
    for i, row in enumerate(load_csv()):
        print("{} - {}".format(i, row['text_id']))
        for lang in LANGUAGES:
            path, file_id = process(row, lang)
            path, file_id = convert(path, file_id)
            standardize(path, file_id)


if __name__ == '__main__':
    main()
