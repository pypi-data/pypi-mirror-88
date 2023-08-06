from djangoldp.permissions import LDPPermissions
from django.db.models.base import ModelBase

class InvoicePermissions(LDPPermissions):
    def user_permissions(self, user, obj_or_model, obj=None):
        if not user.is_anonymous:
            if not isinstance(obj_or_model, ModelBase):
                obj = obj_or_model
            if obj:
                return ['view', 'add', 'change']

        return []
