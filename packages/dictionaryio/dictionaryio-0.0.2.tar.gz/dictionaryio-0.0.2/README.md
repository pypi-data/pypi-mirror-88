# DictionaryIO

DictionaryIO is an English Dictionary wrapper with voice-pronunciation.
## Installation

Use the package manager [pip](https://pypi.org/project/dictionaryio/0.0.1/) to install dictionaryio.

```bash
pip install dictionaryio
```

## Usage

```python
from dictionaryio import DictionaryIO

word = DictionaryIO('happy') # replace `happy` with any word of your choice
word.wordie # returns a string of the word. eg: 'happy'

#GET MEANING:
word.meaning() # returns the meaning of the word

#GET VOICE PRONUNCIATION:
word.pronounce() # plays pronounciation of the word - requires exit with CTRL + C

#GET EXAMPLE:
word.example() # returns a string making an example of the word

#OTHERS:
word.synonyms() # returns a list of synonyms for the word
word.figure_of_speech() # returns the figure of speech for the word
word.phonetics() # returns the phonetics of the word
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/luckyadogun/dictionaryIO/blob/master/LICENSE)