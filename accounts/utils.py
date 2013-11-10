# -*- coding: utf-8 -*-
import hashlib
import random
import string

from django.core.mail import EmailMultiAlternatives
from django.core.signing import Signer
from django.template import Context
from django.template.loader import get_template
import accounts.models
from django.conf import settings

SALT = 'supertajnasolnickakterounikdoneuhadne'

def send_template_email(template, to_emails, subject, context):
    """Sending templated email by html file and text file

    Args:
        template - string, the name of template
        to_users - list of recipients emails
        subject - string
        context - dictionary of context to templates
    """


    plaintext = get_template('emails/accounts/{0}.txt'.format(template))
    htmly = get_template('emails/accounts/{0}.html'.format(template))

    cont = Context(context)

    text_cont = plaintext.render(cont)
    html_cont = htmly.render(cont)

    msg = EmailMultiAlternatives(subject, text_cont, 'sportovnicentrum@apellia.cz', to_emails)
    msg.attach_alternative(html_cont, 'text/html')
    msg.send()


def get_user(email, queryset=None):
    if not queryset:
        queryset = accounts.models.User.objects
    return queryset.get(email=email)

def check_activation_string(user, tested_string):
    new_str = make_activation_string(user)
    return True if tested_string == new_str else False

def make_activation_string(user):
    """ Vytvorti aktivacni klic pro uzivatele. Neuklada se do databaze,
    pouziva se hashovani. Neni moc bezpecne, ale tady snad staci.
    """
    return hashlib.sha224("{0}{1}".format(user.id, user.email)).hexdigest()


def send_activation_email(user, password=None):
    """
    Send email to user to activate his account by generating link
    """
    activation_string = make_activation_string(user)

    activation_link = 'http://{0}/accounts/activate/?ui={1}&as={2}'.format(settings.DOMAIN_NAME, user.id, activation_string)
    send_template_email('activation_email', [user.email], 'Sportovnicentrum - aktivujte svuj ucet',
                        {'user': user, 'activation_link': activation_link, 'password': password}
                        )


