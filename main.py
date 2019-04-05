import re
import sys

import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.OfferData import OfferData

chromedriver_path = sys.argv[1]

options = Options()
options.headless = True
driver = webdriver.Chrome(chromedriver_path, options=options)

query_test = ['Palma-de-Mallorca', '1', '2019-04-20', '2019-04-30']


def get_offerts(query_neighborhood, query_adults, query_check_in, query_check_out):
    driver.get(
       'https://www.airbnb.es/s/' + query_neighborhood +
       '/homes?adults=' + query_adults +
       '&checkin=' + query_check_in +
       '&checkout=' + query_check_out
    )

    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup.findAll('div', id=re.compile('^listing-'))

offerts_soup_divs = get_offerts(*query_test)

for offer_soup_div in offerts_soup_divs:
    ho = OfferData(*query_test, offer_soup_div)
    attrs = vars(ho)
    print(', '.join("%s: %s" % item for item in attrs.items()))
