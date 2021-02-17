import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

cred = credentials.Certificate(settings.creed)
firebase_admin.initialize_app(cred)


def sendPush(title, msg, registration_token, dataObject):
    message = messaging.MulticastMessage(notification=messaging.Notification(title=title,
                                         body=msg,), data=dataObject,
                                         tokens=registration_token)
    response = messaging.send_multicast(message)
    print("successfully sent message", response)
