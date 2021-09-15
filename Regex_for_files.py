import re

ticker_names_dollar = re.compile(r'^\$[a-zA-Z]{2}$ |^\$[a-zA-Z]{3}$ | ^\$[a-zA-Z]{4}$ | ^\$[a-zA-Z]{4}$ | ^\$[a-zA-Z]{5}$')



company_name_endings = {
    'technologies',
    'holding',
    'holdings',
    'inc.',
    'inc',
    'corporation'
}

def pull_good_words(word):

    if re.findall(ticker_names_dollar, word):
        return word
    elif company_name_endings:
        return word + word - 1


