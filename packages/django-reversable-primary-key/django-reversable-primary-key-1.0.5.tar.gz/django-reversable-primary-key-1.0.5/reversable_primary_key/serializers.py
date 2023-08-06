# from rest_framework.serializers import Serializer
from reversable_primary_key.primary_key import reverse_id
from rest_framework import serializers


class CreatedSerializerMixin(serializers.Serializer):

    created = serializers.SerializerMethodField()
    def get_created(self, obj):
        try:
            return reverse_id(obj.id)
        except Exception:
            return None

