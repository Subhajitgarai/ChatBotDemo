import logging
from flask import current_app, jsonify
import json
import requests

# from app.services.openai_service import generate_response
import google.generativeai as genai
import re


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


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


def generate_response(response):
    # genai.configure(api_key="AIzaSyAViVijUjVY6ZrzDMEp_v0B2bUau3kF6YQ")

    # # Set up the model
    # generation_config = {
    #     "temperature": 0.9,
    #     "top_p": 1,
    #     "top_k": 1,
    #     "max_output_tokens": 2048,
    # }
    #
    # safety_settings = [
    #     {
    #         "category": "HARM_CATEGORY_HARASSMENT",
    #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #     },
    #     {
    #         "category": "HARM_CATEGORY_HATE_SPEECH",
    #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #     },
    #     {
    #         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #     },
    #     {
    #         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #     },
    # ]
    #
    # model = genai.GenerativeModel(model_name="gemini-1.0-pro",
    #                               generation_config=generation_config,
    #                               safety_settings=safety_settings)
    #
    # convo = model.start_chat(history=[
    # ])
    #
    # convo.send_message(response)
    # print(convo.last.text)
    # # Return text in uppercase
    # return convo.last.text

    knowledge_base = {
        "ok": "Thank You for your timing Have a greate day 😇",
        "who are you ?": "I am a ChatBot designed by Cbnits Engineers! ",
        "Who are you?":"I am a Rule based ChatBot designed by Cbnits Engineers! ",
        "disease": "*Get the Best Guidance for your Medical Disease*\n\nCan you pls tell us what kind of disease do you have then according to that we can pescribe you medicines 💊?",
        # "medicine": "*Get the Best Guidance for your Medical Disease*\n\nCan you pls tell us what kind of disease do you have then according to that we can pescribe you medicines 💊?",
        # "diet": "*Sample Diet Routine:*\n*Breakfast:*\n\n👉Oatmeal with sliced fruits (e.g., berries, banana)\n👉Greek yogurt with a sprinkle of nuts and seeds\n👉Green tea or black coffee\n*Mid-Morning Snack:*\n\n👉Handful of almonds or walnuts\n👉Fresh fruit (e.g., apple or pear)\n*Lunch:*\n\n👉Grilled chicken or tofu salad with mixed greens, cherry tomatoes, cucumbers, and a vinaigrette dressing\n👉Quinoa or brown rice on the side\n👉Water or herbal tea\n*Afternoon Snack:*\n\n👉Vegetable sticks (carrots, celery) with hummus\n👉Whole-grain crackers or rice cakes\n*Dinner:*\n\n👉Baked or grilled fish (salmon or tilapia) or a plant-based protein source (beans, lentils)\n👉Steamed or roasted vegetables (broccoli, Brussels sprouts, sweet potatoes)\n👉Quinoa or couscous\n👉Herbal tea or water\n*Evening Snack (if needed):*\n\n👉Low-fat Greek yogurt with a drizzle of honey\n👉Chamomile tea or a glass of warm milk\n*Important Tips:*\n\n👉Stay hydrated throughout the day by drinking plenty of water.\n👉Portion control is crucial; try to eat smaller, balanced meals more frequently.\n👉Include a variety of colorful fruits and vegetables for a range of nutrients.\n👉Choose whole grains over refined grains for added fiber and nutrients.\n👉Incorporate lean proteins, such as poultry, fish, tofu, or legumes.\n👉Limit processed foods, sugary snacks, and high-fat items.\n👉Remember, this is a general guideline, and individual dietary needs may vary. Consultation with a healthcare professional or a registered dietitian will help tailor a diet plan that suits your specific health goals and requirements.\n",
        # "support": "*Feel free to connect to our Customer Support by calling 📞+918942053525* \nThank You pls let me know do you have any other quires ? \nPls type *Hi* or *Hello* to see our available services.",
        "book_doctor": "*Fill this google form to book your desired doctor* \nhttps://www.linkedin.com/in/subhajit-garai-5808a3226/",
        "*book_doctor*": "*Fill this google form to book your desired doctor* \nhttps://www.linkedin.com/in/subhajit-garai-5808a3226/",
        # "doctor": "*What kind of doctors are you looking for?*\n\n🥼Cardiologist\n🥼Dermatologist\n🥼Orthopedic Surgeon\n🥼Gastroenterologist\n🥼Neurologist\n🥼Ophthalmologist\n🥼Obstetrician\n🥼Pediatrician\n🥼Pulmonologist\n🥼Urologist\n🥼Oncologist\n🥼Psychiatrist\n🥼Endocrinologist\n🥼Rheumatologist\n🥼Gynecologist",
        # "medicines": "*What kind of medicines are you looking for?*\n\n💊Aspirin\n💊Ibuprofen\n💊Acetaminophen\n💊Lisinopril\n💊Amoxicillin\n💊Atorvastatin\n💊Metformin\n💊Omeprazole\n💊Levothyroxine\n💊Simvastatin\n💊Hydrochlorothiazide\n💊Losartan\n💊Gabapentin\n💊Albuterol\n💊Warfarin\n💊Prednisone\n💊Ciprofloxacin\n💊Diazepam\n💊Fluoxetine\n💊Ranitidine"

    }
    medicine_base = {
        "cold": "Commonly used medicine for Common cold is *Cold Medicine A*\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "influenza": "Commonly used medicine for influenza is *Antiviral Medication B*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "hypertension": "Commonly used medicine for hypertension is *Hypertension Medication C*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "diabetes": "Commonly used medicine for diabetes is *Insulin D*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "migraine": "Commonly used medicine for migraine is *Pain Reliever E*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "asthma": "Commonly used medicine for asthma is *Bronchodilator F*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "arthritis": "Commonly used medicine for arthritis is *Anti-Inflammatory Medication G*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatement",
        "allergies": "Commonly used medicine for allergies is *Antihistamine H*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "digestive": "Commonly used medicine for digestive is *Antacid I*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment",
        "insomnia": "Commonly used medicine for insomnia is *Sleep Aid J*\n\n*Note:* Pls consult to doctor👨‍⚕️ once to get the best treatment"

    }
    diet_base = {
        "breakfast": "*Breakfast:*\n\n👉Oatmeal with sliced fruits (e.g., berries, banana)\n👉Greek yogurt with a sprinkle of nuts and seeds\n👉Green tea or black coffee\n*Mid-Morning Snack:*\n\n👉Handful of almonds or walnuts\n👉Fresh fruit (e.g., apple or pear)*Mid-Morning Snack:*\n\n👉Handful of almonds or walnuts\n👉Fresh fruit (e.g., apple or pear)",
        "lunch": "*Lunch:*\n\n👉Grilled chicken or tofu salad with mixed greens, cherry tomatoes, cucumbers, and a vinaigrette dressing\n👉Quinoa or brown rice on the side\n👉Water or herbal tea",
        "dinner": "*Afternoon Snack:*\n\n👉Vegetable sticks (carrots, celery) with hummus\n👉Whole-grain crackers or rice cakes\n*Dinner:*\n\n👉Baked or grilled fish (salmon or tilapia) or a plant-based protein source (beans, lentils)\n👉Steamed or roasted vegetables (broccoli, Brussels sprouts, sweet potatoes)\n👉Quinoa or couscous\n👉Herbal tea or water\n*Evening Snack (if needed):*\n\n👉Low-fat Greek yogurt with a drizzle of honey\n👉Chamomile tea or a glass of warm milk"
    }
    doctor_base = {
        "cardiologist": "Price for one session of Cardiologist👨‍⚕️ is 1000 \n\n If you want to Book click *Book_Doctor*",
        "dermatologist": "Price for one session of Dermatologist👨‍⚕️ is 500 \n\n If you want to Book click *Book_Doctor*",
        "orthopedic Surgeon": "Price for one session of Orthopedic👨‍⚕️ Surgeon is 3000\n\n If you want to Book click *Book_Doctor*",
        "gastroenterologist": "Price for one session of Gastroenterologist👨‍⚕️ is 900\n\n If you want to Book click *Book_Doctor*",
        "neurologist": "Price for one session of Neurologist👨‍⚕️ is 600\n\n If you want to Book click *Book_Doctor*",
        "ophthalmologist": "Price for one session of Ophthalmologist👨‍⚕️ is 800\n\n If you want to Book click *Book_Doctor*",
        "obstetrician": "Price for one session of Obstetrician👨‍⚕️ is 6900\n\n If you want to Book click *Book_Doctor*",
        "pediatrician": "Price for one session of Pediatrician👨‍⚕️ is 550\n\n If you want to Book click *Book_Doctor*",
        "pulmonologist": "Price for one session of Pulmonologist👨‍⚕️ is 1200\n\n If you want to Book click *Book_Doctor*",
        "urologist": "Price for one session of Urologist👨‍⚕️ is 1500\n\n If you want to Book click *Book_Doctor*",
        "oncologist": "Price for one session of Oncologist👨‍⚕️ is 2500\n\n If you want to Book click *Book_Doctor*",
        "psychiatrist": "Price for one session of Psychiatrist👨‍⚕️ is 800\n\n If you want to Book click *Book_Doctor*",
        "endocrinologist": "Price for one session of Endocrinologist👨‍⚕️ is 1100\n\n If you want to Book click *Book_Doctor*",
        "rheumatologist": "Price for one session of Rheumatologist👨‍⚕️ is 950\n\n If you want to Book click *Book_Doctor*",
        "gynecologist": "Price for one session of Gynecologist👨‍⚕️ is 1200\n\n If you want to Book click *Book_Doctor*",
        # Add more specialties as needed
    }
    medicine_price = {
        "aspirin": "*Price for Aspirin per pack is 5.99* \n\n To book medicine click *Book_Medicine*",
        "ibuprofen": "Price for Ibuprofen per pack is 7.50 \n\n To book medicine click *Book_Medicine*",
        "acetaminophen": "Price for Acetaminophen per pack is 4.25 \n\n To book medicine click *Book_Medicine*",
        "lisinopril": "Price for Lisinopril per pack is 12.99 \n\n To book medicine click *Book_Medicine*",
        "amoxicillin": "Price for Amoxicillin per pack is 15.75 \n\n To book medicine click *Book_Medicine*",
        "atorvastatin": "Price for Atorvastatin per pack is 18.50 \n\n To book medicine click *Book_Medicine*",
        "metformin": "Price for Metformin per pack is 9.99 \n\n To book medicine click *Book_Medicine*",
        "omeprazole": "Price for Omeprazole per pack is 6.75 \n\n To book medicine click *Book_Medicine*",
        "levothyroxine": "Price for Levothyroxine per pack is 8.99 \n\n To book medicine click *Book_Medicine*",
        "simvastatin": "Price for Simvastatin per pack is 14.25 \n\n To book medicine click *Book_Medicine*",
        "hydrochlorothiazide": "Price for Hydrochlorothiazide per pack is 10.50 \n\n To book medicine click *Book_Medicine*",
        "losartan": "Price for Losartan per pack is 11.75 \n\n To book medicine click *Book_Medicine*",
        "gabapentin": "Price for Gabapentin per pack is 20.99 \n\n To book medicine click *Book_Medicine*",
        "albuterol": "Price for Albuterol per pack is 15.50 \n\n To book medicine click *Book_Medicine*",
        "warfarin": "Price for Warfarin per pack is 3.99 \n\n To book medicine click *Book_Medicine*",
        "prednisone": "Price for Prednisone per pack is 9.25 \n\n To book medicine click *Book_Medicine*",
        "ciprofloxacin": "Price for Ciprofloxacin per pack is 12.99 \n\n To book medicine click *Book_Medicine*",
        "diazepam": "Price for Diazepam per pack is 22.50 \n\n To book medicine click *Book_Medicine*",
        "fluoxetine": "Price for Fluoxetine per pack is 7.99 \n\n To book medicine click *Book_Medicine*",
        "ranitidine": "Price for Ranitidine per pack is 5.50 \n\n To book medicine click *Book_Medicine*",
        # Add more medicine prices as needed
    }

    # Tokenize the response (using a simple split for demonstration)
    tokens = response.lower().split()
    f = 0

    # Check tokens in the knowledge base
    for token in tokens:
        if token in knowledge_base:
            f = 1
            # If a matching token is found, return the corresponding content
            return knowledge_base[token]
        elif token in medicine_base:
            f = 1
            custom_interactive_data = {
                'type': 'button',
                'body': {
                    'text': medicine_base[token],
                },
                'action': {
                    'buttons': [
                        {
                            'type': 'reply',
                            'reply': {
                                'id': 'but1',
                                'title': 'Book_Doctor',
                            },
                        },
                    ],
                },
            }
            send_button_message(custom_interactive_data)
            # return medicine_base[token]
        elif token == "medicines":
            f = 1
            messages1 = {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "Get the Best Service for your medicines and great price !!."
                },
                "body": {
                    "text": "\n\n*What kind of medicines are you looking for?*💊"
                },
                "action": {
                    "button": "Choose Medicine",
                    "sections": [
                        {
                            "title": "SECTION_1",
                            "rows": [
                                {"id": "16", "title": "Aspirin"},
                                {"id": "17", "title": "Ibuprofen"},
                                {"id": "8", "title": "Acetaminophen"},
                                {"id": "9", "title": "Lisinopril"},
                                {"id": "10", "title": "Amoxicillin"},
                                {"id": "11", "title": "Atorvastatin"},
                                {"id": "12", "title": "Metformin"},
                                {"id": "13", "title": "Omeprazole"},
                                {"id": "14", "title": "Levothyroxine"},
                                {"id": "15", "title": "Simvastatin"},
                            ]
                        }
                    ]
                }
            }
            send_list_messages(messages1)




        elif token == "medicine":
            f = 1
            messages1 = {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "Get the Best Guidance for your Medical Disease."
                },
                "body": {
                    "text": "\n\n*Can you pls tell us what kind of disease do you have then according to that we can pescribe you medicines ?*💊"
                },
                "action": {
                    "button": "Choose Your Disease",
                    "sections": [
                        {
                            "title": "SECTION_1",
                            "rows": [
                                {"id": "16", "title": "Cold"},
                                {"id": "17", "title": "Influenza"},
                                {"id": "8", "title": "Hypertension"},
                                {"id": "9", "title": "Diabetes"},
                                {"id": "10", "title": "Migraine"},
                                {"id": "11", "title": "Asthma"},
                                {"id": "12", "title": "Arthritis"},
                                {"id": "13", "title": "Allergies"},
                                {"id": "14", "title": "Digestive"},
                                {"id": "15", "title": "Insomnia"},
                            ]
                        }
                    ]
                }
            }
            send_list_messages(messages1)

        elif token in doctor_base:
            f = 1
            custom_interactive_data = {
                'type': 'button',
                'body': {
                    'text': doctor_base[token],
                },
                'action': {
                    'buttons': [
                        {
                            'type': 'reply',
                            'reply': {
                                'id': 'but1',
                                'title': 'Book_Doctor',
                            },
                        },
                    ],
                },
            }
            send_button_message(custom_interactive_data)
            # return doctor_base[token]

        elif token in medicine_price:
            f = 1
            f = 1
            custom_interactive_data = {
                'type': 'button',
                'body': {
                    'text': medicine_price[token],
                },
                'action': {
                    'buttons': [
                        {
                            'type': 'reply',
                            'reply': {
                                'id': 'but1',
                                'title': 'Book_Medicine',
                            },
                        },
                    ],
                },
            }
            send_button_message(custom_interactive_data)
        elif token == "doctor":
            f = 1
            messages1 = {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "What kind of doctors are you looking for?"
                },
                "body": {
                    "text": "*Here are our top doctor services we offer:*"
                },
                "action": {
                    "button": "Choose",
                    "sections": [
                        {
                            "title": "SECTION_1",
                            "rows": [
                                {"id": "6", "title": "Cardiologist"},
                                {"id": "7", "title": "Dermatologist"},
                                {"id": "8", "title": "Orthopedic Surgeon"},
                                {"id": "9", "title": "Gastroenterologist"},
                                {"id": "10", "title": "Neurologist"},
                                {"id": "11", "title": "Ophthalmologist"},
                                {"id": "12", "title": "Obstetrician"},
                                {"id": "13", "title": "Pediatrician"},
                                {"id": "14", "title": "Pulmonologist"},
                                {"id": "15", "title": "Urologist"},
                            ]
                        }
                    ]
                }
            }
            send_list_messages(messages1)
        elif token == "diet":
            f = 1
            custom_interactive_data = {
                'type': 'button',
                'body': {
                    'text': "*Sooo excited to see you here!* 🙂 \nTell me for what time of the day you want to choose get the diet plan\n\nClick any of the floowing time of the day :)",
                },
                'action': {
                    'buttons': [
                        {
                            'type': 'reply',
                            'reply': {
                                'id': 'but1',
                                'title': 'Breakfast',
                            },
                        },
                        {
                            'type': 'reply',
                            'reply': {
                                'id': 'but2',
                                'title': 'Lunch',
                            },
                        },
                        {
                            'type': 'reply',
                            'reply': {
                                'id': 'but3',
                                'title': 'Dinner',
                            },
                        },

                    ],
                },
            }
            send_button_message(custom_interactive_data)

    if response in knowledge_base:
        f = 1
        return knowledge_base[response]
    # For Hi and Hello
    if response.lower() == "hi" or response.lower() == "hello":
        f = 1
        messages1 = {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Namaste 🙏 "
            },
            "body": {
                "text": "*Welcome to Medical App Bot !* \n\n✅ Ready to explore ?\n\nLet's Know what's you looking for ?"
            },
            # "footer": {
            #     "text": "Let's Know what's you looking for ?"
            # },
            "action": {
                "button": "Categories",
                "sections": [
                    {
                        "title": "SECTION_1",
                        "rows": [
                            {
                                "id": "1",
                                "title": "Medicine Predictor",
                                # "description": "SECTION_1_ROW_1_DESCRIPTION"
                            },
                            {
                                "id": "2",
                                "title": "Book a Doctor",
                                # "description": "SECTION_1_ROW_2_DESCRIPTION"
                            },
                            {
                                "id": "3",
                                "title": "Diet Routine",
                                # "description": "SECTION_1_ROW_2_DESCRIPTION"
                            },
                            {
                                "id": "4",
                                "title": "Available Medicines",
                                # "description": "SECTION_1_ROW_2_DESCRIPTION"
                            },
                            {
                                "id": "5",
                                "title": "Support",
                                # "description": "SECTION_1_ROW_2_DESCRIPTION"
                            }
                        ]
                    }
                ]
            }
        }
        send_list_messages(messages1)
    if response.lower() in diet_base:
        return diet_base[response.lower()]
    if response.lower()=="book_medicine":
        f=1
        return "To book your desired medicines pls fill out the google form link\n\nTo Book:- https://github.com/Subhajitgarai?tab=repositories "
    if response.lower()=="support":
        f=1
        contact_data = {
            "name": {
                "formatted_name": "Customer Care",
                "first_name": "Customer",
                "last_name": "Care"
            },
            "phones": [
                {
                    "phone": "8942053525",
                    "type": "HOME"
                }
            ]
        }
        send_contact_message(contact_data)
        return "*If you have any quires you can contact to this following contact details*📞"
    if f == 0:
        custom_interactive_data = {
            'type': 'button',
            'body': {
                'text': "*Welcome to Medical Bot !*\n\nSooo excited to see you here! 🙂 \nTell us what is on your mind & we will help you as much as we can...\n\nLet's get started?\nClick Hi or Hello to Continue >",
            },
            'action': {
                'buttons': [
                    {
                        'type': 'reply',
                        'reply': {
                            'id': 'but1',
                            'title': 'Hi',
                        },
                    },
                    {
                        'type': 'reply',
                        'reply': {
                            'id': 'but2',
                            'title': 'Hello',
                        },
                    },
                ],
            },
        }

        # Call the function with the custom interactive data
        send_button_message(custom_interactive_data)
        # If no matching token is found, return a default response
        # return "Sorry, I didn't understand that you can press Hi or Hello to see our available services.\nThank You for being here 🙂"


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
            requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    # wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    # name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
    #
    # message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    # print("Message is ", message)
    # message_body = message["text"]["body"]
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = ""
    # Check the message type
    if message["type"] == "text":
        message_body = message["text"]["body"]
    elif message["type"] == "interactive" and "list_reply" in message["interactive"]:
        message_body = message["interactive"]["list_reply"]["title"]
    elif message["type"] == "interactive" and "button_reply" in message["interactive"]:
        message_body = message["interactive"]["button_reply"]["title"]
    else:
        # Handle other message types or log a warning
        logging.warning(f"Received message of unknown type: {message['type']}")
        message_body = ""

    # Now you can use message_body as needed
    print("Message body is", message_body)
    print("Message is =", message)

    # TODO: implement custom function here for uppercase
    response = generate_response(message_body)

    # OpenAI Integration
    # response = generate_response(message_body, wa_id, name)
    # response = process_text_for_whatsapp(response)

    # For Gemini Connect

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
            body.get("object")
            and body.get("entry")
            and body["entry"][0].get("changes")
            and body["entry"][0]["changes"][0].get("value")
            and body["entry"][0]["changes"][0]["value"].get("messages")
            and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )


# Trial List Message
def send_list_messages(messages):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/v19.0/{current_app.config['PHONE_NUMBER_ID']}/messages"

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "918942053525",
        "type": "interactive",
        "interactive": messages

    }

    try:
        response = requests.post(
            url, json=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except requests.RequestException as e:
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


# Send button messages with quick reply
def send_button_message(interactive_data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/v19.0/{current_app.config['PHONE_NUMBER_ID']}/messages"

    data = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': current_app.config['RECIPIENT_WAID'],  # Replace PHONE_NUMBER with the recipient's phone number
        'type': 'interactive',
        'interactive': interactive_data,
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        print("Button message sent successfully!")
        print(response.json())  # Optional: Print the response for debugging purposes
    except requests.exceptions.RequestException as e:
        print(f"Error sending button message: {e}")

# Sending Contact Messages
def send_contact_message(contact_data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/v19.0/{current_app.config['PHONE_NUMBER_ID']}/messages"

    data = {
        'messaging_product': 'whatsapp',
        'to': current_app.config['RECIPIENT_WAID'],  # Replace with the recipient's phone number
        'type': 'contacts',
        'contacts': [contact_data],
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        print("Contact message sent successfully!")
        print(response.json())  # Optional: Print the response for debugging purposes
    except requests.exceptions.RequestException as e:
        print(f"Error sending contact message: {e}")
