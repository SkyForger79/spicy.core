# coding: utf-8
"""
Stuff utils for abstract models
"""
from django.db.models.loading import cache

def get_custom_model_class(custom_model_name):
    '''
    Returns class for abstract model

    Args:
        custom_model_name (str): Custom model name in format 'app_name.CustomModel'
    '''
    return cache.get_model(*custom_model_name.split('.'))


__all__ = 'get_custom_model_class',
