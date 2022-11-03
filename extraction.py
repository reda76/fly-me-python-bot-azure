from dateutil.parser import parse
from price_parser import Price

import datetime
import re


def result_to_json(result):
    luis_result = str(result)

    luis_result = re.sub(
            r">", 
            ">'", luis_result
        )

    luis_result = re.sub(
            r"<", 
            "'<", luis_result
        )
    luis_result = eval(luis_result)

    return luis_result

# Fonction de formatage des budgets et dates
def parse_price(price):
    try:
        price = Price.fromstring(price, decimal_separator=".")
        return price.amount_float
    except:
        return "None"

def parse_date(date):
    try:
        return parse(date, fuzzy_with_tokens=True)[0]
    except:
        return "None"

def extract(result):
    dict_information = {
            "text": "None",
            "or_city": "None",
            "dst_city": "None",
            "str_date": "None",
            "end_date": "None",
            "budget": "None",
            "datetimeV2": "None",
            "geography": "None",
            "money": "None"
            }
    
    dict_information["text"] = result["text"]
    
    list_information_fly = ["or_city", "dst_city", "str_date", "end_date", "budget"]
    
    dict_fly = result["entities"]["FlyOrder"][0]['Fly'][0]
    
    for inf_fly in list_information_fly:
        if inf_fly == "budget":
            try:
                dict_information[inf_fly] = parse_price(dict_fly[inf_fly][0])
            except:
                dict_information[inf_fly] = "None" 
        elif inf_fly == "str_date":
            try:
                dict_information[inf_fly] = parse_date(dict_fly[inf_fly][0]).date()
            except:
                dict_information[inf_fly] = "None"
        elif inf_fly == "end_date":
            try:
                dict_information[inf_fly] = parse_date(dict_fly[inf_fly][0]).date()
            except:
                dict_information[inf_fly] = "None"
        else:
            try:
                dict_information[inf_fly] = dict_fly[inf_fly][0]
            except:
                dict_information[inf_fly] = "None"
    
    liste_geo = []
    # Il peut y avoir plusieurs informations stockées dans la géographie
    # nous avons donc mis une condition si deux étaient trouvées
    if len(result["entities"]["geographyV2"]) > 1:
        liste_geo.append(result["entities"]["geographyV2"][0]["location"])
        liste_geo.append(result["entities"]["geographyV2"][1]["location"])
    else:
        liste_geo = result["entities"]["geographyV2"][0]["location"]
    dict_information["geography"] = liste_geo  
        
    liste_datetime = []
    date_time_brute = result["entities"]["datetime"][0]["timex"][0]
    
    # Le tuple est dans un string mais le contenu du tuple ne l'est pas
    # nous de devons donc ajouter des string à chaque élément
    date_time_brute = re.sub(r"\(", "('", date_time_brute)
    date_time_brute = re.sub(r"\)", "')", date_time_brute)
    date_time_brute = re.sub(r",", "','", date_time_brute)
    try:
        date_time_brute = eval(date_time_brute)
    except:
        date_time_brute = str(date_time_brute)
    if type(date_time_brute) is tuple:
        for i in date_time_brute:
            if len(date_time_brute) != 0:
                if i[0] != "P":
                    liste_datetime.append(parse_date(i).date())
    else:
        if len(date_time_brute) != 0:
            if date_time_brute[0] != "P":
                liste_datetime.append(parse_date(date_time_brute).date())
    dict_information["datetimeV2"] = liste_datetime
    
    dict_information["money"] = float(result["entities"]["money"][0]['number'])
    
    return dict_information