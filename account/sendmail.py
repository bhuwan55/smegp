from django.core.mail import send_mail


class SendVerificationMail:
    def send_mail(user):
        email_plaintext_message = "Welcome " + user['first_name'] + ", We will let you know when we approve the data you have provided.\n Thank You for joining us."
        print("helo")
        send_mail(
            # title:
            'Welcome to SMS APP',
            # message:
            email_plaintext_message,
            # from:
            "awsumbj2054@gmail.com",
            # to:
            [user['email']]
        )