import re
import json

from botbuilder.core import TurnContext,ActivityHandler
from botbuilder.ai.luis import LuisApplication,LuisRecognizer, LuisRecognizerOptionsV3

from config import DefaultConfig
from extraction import extract, result_to_json, message_si_manque_info

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

        dict_extract = extract(luis_result)
        
        # 8 'None' indique que le message n'a pas été comprit par le bot
        count = 0
        for key, value in dict_extract.items():
            if key == 'geography':
                if value[0] == 'None':
                    count += 1
            elif value == 'None':
                count += 1

        if count == 8:
            message= "Sorry, I did not understand your request, can you repeat please?"
        else:
            message = message_si_manque_info(dict_extract)

        await turn_context.send_activity(message)