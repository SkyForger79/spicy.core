import string
import random


def generate_random_password(length=10):
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for i in range(length)])