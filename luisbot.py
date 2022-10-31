from botbuilder.core import TurnContext,ActivityHandler
from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer

import os

app_id = os.environ.get('APP_ID')

appAuthoring_Key = os.environ.get('APP_AUTHORING_KEY')
endpointAuthoring_url = os.environ.get('ENDPOINT_AUTHORING_URL')

appPrediction_Key = os.environ.get('APP_PREDICTION_KEY')
endpointPrediction_url = os.environ.get('ENDPOINT_PREDICTION_URL')

class LuisBot(ActivityHandler):
    def __init__(self):
        luis_app = LuisApplication(app_id, appPrediction_Key, endpointPrediction_url)
        luis_option = LuisPredictionOptions(include_all_intents=True,include_instance_data=True)
        self.LuisReg = LuisRecognizer(luis_app,luis_option,True)


    async def on_turn(self, turn_context:TurnContext):
        luis_result = await self.LuisReg.recognize(turn_context)
        intent = LuisRecognizer.top_intent(luis_result)
        await turn_context.send_activity(luis_result)
        print(luis_result.text)
        print()
        print(luis_result)