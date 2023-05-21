from kundi.helpers import parse_export, parse_import

sample_input = "word1 def1\nword2 def2\nword3 def3"
listresult = parse_import(sample_input, " ", "\n")
stringresult = parse_export(listresult, " ", "\n")


def test_import():
    assert listresult == [{'word': 'word1', 'definition': 'def1'}, {
        'word': 'word2', 'definition': 'def2'}, {'word': 'word3', 'definition': 'def3'}]


def test_export():
    assert stringresult == "word1 def1\nword2 def2\nword3 def3"
