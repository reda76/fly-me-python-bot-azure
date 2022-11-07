import os
from dotenv import load_dotenv

load_dotenv()

class DefaultConfig:
    """Bot Configuration"""

    APP_ID = os.environ.get("APP_ID")

    APP_AUTHORING_KEY = os.environ.get("APP_AUTHORING_KEY")

    ENDPOINT_AUTHORING_URL = os.environ.get("ENDPOINT_AUTHORING_URL")

    APP_PREDICTION_KEY = os.environ.get("APP_PREDICTION_KEY")

    ENDPOINT_PREDICTION_URL = os.environ.get("ENDPOINT_PREDICTION_URL")

    MICROSOFT_APP_ID = os.environ.get("MICROSOFT_APP_ID")
    MICROSOFT_APP_PSWD = os.environ.get("MICROSOFT_APP_PSWD")

    INSIGHT_INSTRUMENT_KEY = os.environ.get("INSIGHT_INSTRUMENT_KEY")
    INSIGHT_KEY = os.environ.get("INSIGHT_KEY")

    PORT = os.environ.get("PORT")