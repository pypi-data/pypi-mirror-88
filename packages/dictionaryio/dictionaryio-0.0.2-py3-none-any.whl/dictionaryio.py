import sys

import requests
import vlc

author_name = 'Lucky Adogun'
LICENSE = 'MIT License'

class WordNotFoundError(Exception):
    pass

class SynonymsNotFoundError(Exception):
    pass


class DictionaryIO:

    """
    A simple wrapper class over https://dictionaryapi.dev/

    Usage: 

        word = DictionaryIO('happy') # replace `happy` with any word of your choice
        word.wordie # returns a string of the word. eg: 'happy'
        word.pronounce() # plays pronounciation of the word - requires exit with CTRL + C
        word.example() # returns a string making an example of the word
        word.meaning() # returns the meaning of the word
        word.synonyms() # returns a list of synonyms for the word
        word.figure_of_speech() # returns the figure of speech for the word
        word.phonetics() # returns the phonetics of the word

    """

    __obj = None

    def __init__(self, word):
        self._get_meaning(word)

    def _get_meaning(self, word):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        res = requests.get(url)
        if not res.status_code == 200:
            raise WordNotFoundError("Word not found. Try again")
        DictionaryIO.__obj = res.json()

    @property
    def wordie(self):
        return DictionaryIO.__obj[0]['word']

    def pronounce(self):
        voice = vlc.MediaPlayer(DictionaryIO.__obj[0]['phonetics'][0]['audio'])
        return voice.play()

    def example(self):
        return DictionaryIO.__obj[0]['meanings'][0]['definitions'][0]['example']

    def meaning(self):
        return DictionaryIO.__obj[0]['meanings'][0]['definitions'][0]['definition']

    def synonyms(self):
        try:
            return DictionaryIO.__obj[0]['meanings'][0]['definitions'][0]['synonyms']
        except KeyError:
            raise SynonymsNotFoundError('Synonyms not found')


    def figure_of_speech(self):
        return DictionaryIO.__obj[0]['meanings'][0]['partOfSpeech']

    def phonetics(self):
        return DictionaryIO.__obj[0]['phonetics'][0]['text']


        



