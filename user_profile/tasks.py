# Create your tasks here
from __future__ import absolute_import, unicode_literals

from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from channellive.celery import app
from notification.models import Notification


@app.task
def send_email_verification(user_id):
    user = User.objects.filter(pk=user_id).first()
    if user is not None:
        code = user.userprofile.verification_code
        print code
        message = "Your verification code for %s is: \
                   \n\n %s \
                  \n\n- Channel Live Team -" % (user.username, code)
        send_mail(subject="Verify your Channel Live account",
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[user.email, ],
                  fail_silently=False,
                  )


@app.task
def verification_code_generator(pk=None):
    userset = User.objects.all()
    for user in userset.filter(userprofile__is_verified=False):
        code = str(randint(0, 9))
        count = 0
        while count < 3:
            code += str(randint(0, 9))
            count += 1
        user.userprofile.verification_code = code
        user.userprofile.save(update_fields=['verification_code'])


@app.task
def user_code_generator(user_id):
    user = User.objects.filter(id=user_id).first()
    code = str(randint(0, 9))
    count = 0
    while count < 3:
        code += str(randint(0, 9))
        count += 1
    user.userprofile.verification_code = code
    user.userprofile.save(update_fields=['verification_code'])
    send_email_verification.delay(user_id)


@app.task
def change_notifications(user_id):
    queryset = Notification.objects.filter(user_id=user_id)
    queryset.update(unread=False)
