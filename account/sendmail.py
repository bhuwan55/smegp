from django.core.mail import send_mail
from django.conf import settings


class SendVerificationMail:
    def send_mail(user):
        email_plaintext_message = "Welcome " + user['first_name'] + ", We will let you know when we approve the data you have provided.\n Thank You for joining us."
        print("hello")
        send_mail(
            # title:
            'Welcome to SMS APP',
            # message:
            email_plaintext_message,
            # from:
            settings.FROM_EMAIL,
            # to:
            [user['email']]
        )