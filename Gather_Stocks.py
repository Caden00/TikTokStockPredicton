import Common_Words, requests, pprint
import re
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import date

# Open text file
def find_important_words():

    captial_word_regex = re.compile(r'^[A-Z]+')

    delete_list = Common_Words.common_words

    try:
        key_words = open('key_words.txt', 'a+')
    except:
        print('File does not exist')

    write = open('key_words.txt')

    with open(r'text_files/text_files2021-01-22johnnyonthestocks1.mp4.txt') as f:
        for line in f:
            for word in line.split():
                if word not in delete_list:
                    key_words.write(word + ' ')

    key_words.close()



def yahoo_finance_search(words):

    finance_url = 'https://finance.yahoo.com/quote/'

    request = requests.get(finance_url + words)

    print(request.status_code)

    soup_text = request.text

    soup = BeautifulSoup(soup_text, 'html.parser')

    if soup.findAll(class_='data-col0'):
        # Print that there are multiple
        print('Multiple search results')

        for search_result in soup.findAll('tbody', {'data-reactid':'54'}):
            rows = soup.findAll('td')
            information = [i.text for i in rows]

        ticker_names = []
        stock_names = []

        for i in range(len(information)):
            if (i % 6) == 0:
                ticker_names.append(information[i])
            elif (i - 1) % 6 == 0:
                stock_names.append(information[i])

        found_possibilities = '{} ({})'.format(stock_names[0], ticker_names[0])
        print('{} ({})'.format(stock_names[0], ticker_names[0]))

        return found_possibilities

    if soup.findAll(class_='D(ib) Fz(18px)'):
        # Print stocks
        print('Single stock found')

        # Write name of stock
        for hit in soup.findAll(class_='D(ib) Fz(18px)'):
            print(hit.text)
            return hit.text

    else:
        print('No data')
        return False



yahoo_finance_search('Ghive')





