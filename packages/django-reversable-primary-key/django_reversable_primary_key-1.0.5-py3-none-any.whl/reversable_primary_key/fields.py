from django_utils.fields import BigIntStrRepr
from reversable_primary_key.primary_key import make_id

class BigIntStrReprAuto(BigIntStrRepr):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{
            'default': make_id,
            **kwargs,
        })