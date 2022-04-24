from drf_base64.fields import Base64ImageField as _Base64ImageField
from rest_framework.fields import SkipField


class Base64ImageField(_Base64ImageField):
    def _decode(self, data):
        try:
            value = super()._decode(data)
        except SkipField:
            if self.required:
                self.fail('invalid_image')
            raise
        except (ValueError, UnicodeDecodeError):
            self.fail('invalid_image')
        return value
