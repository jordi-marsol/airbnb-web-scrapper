import re


class OfferData:
    def __init__(self, query_neighborhood, query_adults, query_check_in, query_check_out, offer_soup_div):

        self.query_neighborhood = query_neighborhood
        self.query_adults = query_adults
        self.query_check_in = query_check_in
        self.query_check_out = query_check_out

        def get_prices():
            not_formatted_prices = offer_soup_div.findAll(text=re.compile(r'\d€'))
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
            features = offer_soup_div.findAll(text=re.compile(r'\d huésped|\d dormitorio|\d cama|\d baño'))
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
            features_list = offer_soup_div.findAll(text=re.compile(r'\b(Cocina|Wifi)\b'))
            return {
               'has_kitchen': 'Cocina' in features_list,
               'has_wifi': 'Wifi' in features_list
            }

        logical_features = get_logical_features()

        self.has_kitchen = logical_features['has_kitchen']
        self.has_wifi = logical_features['has_wifi']
