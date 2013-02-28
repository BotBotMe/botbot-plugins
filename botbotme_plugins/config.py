class ImproperlyConfigured(Exception):
    pass

class Field(object):
    """An individual field in a plugin config"""
    def __init__(self, *args, **kwargs):
        self.required = kwargs.get('required', True)
        self.help_text = kwargs.get('help_text', '')
        self.default = kwargs.get('default', None)

class BaseConfig(object):
    """
    Base class for plugin configs.
    `fields` attribute is a dictionary of {field_name}: {field_value}
    """
    def __new__(self, *args, **kwargs):
        self.fields = {}
        for attr, value in self.__dict__.items():
            if isinstance(value, Field):
                self.fields[attr] = value.default
        return object.__new__(self, *args, **kwargs)

    def is_valid(self):
        """Verifies that required fields have a value"""
        for field_name, value in self.fields.items():
            if getattr(self, field_name).required and not value:
                raise ImproperlyConfigured('"{}" config field is required'.format(field_name))
        return True