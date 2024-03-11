import sys
import os
from dotenv import load_dotenv
import logging


def load_configurations(app):
    load_dotenv()
    app.config["ACCESS_TOKEN"] = "EAAhqu1TtTwMBOZCV59jKVoZBV1r5uYhMXUFVYOMIqUIY9ZCnLneZA2vkFuHAJr5I9uXKJsK2JbaxBxQ2vWjYr6SryGkuyZB5e25NtHkGeZAAmPL3VvoVCxJwtJr0U5SIZCYAmEhumxR9wqg4YQECuNgCNYKbct17sJUYgGxnaltcOT7zZAwofiZCSjJgQQlMOmavzdHds0W9lZBnk4vKKt5lMZD"

    app.config["YOUR_PHONE_NUMBER"] = "+15550885343"
    app.config["APP_ID"] = "2369152629952259"
    app.config["APP_SECRET"] = "7dbccd52b8578cc636c58b7201fcae0f"
    app.config["RECIPIENT_WAID"] = "+918942053525"
    app.config["VERSION"] = "v19.0"
    app.config["PHONE_NUMBER_ID"] = "225908483946704"
    app.config["VERIFY_TOKEN"] = "1234"


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
