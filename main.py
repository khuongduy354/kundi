# import
def parse_import(source: str, wd_delim: str, card_delim: str):
    cards = source.split(card_delim)
    results = []
    for card in cards:
        word = card.split(wd_delim)[0]
        defi = card.split(wd_delim)[1]
        results.append({"word": word, "definition": defi})
    return results

# export


def parse_export(source: list[dict], wd_delim: str, card_delim: str):
    result = ""
    for card in source:
        col = card["word"]+wd_delim+card["definition"]
        result += col + card_delim
    # remove last card delim
    result = result.rstrip(card_delim)
    return result


def app():
    sample_input = "word1 def1\nword2 def2\nword3 def3"
    result1 = parse_import(sample_input, " ", "\n")
    print(result1)
    result2 = parse_export(result1, " ", "\n")
    print(result2)


if __name__ == "__main__":
    app()
