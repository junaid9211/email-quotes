# Sends a random quote to all of the people in email list

import os
import smtplib
from email.message import EmailMessage
import json
from random import choice

MY_EMAIL = os.environ['GMAIL1']
MY_PASSWORD = os.environ['GMAIL1_PASS']

GREET_EMOJIS = ['👏', '👋', '✌', '🤘', '👊', '🤟', '👌']
HEADING_EMOJIS = ['😎', '😉', '😁', '😼', '💯', '💪']

FOOTER = '''

Tomorrow I will shoot another great quote to your mailbox 🦊 





Interested in knowing how I did this? Well, I wrote ✍ a simple emailing 🐍 script and scheduled it on PythonAnywhere 👨‍💻 to run it every day, so that I don't have to run it manually. I have uploaded the script on my GitHub, you can find it here https://github.com/junaid9211/email-quotes. 😺 If you don't want to receive such emails, you can safely block me.

Thanks 👽

ps.
The purpose of this email was not to annoy you, I just wanted to test my python skills ‍💻'''


# get all qoutes
with open('quotes.json') as f:
    quotes = json.load(f)


# get email list
with open('email_list.json') as f:
    email_list = json.load(f)



with smtplib.SMTP_SSL('smtp.gmail.com', 465) as conn:
    conn.login(MY_EMAIL, MY_PASSWORD)


    for info in email_list:
        msg = EmailMessage()
        emoji1 = choice(GREET_EMOJIS)
        emoji2 = choice(HEADING_EMOJIS)
        msg['Subject'] = f"Hello, {info['name']} {emoji1}"
        msg['From'] = MY_EMAIL
        msg['To'] = info['email']
        quote = choice(quotes)
        content = f"Here's a motivation quote to help you get through tough times {emoji2}\n\n\n{quote}\n\n{FOOTER}"
        msg.set_content(content)
        conn.send_message(msg)
        print(f"Sent {quote} to {info['name']}")



