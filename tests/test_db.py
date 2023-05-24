from kundi.server.main import Card, db_delete_cards, db_get_cards, db_create_cards

sample_email = "E8KaeUwdHVzsNkpdj3WY"


def test_get_cards():
    result = db_get_cards(sample_email, "1")
    expected = [{'word': ''}]
    assert result == expected


def test_create_cards():
    try:
        db_create_cards(sample_email, "2", [Card(
            card_id=2, word="go", definition="đi2")])
        assert True
    except:
        assert False


def test_delete_cards():
    try:
        db_create_cards(sample_email, "3", [Card(
            card_id=2, word="asdf", definition="asdkjsak")])
        db_delete_cards(sample_email, "3", [Card(
            card_id=2, word="asdf", definition="asdkjsak")])
        assert True
    except:
        assert False
