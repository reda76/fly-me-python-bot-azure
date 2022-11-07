import extraction    # The code to test
import unittest   # The test framework
import numpy as np
from dateutil.parser import parse
import datetime

class Test_Testextraction(unittest.TestCase):
    def test_result_to_json(self):
        dict_json = "{'additional_properties': {}, 'text': 'IM IN TIJUANA FIND ME A FLIGHT TO CURITIBA AUG 27 TO SEPT 4 for a budget of 3500 dollars', 'altered_text': None, 'intents': {'Booking': <botbuilder.core.intent_score.IntentScore object at 0x000001A5577C08E0>}, 'entities': {'FlyOrder': [{'Fly': [{'or_city': ['TIJUANA'], 'dst_city': ['CURITIBA'], 'str_date': ['AUG 27'], 'end_date': ['SEPT 4'], 'budget': ['3500 dollars']}]}], 'geographyV2': [{'location': 'TIJUANA', 'type': 'city'}, {'location': 'CURITIBA', 'type': 'city'}], 'datetime': [{'timex': ['(XXXX-08-27,XXXX-09-04,P8D)'], 'type': 'daterange'}], 'money': [{'number': 3500, 'units': 'Dollar'}]}, 'properties': {}}"
        dict_json_resultat = {'additional_properties': {}, 
        'text': 'IM IN TIJUANA FIND ME A FLIGHT TO CURITIBA AUG 27 TO SEPT 4 for a budget of 3500 dollars', 
        'altered_text': None, 'intents': {'Booking': '<botbuilder.core.intent_score.IntentScore object at 0x000001A5577C08E0>'}, 
        'entities': {'FlyOrder': [{'Fly': [{'or_city': ['TIJUANA'], 'dst_city': ['CURITIBA'], 'str_date': ['AUG 27'], 
        'end_date': ['SEPT 4'], 'budget': ['3500 dollars']}]}], 'geographyV2': [{'location': 'TIJUANA', 'type': 'city'}, 
        {'location': 'CURITIBA', 'type': 'city'}], 'datetime': [{'timex': ['(XXXX-08-27,XXXX-09-04,P8D)'], 'type': 'daterange'}], 
        'money': [{'number': 3500, 'units': 'Dollar'}]}, 'properties': {}}
        self.assertEqual(extraction.result_to_json(dict_json), dict_json_resultat)

        list_none = ["", '', np.nan]
        for i in list_none:
            self.assertEqual(extraction.result_to_json(i), 'None')

    def test_parse_price(self):
        dict_test = {"3200 dollars": 3200, "5000": 5000, "145,000": 145000, "qfqf": 'None'}
        for price_string, price in dict_test.items():
            self.assertEqual(extraction.parse_price(price_string), price)

    def test_parse_date(self):
        dict_test = {"AUG 27": datetime.datetime(2022, 8, 27, 0, 0), 
                    "september": datetime.datetime(2022, 9, 7, 0, 0),
                    "15 may 2023": datetime.datetime(2023, 5, 15, 0, 0)}
        for key,value in dict_test.items():
            self.assertEqual(extraction.parse_date(key), value)
    
    def test_extract(self):
        dict_json = {'additional_properties': {}, 'text': 'IM IN TIJUANA FIND ME A FLIGHT TO CURITIBA AUG 27 TO SEPT 4 for a budget of 3500 dollars', 'altered_text': None, 'intents': {'Booking': '<botbuilder.core.intent_score.IntentScore object at 0x000001A5577C08E0>'}, 'entities': {'FlyOrder': [{'Fly': [{'or_city': ['TIJUANA'], 'dst_city': ['CURITIBA'], 'str_date': ['AUG 27'], 'end_date': ['SEPT 4'], 'budget': ['3500 dollars']}]}], 'geographyV2': [{'location': 'TIJUANA', 'type': 'city'}, {'location': 'CURITIBA', 'type': 'city'}], 'datetime': [{'timex': ['(XXXX-08-27,XXXX-09-04,P8D)'], 'type': 'daterange'}], 'money': [{'number': 3500, 'units': 'Dollar'}]}, 'properties': {}}
        dict_json_resultat = {'text': 'IM IN TIJUANA FIND ME A FLIGHT TO CURITIBA AUG 27 TO SEPT 4 for a budget of 3500 dollars', 'or_city': 'TIJUANA', 'dst_city': 'CURITIBA', 'str_date': datetime.date(2022, 8, 27), 'end_date': datetime.date(2022, 9, 4), 'budget': 3500.0, 'datetimeV2': [datetime.date(2022, 8, 27), datetime.date(2022, 9, 4)], 'geography': ['TIJUANA', 'CURITIBA'], 'money': 3500.0}
        self.assertEqual(extraction.extract(dict_json), dict_json_resultat)

    def test_message_si_manque_info(self):
        dict_extract_1 = {'text': 'IM IN TIJUANA FIND ME A FLIGHT TO CURITIBA AUG 27 TO SEPT 4 for a budget of 3500 dollars','or_city': 'TIJUANA','dst_city': 'CURITIBA','str_date': datetime.date(2022, 8, 27),'end_date': datetime.date(2022, 9, 4), 'budget': 3500.0, 'datetimeV2': [datetime.date(2022, 8, 27), datetime.date(2022, 9, 4)], 'geography': ['TIJUANA', 'CURITIBA'], 'money': 3500.0}
        dict_extract_2 = {'text': 'I would like to go from Dijon to Taiwan, but I only have 2000 dollars. My trip is from June the 9 to august the 10', 'or_city': 'None', 'dst_city': 'Taiwan', 'str_date': datetime.date(2022, 6, 9), 'end_date': datetime.date(2022, 8, 10), 'budget': 2000.0, 'datetimeV2': [datetime.date(2022, 6, 9), datetime.date(2022, 8, 10)], 'geography': 'Taiwan', 'money': 2000.0}
        dict_extract_3 = {'text': 'None', 'or_city': 'None', 'dst_city': 'None', 'str_date': 'None', 'end_date': 'None', 'budget': 'None', 'datetimeV2': 'None', 'geography': 'None', 'money': 'None'}
        message_1 = "Do you want to go to CURITIBA from TIJUANA on 2022-08-27 to 2022-09-04 for a budget of 3500.0 ? If yes say 'Yes' if not say 'No'."
        message_2 = 'Sorry but I did not understand the following information: your origine city. Can you repeat it please?'
        message_3 = 'Sorry but I did not understand the following information: your origine city, your destination city, your start date, your end date, your budget. Can you repeat them please?'
        self.assertEqual(extraction.message_si_manque_info(dict_extract_1), message_1)
        self.assertEqual(extraction.message_si_manque_info(dict_extract_2), message_2)
        self.assertEqual(extraction.message_si_manque_info(dict_extract_3), message_3)

    def test_none_liste(self):
        dict_extract_1 = {'text': 'None', 'or_city': 'None', 'dst_city': 'None', 'str_date': 'None', 'end_date': 'None', 'budget': 'None', 'datetimeV2': 'None', 'geography': 'None', 'money': 'None'}
        dict_extract_2 = {'text': 'IM IN TIJUANA FIND ME A FLIGHT TO CURITIBA AUG 27 TO SEPT 4 for a budget of 3500 dollars', 'or_city': 'TIJUANA', 'dst_city': 'CURITIBA', 'str_date': datetime.date(2022, 8, 27), 'end_date': datetime.date(2022, 9, 4), 'budget': 3500.0, 'datetimeV2': [datetime.date(2022, 8, 27), datetime.date(2022, 9, 4)], 'geography': ['TIJUANA', 'CURITIBA'], 'money': 3500.0}
        list_none_1 = ['or_city', 'dst_city', 'str_date', 'end_date', 'budget']
        list_none_2 = []
        self.assertEqual(extraction.none_liste(dict_extract_1), list_none_1)
        self.assertEqual(extraction.none_liste(dict_extract_2), list_none_2)
    

if __name__ == '__main__':
    unittest.main()