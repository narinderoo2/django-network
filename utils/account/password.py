
from django.contrib.auth.hashers import make_password

from account.models import *


def last_three_password_history(email,password):

    pass_check = PasswordHistory.objects.filter(email__email = email,
    password=password).order_by('-create_at')[:3]
    if pass_check.exists():
        print(pass_check,'password check last 3 password history')
        return True
    else:
        return False

def password_history_save(email,password):
    get_detail = UserProfile.objects.get(email=email)
    pass_save= PasswordHistory.objects.create(email=get_detail,password=make_password(password))
    print('--------==************>>>>>',get_detail)
    pass_save.save()
    return 