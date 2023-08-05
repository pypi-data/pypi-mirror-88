from django.apps import AppConfig


class PostaladdressConfig(AppConfig):
    """
    Define config for the member app so that we can hook in signals.
    """
    name = 'postaladdress'
