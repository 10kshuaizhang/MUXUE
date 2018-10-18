from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM

def generate_random_str(rand_length=8):
    raw_str = "1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"
    new_str = ""
    length = len(raw_str)-1
    for n in range(rand_length):
        new_str += raw_str[Random().randint(0, length)]

    return new_str


def send_register_email(email, send_type=0):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = generate_random_str(4)
    else:
        code = generate_random_str(16)

    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()
    email_title = ""
    email_body = ""
    if send_type == "register":

        email_title = "Register activation"
        email_body = "Please click the following link to finish register: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    if send_type == "forget":
        email_title = "Reset"
        email_body = "Please click the following link to reset password: http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    if send_type == "update_email":
        email_title = "update_email"
        email_body = "Your verification code: {0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
