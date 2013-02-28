class ImproperlyConfigured(Exception):
    pass

class Field(object):
    def __init__(self, *args, **kwargs):
        self.required = kwargs.get('required', True)
        self.help_text = kwargs.get('help_text', '')
        self.default = kwargs.get('default', '')

class BaseConfig(object):
    def __new__(self, *args, **kwargs):
        self.fields = {}
        for attr, value in self.__dict__.items():
            if isinstance(value, Field):
                self.fields[attr] = None
        return object.__new__(self, *args, **kwargs)

    def is_valid(self):
        for field_name, value in self.fields.items():
            if getattr(self, field_name).required and not value:
                raise ImproperlyConfigured('"{}" config field is required'.format(field_name))
        return True