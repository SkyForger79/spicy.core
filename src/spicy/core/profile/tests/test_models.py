BASIC_TESTS = """
>>> from profile.models import Profile
>>> p = Profile.objects.create_inactive_user('testuser', 'test@example.com', password='testpw', is_staff=True)
>>> p.has_usable_password()
True
>>> p.check_password('bad')
False
>>> p.check_password('testpw')
True
>>> p.set_unusable_password()
>>> p.save()
>>> p.check_password('testpw')
False
>>> p.has_usable_password()
False
>>> p.activation_key_expired()
False
>>> p.is_authenticated()
True
>>> p.is_staff
True
>>> p.is_active
False
>>> p.is_superuser
False
>>> profile = Profile.objects.activate_user('invalid_key')
>>> profile is None
True
>>> profile = Profile.objects.activate_user(p.activation_key)
>>> profile.is_active
True
>>> profile == p
True
>>> p2 = Profile.objects.create_inactive_user('test2', 'test@example.com')
>>> p2.is_staff
False
>>> p2.is_active
False
>>> p3 = Profile.objects.create_inactive_user('test3', 'test@example.com')
>>> from django.core.management import call_command
>>> call_command("cleanup_expired_profiles", interactive=False)
0 profiles has been expired and deleted.
>>> p.add_service(s)
>>> p.get_service_settings(s)
<ServiceExtra: ServiceExtra object>
>>> [ps for ps in p.get_all_services()]
[<ServiceExtra: ServiceExtra object>]
"""
