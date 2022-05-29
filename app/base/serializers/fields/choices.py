from rest_framework.fields import ChoiceField


class ChoicesField(ChoiceField):
    def __init__(self, choices_class, **kwargs):
        self.choices_class = choices_class
        kwargs.setdefault('help_text', choices_class.help_text)
        super().__init__(choices_class.choices, **kwargs)
    
    def to_internal_value(self, data):
        return self.choices_class(super().to_internal_value(data))
