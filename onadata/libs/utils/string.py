from past.builtins import basestring


def str2bool(v):
    return v.lower() in (
        'yes', 'true', 't', '1') if isinstance(v, basestring) else v


def str2int(value):
    """Convert string to integer but if the string value is 'None' return None.
    """
    if isinstance(value, basestring) and value.lower() == 'none':
        return None
    return int(value)
