import re
import json

from botbuilder.core import TurnContext,ActivityHandler
from botbuilder.ai.luis import LuisApplication,LuisRecognizer, LuisRecognizerOptionsV3

from config import DefaultConfig
from extraction import extract, result_to_json

CONFIG = DefaultConfig()

app_id = CONFIG.APP_ID

appAuthoring_Key = CONFIG.APP_AUTHORING_KEY
endpointAuthoring_url = CONFIG.ENDPOINT_AUTHORING_URL

appPrediction_Key = CONFIG.APP_PREDICTION_KEY
endpointPrediction_url =CONFIG.ENDPOINT_PREDICTION_URL

class LuisBot(ActivityHandler):
    def __init__(self):
        luis_app = LuisApplication(app_id, appPrediction_Key, endpointPrediction_url)
        luis_option = LuisRecognizerOptionsV3(include_all_intents=False,include_instance_data=False)
        self.LuisReg = LuisRecognizer(luis_app,luis_option,True)


    async def on_turn(self, turn_context:TurnContext):
        luis_result = await self.LuisReg.recognize(turn_context)
        intent = LuisRecognizer.top_intent(luis_result)

        # Nous avons besoin de modifier une valeur, le dictionnaire return dans la valeur de la clé "Booking" ceci :
        # <botbuilder.core.intent_score.IntentScore object at 0x000001C516A00910>, et renvoie donc une erreur de syntaxe
        # Nous devons donc rentre le dictionnaire en string, et ajouté des strings à cette partie pour avoir un dictionnaire normal
        luis_result = result_to_json(luis_result)
        print(luis_result)
        dict_extract = extract(luis_result)

        origine = dict_extract["or_city"]
        destination = dict_extract["dst_city"]
        start_date = dict_extract["str_date"]
        end_date = dict_extract["end_date"]
        budget = dict_extract["budget"]
        datetimeV = dict_extract["datetimeV2"]
        geographyV = dict_extract["geography"]
        money = dict_extract["money"]

        await turn_context.send_activity(f"Do you want to go to {destination} from {origine} on {start_date} to {end_date} for a budget of {budget} ?")