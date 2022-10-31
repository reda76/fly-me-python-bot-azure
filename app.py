from flask import Flask,request,Response
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings, TurnContext, ConversationState, MemoryStorage
import asyncio
from luisbot import LuisBot

import os

app = Flask(__name__)
loop = asyncio.get_event_loop()

microsoftAppId = os.environ.get('MICROSOFT_APP_ID')

botsettings = BotFrameworkAdapterSettings(microsoftAppId,"")
botadapter = BotFrameworkAdapter(botsettings)

CONMEMORY = ConversationState(MemoryStorage())
botdialog = LuisBot()

@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status = 415)

    # Json où contient les informations
    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await botdialog.on_turn(turncontext)

    task = loop.create_task(
        botadapter.process_activity(activity,auth_header,call_fun)
        )
    loop.run_until_complete(task)

if __name__ == '__main__':
    try:
        app.run_app(app, host='localhost', port=3978)
    except Exception as e:
        raise e