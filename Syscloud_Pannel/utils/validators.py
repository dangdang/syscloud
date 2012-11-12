'''
Created on 2012-11-5

@author: root
'''

from django.conf import settings
from django.core.exceptions import ValidationError

horizon_config = getattr(settings, "HORIZON_CONFIG", {})
password_config = horizon_config.get("password_validator", {})


def validate_port_range(port):
    if port not in range(-1, 65536):
        raise ValidationError("Not a valid port number")


def password_validator():
    return password_config.get("regex", ".*")


def password_validator_msg():
    return password_config.get("help_text", ("Password is not accepted"))
