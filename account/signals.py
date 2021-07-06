from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print("from signals hello")

    email_plaintext_message = "Hello " + reset_password_token.key + " is your SMS OTP. Please Do not share it with anyone."
    send_mail(
        # title:
        "Password Reset for {title}".format(title="SMS"),
        # message:
        email_plaintext_message,
        # from:
        "awsumbj2054@gmail.com",
        # to:
        [reset_password_token.user.email]
    )