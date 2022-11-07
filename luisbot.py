from botbuilder.core import TurnContext,ActivityHandler, ConversationState, MessageFactory
from botbuilder.ai.luis import LuisApplication,LuisRecognizer, LuisRecognizerOptionsV3
from botbuilder.dialogs import DialogSet, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

from config import DefaultConfig
from extraction import extract, result_to_json, message_si_manque_info, none_liste

CONFIG = DefaultConfig()

app_id = CONFIG.APP_ID

appAuthoring_Key = CONFIG.APP_AUTHORING_KEY
endpointAuthoring_url = CONFIG.ENDPOINT_AUTHORING_URL

appPrediction_Key = CONFIG.APP_PREDICTION_KEY
endpointPrediction_url =CONFIG.ENDPOINT_PREDICTION_URL

key_insight_instrumentation = CONFIG.INSIGHT_INSTRUMENT_KEY

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey='+key_insight_instrumentation)
)

class LuisBot(ActivityHandler):
    def __init__(self, conversation:ConversationState):
        luis_app = LuisApplication(app_id, appPrediction_Key, endpointPrediction_url)
        luis_option = LuisRecognizerOptionsV3(include_all_intents=False,include_instance_data=False)
        self.LuisReg = LuisRecognizer(luis_app,luis_option,True)
        self.con_statea = conversation
        self.state_prop = self.con_statea.create_property("dialog_set")
        self.dialog_set = DialogSet(self.state_prop)
        self.dialog_set.add(TextPrompt("text_prompt"))
        self.dialog_set.add(WaterfallDialog("main_dialog", [self.GetBooking, self.Verification, self.VerificationDeux, self.VerificationTrois]))

    async def GetBooking(self, waterfall_step:WaterfallStepContext):
        return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=MessageFactory.text("Hello ! You can book your flight here, I'm listening.")))

    async def Verification(self, waterfall_step:WaterfallStepContext) -> DialogTurnResult:
        luis_result = await self.LuisReg.recognize(waterfall_step.context)
        # Nous avons besoin de modifier une valeur, le dictionnaire return dans la valeur de la clé "Booking" ceci :
        # <botbuilder.core.intent_score.IntentScore object at 0x000001C516A00910>, et renvoie donc une erreur de syntaxe
        # Nous devons donc rentre le dictionnaire en string, et ajouté des strings à cette partie pour avoir un dictionnaire normal
        luis_result = result_to_json(luis_result)
        waterfall_step.values["luis_result"] = luis_result
        dict_extract = extract(luis_result)
        waterfall_step.values["dict_extract"] = dict_extract
        # 8 'None' indique que le message n'a pas été comprit par le bot
        count = 0
        for key, value in dict_extract.items():
            if key == 'geography':
                if value[0] == 'None':
                    count += 1
            if key == 'datetimeV2':
                if value[0] == 'None':
                    count += 1
            elif value == 'None':
                count += 1

        if count == 8:
            message= "Sorry, I did not understand your request, can you repeat please?"
        else:
            message = message_si_manque_info(dict_extract)
        return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=MessageFactory.text(message)))


    async def VerificationDeux(self, waterfall_step:WaterfallStepContext) -> DialogTurnResult:
        luis_result_2 = await self.LuisReg.recognize(waterfall_step.context)
        luis_result = waterfall_step.values["luis_result"]

        dict_extract = waterfall_step.values["dict_extract"]
        luis_result_2 = result_to_json(luis_result_2)
        waterfall_step.values["luis_result_2"] = luis_result_2
        dict_extract_2 = extract(luis_result_2)

        liste_info_manque = none_liste(dict_extract)
        for i in liste_info_manque:
            dict_extract[i] = dict_extract_2[i]
        
        waterfall_step.values["dict_extract"] = dict_extract
        if luis_result_2["text"] in ['No', "no", "Nop", "nop", "Absolutely no", "Absolutely No", "absolutely no", "absolutely No"]:
            await waterfall_step._turn_context.send_activity("Sorry, we'll put you through to an advisor.")
            luis_result = waterfall_step.values["luis_result"]
            luis_result_2 = waterfall_step.values["luis_result_2"]
            # Renvoie à l'application Insight le json et le dictionnaire
            properties = {'custom_dimensions': {'turn': str([luis_result, luis_result_2]), 
            'information': str(dict_extract), 
            'reason': "The bot to propose a reservation that does not comply with the user's request"}}
            logger.warning('action', extra=properties)
        elif luis_result_2["text"] not in ['Yes', "yes", "yep", "Yep", "yeah", "Yeah"]:
            # 8 'None' indique que le message n'a pas été comprit par le bot
            count = 0
            for key, value in dict_extract.items():
                if key == 'geography':
                    if value[0] == 'None':
                        count += 1
                if key == 'datetimeV2':
                    if value[0] == 'None':
                        count += 1
                elif value == 'None':
                    count += 1

            if count == 8:
                message= "Sorry, I did not understand your request, can you repeat please?"
            else:
                message = message_si_manque_info(dict_extract)
            return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=MessageFactory.text(message)))
        else:
            await waterfall_step._turn_context.send_activity("Thank you !")
            return await waterfall_step.end_dialog()

    async def VerificationTrois(self, waterfall_step:WaterfallStepContext) -> DialogTurnResult:
        luis_result_3 = await self.LuisReg.recognize(waterfall_step.context)
        
        dict_extract = waterfall_step.values["dict_extract"]
        luis_result_3 = result_to_json(luis_result_3)
        waterfall_step.values["luis_result_3"] = luis_result_3
        dict_extract_3 = extract(luis_result_3)
    
        liste_info_manque = none_liste(dict_extract)
        for i in liste_info_manque:
            dict_extract[i] = dict_extract_3[i]
        
        waterfall_step.values["dict_extract"] = dict_extract
        if luis_result_3["text"] in ['No', "no", "Nop", "nop", "Absolutely no", "Absolutely No", "absolutely no", "absolutely No"]:
            await waterfall_step._turn_context.send_activity("Sorry, we'll put you through to an advisor.")
            luis_result = waterfall_step.values["luis_result"]
            luis_result_2 = waterfall_step.values["luis_result_2"]
            luis_result_3 = waterfall_step.values["luis_result_3"]
            # Renvoie à l'application Insight le json et le dictionnaire
            properties = {'custom_dimensions': {'turn': str([luis_result, luis_result_2, luis_result_3]), 
            'information': str(dict_extract), 
            'reason': "The bot to propose a reservation that does not comply with the user's request"}}
            logger.warning('action', extra=properties)
        elif luis_result_3["text"] not in ['Yes', "yes", "yep", "Yep", "yeah", "Yeah"]:
            count = 0
            for key, value in dict_extract.items():
                if key == 'geography':
                    if value[0] == 'None':
                        count += 1
                if key == 'datetimeV2':
                    if value[0] == 'None':
                        count += 1
                elif value == 'None':
                    count += 1
            if count != 0:
                message = "Sorry, we'll put you through to an advisor."
                luis_result = waterfall_step.values["luis_result"]
                luis_result_2 = waterfall_step.values["luis_result_2"]
                luis_result_3 = waterfall_step.values["luis_result_3"]
                properties = {'custom_dimensions': {'turn': str([luis_result, luis_result_2, luis_result_3]), 
                'information': str(dict_extract), 
                'reason': "The bot failed to understand the user's request after the 3rd exchange"}}
                logger.warning('action', extra=properties)
                return await waterfall_step.prompt("text_prompt", PromptOptions(prompt=MessageFactory.text(message)))   
        else:
            await waterfall_step._turn_context.send_activity("Thank you !")
            return await waterfall_step.end_dialog()

    async def on_turn(self, turn_context:TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if(dialog_context.active_dialog is not None):
            await dialog_context.continue_dialog()
        else:
            await dialog_context.begin_dialog("main_dialog")

        await self.con_statea.save_changes(turn_context)