
def get_cls_keys(cls):
    """Yield custom class keys."""
    # Loop through all the class keys
    for key in dir(cls):

        # Only yield custom keys
        if not key.startswith('_') and not callable(getattr(cls, key)):
            yield key
