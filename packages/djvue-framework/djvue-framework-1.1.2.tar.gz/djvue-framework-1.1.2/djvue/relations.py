from rest_framework.relations import PrimaryKeyRelatedField
from djvue.fields import DVField


# Attenzione: nel caso in cui si tratti di una relazione many to many, le informazioni non vengono prese dal get_dv_info
# ma bensì inserite direttamente dalla classe metadata, questo a causa di un funzionamento interno di django drf


class DVAutocompletePrimaryKeyRelatedField(PrimaryKeyRelatedField, DVField):
    """
       Equivalent of DRF PrimaryKeyRelatedField
    """
    allowCreation = False
    # placeholder = None
    # widget = None
    ac = True

    def __init__(self, allowCreation=False, *args, **kwargs):
        """

        :param widget:
        :param placeholder:
        :param allow_creation:
        :param size:
        :param args:
        :param kwargs:
        """
        # self.placeholder = placeholder
        self.allowCreation = allowCreation
        # self.widget = widget
        # self.size = size
        PrimaryKeyRelatedField.__init__(self, **kwargs)

    class Meta(DVField.Meta):
        dv_field = DVField.Meta.dv_field + ('ac', 'allowCreation')


class DVInlinePrimaryKeyRelatedField(PrimaryKeyRelatedField, DVField):

    def __init__(self, *args, **kwargs):
        PrimaryKeyRelatedField.__init__(self, many=True, **kwargs)