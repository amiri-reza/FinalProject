# import requests

# def send_simple_message():
# 	return requests.post(
# 		"https://api.mailgun.net/v3/sandbox9cea4887640d4f049bf31c7267389a57.mailgun.org/messages",
# 		auth=("api", "4a470d5d4e89a0b4cd48ab552f4b11fc-15b35dee-db0ec3c6"),
# 		data={"from": "Excited User <noreply@stockprediction.com>",
# 			"to": ["amiri.reza.python@gmail.com",],
# 			"subject": "Hello",
# 			"text": "Testing some Mailgun awesomness 2!"})

# send_simple_message()

from django.conf import settings
from django.core.mail import send_mail


send_mail(
    "adsfasdf",
    "hasdfasdfasdf",
    "amiri.reza.python@gmail.com",
    "[amiri.reza68@yahoo.com]",
    fail_silently=False,
)
