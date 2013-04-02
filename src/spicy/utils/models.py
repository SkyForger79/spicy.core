# coding: utf-8
"""
Stuff utils for abstract models
"""
from django.db.models import get_model


def get_custom_model_class(custom_model_name):
    '''
    Returns class for abstract model

    Args:
        custom_model_name (str): Custom model name in format 'appName.UserModel'
    '''
    return get_model(*custom_model_name.split('.'))
