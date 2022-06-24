import base64
import uuid

from django.core.files.base import ContentFile

from rest_framework import serializers


class Base64ToImageField(serializers.ImageField):
    """Decode base64 string to image file."""
    def to_internal_value(self, data: str):
        if ';base64,' not in data:
            raise serializers.ValidationError('wrong_image')
        base64_head, base64_str_image = data.split(sep=';base64,')
        try:
            extension = base64_head[base64_head.find('/') + 1:]
            image_name_extension = str(uuid.uuid4()) + '.' + extension
        except ValueError:
            raise serializers.ValidationError('wrong_image')
        image_file = base64.b64decode(base64_str_image)

        data = ContentFile(content=image_file, name=image_name_extension)
        return super(Base64ToImageField, self).to_internal_value(data)
