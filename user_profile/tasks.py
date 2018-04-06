# Create your tasks here
from __future__ import absolute_import, unicode_literals

from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from channellive.celery import app


@app.task
def send_email_verification(user_id):
    user = User.objects.filter(pk=user_id).first()
    if user is not None:
        code = user.userprofile.verification_code
        message = "Your verification code is: \
                   \n\n %s \
                  \n\n- Channel Live Team -" % code
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
