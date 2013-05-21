class AjaxException(Exception):
    """Base class for AJAX exceptions"""
    pass

class Ajax404(AjaxException):
    """Object not found"""
    pass

class AjaxDataException(AjaxException):
    """                                                                                                                                                                          
    Use it to push json data to response
    """

    def __init__(self, data, *args, **kwargs):
        self.data = data
        Exception.__init__(self, *args, **kwargs)
