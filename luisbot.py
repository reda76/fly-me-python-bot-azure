from botbuilder.core import TurnContext,ActivityHandler
from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer
from config import DefaultConfig
import os

CONFIG = DefaultConfig()

app_id = CONFIG.APP_ID

appAuthoring_Key = CONFIG.APP_AUTHORING_KEY
endpointAuthoring_url = CONFIG.ENDPOINT_AUTHORING_URL

appPrediction_Key = CONFIG.APP_PREDICTION_KEY
endpointPrediction_url =CONFIG.ENDPOINT_PREDICTION_URL

class LuisBot(ActivityHandler):
    def __init__(self):
        luis_app = LuisApplication(app_id, appPrediction_Key, endpointPrediction_url)
        luis_option = LuisPredictionOptions(include_all_intents=True,include_instance_data=True)
        self.LuisReg = LuisRecognizer(luis_app,luis_option,True)


    async def on_turn(self, turn_context:TurnContext):
        luis_result = await self.LuisReg.recognize(turn_context)
        intent = LuisRecognizer.top_intent(luis_result)
        await turn_context.send_activity(luis_result.text)
        print(luis_result.text)
        print()
        print(luis_result)