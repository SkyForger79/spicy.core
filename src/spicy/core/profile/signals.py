from django.dispatch import Signal

create_message = Signal()
create_profile = Signal(providing_args=['profile'])
