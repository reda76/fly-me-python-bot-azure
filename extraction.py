from dateutil.parser import parse
from price_parser import Price

from datetime import datetime
import re
import json



def result_to_json(result):
    try:
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
    except:
        luis_result = "None"

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
    
    
    try:
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
    except:
        pass
    
    liste_geo = []
    # Il peut y avoir plusieurs informations stockées dans la géographie
    # nous avons donc mis une condition si deux étaient trouvées
    try:
        if len(result["entities"]["geographyV2"]) > 1:
            liste_geo.append(result["entities"]["geographyV2"][0]["location"])
            liste_geo.append(result["entities"]["geographyV2"][1]["location"])
        else:
            liste_geo = result["entities"]["geographyV2"][0]["location"]
    except:
        liste_geo.append("None")
    dict_information["geography"] = liste_geo  
        
    liste_datetime_brute = []
    liste_datetime = []
    try:
        date_time_brute = result["entities"]["datetime"]
        # Le tuple est dans un string mais le contenu du tuple ne l'est pas
        # nous de devons donc ajouter des string à chaque élément
        for i in date_time_brute:
            i = i["timex"][0]
            i = re.sub(r"\(", "('", i)
            i = re.sub(r"\)", "')", i)
            i = re.sub(r",", "','", i)
            liste_datetime_brute.append(i)

        for date in liste_datetime_brute:
            try:
                date = eval(date)
            except:
                date = str(date)
            if type(date) is tuple:
                for i in date:
                    if len(date) != 0:
                        if i[0] != "P":
                            liste_datetime.append(parse_date(i).date())
            else:
                if isinstance(date, int) == False and len(date) != 0:
                    if date[0] != "P":
                        liste_datetime.append(parse_date(date).date())
    except:
        liste_datetime.append('None')
    dict_information["datetimeV2"] = liste_datetime
    
    try:
        dict_information["money"] = float(result["entities"]["money"][0]['number'])
    except:
        dict_information["money"] = 'None'
    
    # Replace les valeurs None de base par les valeurs prebuilt
    if dict_information["or_city"] == 'None':
        if type(dict_information['geography']) is list:
            try:
                dict_information["or_city"] = dict_information['geography'][1]
            except:
                pass
        
    if dict_information["dst_city"] == 'None':
        if type(dict_information['geography']) is list:
            dict_information["dst_city"] = dict_information['geography'][0]
        else:
            dict_information["dst_city"] = dict_information['geography']

    if dict_information["str_date"] == 'None':
        if type(dict_information['datetimeV2']) is list:
            dict_information["str_date"] = dict_information['datetimeV2'][0]
        else:
            dict_information["str_date"] = dict_information['datetimeV2']

    if dict_information["end_date"] == 'None':
        if type(dict_information['datetimeV2']) is list:
            try:
                dict_information["end_date"] = dict_information['datetimeV2'][1]
            except:
                pass

    if dict_information["budget"] == 'None':
        dict_information["budget"] = dict_information['money']
    
    return dict_information


def message_si_manque_info(dict_information):
    origine = dict_information["or_city"]
    destination = dict_information["dst_city"]
    start_date = dict_information["str_date"]
    end_date = dict_information["end_date"]
    budget = dict_information["budget"]
    
    dict_info_sans_prebuilt = {"your origine city": origine, "your destination city": destination, 
                            "your start date": start_date, "your end date": end_date, 
                            "your budget": budget}
    liste_info_manque = []
    for key, value in dict_info_sans_prebuilt.items():
        if value =="None":
            liste_info_manque.append(key)

    if len(liste_info_manque) > 0:
        message = "Sorry but I did not understand the following information: "
    if len(liste_info_manque) == 1:
        for i in liste_info_manque:
            message += i
        message += ". Can you repeat it please?"
    if len(liste_info_manque) > 1:
        for i in liste_info_manque:
            if i == liste_info_manque[-1]:
                message += i
            else:
                message += i + ", "
        message += ". Can you repeat them please?"
        
    if len(liste_info_manque) == 0:
        message = f"Do you want to go to {destination} from {origine} on {start_date} to {end_date} for a budget of {budget} ? If yes say 'Yes' if not say 'No'."
        
    return message


def none_liste(dict_extract):
    origine = dict_extract["or_city"]
    destination = dict_extract["dst_city"]
    start_date = dict_extract["str_date"]
    end_date = dict_extract["end_date"]
    budget = dict_extract["budget"]

    dict_info_sans_prebuilt = {"or_city": origine, "dst_city": destination, 
                            "str_date": start_date, "end_date": end_date, 
                            "budget": budget}
    liste_info_manque = []
    for key, value in dict_info_sans_prebuilt.items():
        if value =="None":
            liste_info_manque.append(key)
            
    return liste_info_manque


def export_json(luis_result, luis_result_2, luis_result_3):
    now = datetime.now()
    list_result = []

    if luis_result != 'None':
        list_result.append(luis_result)
    
    if luis_result_2 != 'None':
        list_result.append(luis_result_2)
    
    if luis_result_3 != 'None':
        list_result.append(luis_result_3)
    
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    with open("data/"+dt_string+".json", "w") as final:
        json.dump(list_result, final)