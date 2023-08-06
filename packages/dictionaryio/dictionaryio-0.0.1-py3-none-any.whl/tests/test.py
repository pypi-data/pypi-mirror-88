from dictionaryio import DictionaryIO

def test_response():
    word: DictionaryIO = DictionaryIO('car')
    assert type(word.wordie) == str

