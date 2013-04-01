from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


def send_message_social_notify(sender, **kwargs):    
    instance = kwargs.get('instance')
    if instance.receiver and kwargs.get('created'):
        instance.receiver.email_user(instance.title, mark_safe(instance.msg))
                                                         

def update_user_details(sender, **kwargs):
    changed = False
    details = kwargs.pop('details', {})
    user = kwargs.pop('user')
    for name, value in details.iteritems():
        if (name not in ('username', 'email') and value and
            value != getattr(user, name, value)):
            setattr(user, name, value)
            changed = True

    return changed
