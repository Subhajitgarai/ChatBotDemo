import json
from dotenv import load_dotenv
import os
import requests
import aiohttp
import asyncio

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()
ACCESS_TOKEN ="EAAhqu1TtTwMBOZCV59jKVoZBV1r5uYhMXUFVYOMIqUIY9ZCnLneZA2vkFuHAJr5I9uXKJsK2JbaxBxQ2vWjYr6SryGkuyZB5e25NtHkGeZAAmPL3VvoVCxJwtJr0U5SIZCYAmEhumxR9wqg4YQECuNgCNYKbct17sJUYgGxnaltcOT7zZAwofiZCSjJgQQlMOmavzdHds0W9lZBnk4vKKt5lMZD"
RECIPIENT_WAID = "+918942053525"
PHONE_NUMBER_ID = "225908483946704"
VERSION = "v19.0"

APP_ID = "2369152629952259"
APP_SECRET = "7dbccd52b8578cc636c58b7201fcae0f"


# --------------------------------------------------------------
# Send a template WhatsApp message
# --------------------------------------------------------------


def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response


# Call the function
response = send_whatsapp_message()
print(response.status_code)
print(response.json())
#
# # --------------------------------------------------------------
# # Send a custom text WhatsApp message
# # --------------------------------------------------------------
#
# # NOTE: First reply to the message from the user in WhatsApp!
#
#
def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Hello, this is a test message."
)

response = send_message(data)
print(response.json())

# # --------------------------------------------------------------
# # Send a custom text WhatsApp message asynchronously
# # --------------------------------------------------------------


# Does not work with Jupyter!
async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = "https://graph.facebook.com" + f"/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers["content-type"])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Hello, this is a test message."
)

loop = asyncio.get_event_loop()
loop.run_until_complete(send_message(data))
loop.close()
