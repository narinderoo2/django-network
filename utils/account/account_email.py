from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings



def send_otp(user_name, to_email, otp):
    subject = 'Hello, {} Request to Reset Password'
    message = '''
    Hi {},

    Need to reset your password? 

    Use this secret code {} 

    



    Thanks & Regards
    Narinder Singh

    '''.format(user_name,user_name, otp)

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email,]
    try:
        send_mail( subject, message, email_from, recipient_list )
        return 1
    except Exception as e:
        return 0
        

def send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    connection=None,
    html_message=None,
):
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(
        subject, message, from_email, recipient_list, connection=connection
    )
    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()
