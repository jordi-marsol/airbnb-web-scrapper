import re
import sys
import bs4
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromedriver_path = sys.argv[1]

options = Options()
options.headless = True
driver = webdriver.Chrome(chromedriver_path, options=options)

query_test = ['Palma-de-Mallorca', '1', '2019-04-20', '2019-04-30']


def search_airbnb (query_neighborhood, query_adults, query_check_in, query_check_out):
    driver.get(
       'https://www.airbnb.es/s/' + query_neighborhood +
       '/homes?adults=' + query_adults +
       '&checkin=' + query_check_in +
       '&checkout=' + query_check_out
    )

    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup.findAll('div', id=re.compile('^listing-'))


class House:
    def __init__(self, query_neighborhood, query_adults, query_check_in, query_check_out, house_div):

        self.query_neighborhood = query_neighborhood
        self.query_adults = query_adults
        self.query_check_in = query_check_in
        self.query_check_out = query_check_out

        def get_prices():
            not_formatted_prices = house_div.findAll(text=re.compile(r'\d€'))
            formatted_prices = list(map((lambda w: re.sub(r'[^\w]', ' ', w)), not_formatted_prices))
            return {
               'night_price': formatted_prices[0],
               'total_price': formatted_prices[1]
            }

        prices = get_prices()

        self.night_price = prices['night_price']
        self.total_price = prices['total_price']

        def get_num_for_feature(features_array, feature_regex):
            feature_item = next(filter(re.compile(feature_regex).match, features_array), '0')
            return re.match(r'^([\d|,]+)', feature_item).group(0)

        def get_num_features():
            features = house_div.findAll(text=re.compile(r'\d huésped|\d dormitorio|\d cama|\d baño'))
            return {
               'guest_num': get_num_for_feature(features, r'[+-]?([0-9]*[,])?[0-9]+ huésped'),
               'bedroom_num': get_num_for_feature(features, r'[+-]?([0-9]*[,])?[0-9]+ dormitorio'),
               'beds_num': get_num_for_feature(features, r'[+-]?([0-9]*[,])?[0-9]+ cama'),
               'bathroom_num': get_num_for_feature(features, r'[+-]?([0-9]*[,])?[0-9]+ baño')
            }

        num_features = get_num_features()

        self.guest_num = num_features['guest_num']
        self.bedroom_num = num_features['bedroom_num']
        self.beds_num = num_features['beds_num']
        self.bathroom_num = num_features['bathroom_num']

        def get_logical_features():
            features_list = house_div.findAll(text=re.compile(r'\b(Cocina|Wifi)\b'))
            return {
               'has_kitchen': 'Cocina' in features_list,
               'has_wifi': 'Wifi' in features_list
            }

        logical_features = get_logical_features()

        self.has_kitchen = logical_features['has_kitchen']
        self.has_wifi = logical_features['has_wifi']


houses = search_airbnb(*query_test)
rows = ''

for house in houses:
    ho = House(*query_test, house)
    attrs = vars(ho)
    #print(', '.join("%s: %s" % item for item in attrs.items()))
    rows = (attrs['query_neighborhood'] +','
    + attrs['query_adults'] +','
    + attrs['query_check_in'] +','
    + attrs['query_check_out'] +','
    + attrs['night_price'].strip() +','
    + attrs['total_price'].strip() +','
    + attrs['guest_num'] +','
    + attrs['bedroom_num'] +','
    + attrs['beds_num'] +','
    + attrs['bathroom_num'] +','
    + str(attrs['has_kitchen']) +','
    + str(attrs['has_wifi']) + '\r'
    + rows )

with open(time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv","w") as f:
        f.write('query_neighborhood,query_adults,query_check_in,query_check_out,night_price,total_price,guest_num,bedroom_num,beds_num,bathroom_num,has_kitchen,has_wifi' + '\r')
        f.write(rows)
        f.close()

driver.quit() #necessari per no deixar obert el chrome cada cop