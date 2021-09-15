import requests
import pprint

url_nasdaq ='https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
url_amex = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'
url_nyse = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'

headers = { "user-agent":"Mozilla"}

r = requests.get(url_nasdaq, headers=headers)



