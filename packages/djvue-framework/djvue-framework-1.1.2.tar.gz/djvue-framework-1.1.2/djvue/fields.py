from enum import IntEnum, Enum

import rest_framework
from django.conf import settings
from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework.fields import ChoiceField, BooleanField, NullBooleanField, CharField, EmailField, RegexField, \
    SlugField, URLField, UUIDField, IPAddressField, IntegerField, FloatField, DecimalField, DateTimeField, DateField, \
    TimeField, DurationField, MultipleChoiceField, FilePathField, FileField, ImageField, ListField, _UnvalidatedField, \
    DictField, HStoreField, JSONField, ReadOnlyField, HiddenField, SerializerMethodField, ModelField, Field, empty


class DVComponent(IntEnum):
    B_FORM_INPUT = 0
    B_FORM_CHECKBOX = 1
    B_FORM_TEXTAREA = 2
    B_ROW = 3
    B_COL = 4
    DIV = 5
    DJVUE_HIDDEN = 6
    DJVUE_SELECT = 7
    DJVUE_CHECKBOX_GROUP = 8
    DJVUE_RADIO_GROUP = 9
    DJVUE_AC_SELECT = 10,
    DJVUE_INPUT_GROUP = 11,


class DVFormLabelAlign(Enum):
    NONE = None
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


DEFAULT_DV_FORM_SIZE = getattr(settings, 'DEFAULT_DV_FORM_SIZE', None)


class ChoiceSerializer(serializers.Serializer):
    id = serializers.CharField(source='value')
    text = serializers.CharField(source='label')


class DVField:
    """
    Base class for **DjVue**'s serializers fields.
    """
    def get_dv_info(self):
        ret = {}
        for i in self.Meta.dv_field:
            value = getattr(self, i, None)
            if isinstance(value, Enum):
                value = value.value
            if value is not None and value != rest_framework.fields.empty:
                ret[i] = force_str(value, strings_only=True)
        return ret

    class Meta:
        dv_field = (
            'read_only', 'label', 'help_text', 'default', 'required', 'allow_null')

#
# class DVBooleanField(BooleanField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`BooleanField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#booleanfield>`_)
#     """
#
#     def __init__(self, size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         """
#         :param str size: bootstrap form size
#         :param args:
#         :param kwargs:
#         """
#         super(DVBooleanField, self).__init__(*args, **kwargs)
#         self.size = size


# class DVNullBooleanField(NullBooleanField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`NullBooleanField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#nullbooleanfield>`_)
#     """
#
#     def __init__(self, size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         """
#         :param str size: bootstrap form size
#         :param args:
#         :param kwargs:
#         """
#         super(DVNullBooleanField, self).__init__(*args, **kwargs)
#         self.size = size


# class DVEmailField(EmailField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`EmailField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#emailfield>`_)
#     """
#     pass


# class DVRegexField(RegexField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`RegexField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#regexfield>`_)
#     """
#     pass


# class DVSlugField(SlugField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`SlugField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#slugfield>`_)
#     """
#     pass


# class DVURLField(URLField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`URLField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#urlfield>`_)
#     """
#     pass


# class DVUUIDField(UUIDField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`UUIDField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#uuidfield>`_)
#     """
#     pass


# class DVIPAddressField(IPAddressField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`IPAddressField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#ipaddressfield>`_)
#     """
#     pass


# class DVIntegerField(IntegerField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`IntegerField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#integerfield>`_)
#     """
#     placeholder = None
#
#     def __init__(self, widget=None, placeholder=None, size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         """
#         :param str placeholder: form field placeholder
#         :param str size: bootstrap form fiels size
#         :param args:
#         :param kwargs:
#         """
#         super(DVIntegerField, self).__init__(*args, **kwargs)
#         self.placeholder = placeholder
#         self.widget = widget
#         self.size = size
#
#     class Meta(DVField.Meta):
#         dv_field = DVField.Meta.dv_field + ('max_value', 'min_value', 'placeholder')


# class DVFloatField(FloatField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`FloatField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#floatfield>`_)
#     """
#     placeholder = None
#
#     def __init__(self, placeholder=None, size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         """
#
#         :param str placeholder: form field placeholder
#         :param str size: bootstrap form fiels size
#         :param args:
#         :param kwargs:
#         """
#         super(DVFloatField, self).__init__(*args, **kwargs)
#         self.placeholder = placeholder
#         self.size = size
#
#     class Meta(DVField.Meta):
#         dv_field = DVField.Meta.dv_field + ('max_value', 'min_value', 'placeholder')


# class DVDecimalField(DecimalField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`DecimalField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#decimalfield>`_)
#     """
#     placeholder = None
#
#     def __init__(self, max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
#                  localize=False, rounding=None, placeholder=None, widget=None,
#                  size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         """
#
#         :param max_digits:
#         :param decimal_places:
#         :param coerce_to_string:
#         :param max_value:
#         :param min_value:
#         :param localize:
#         :param rounding:
#         :param str placeholder: form field placeholder
#         :param str size: bootstrap form fiels size
#         :param args:
#         :param kwargs:
#         """
#         super(DVDecimalField, self).__init__(max_digits, decimal_places, coerce_to_string, max_value, min_value,
#                                              localize, rounding, *args, **kwargs)
#         self.placeholder = placeholder
#         self.widget = widget
#         self.size = size
#
#     class Meta(DVField.Meta):
#         dv_field = DVField.Meta.dv_field + ('max_digits', 'decimal_places', 'max_value', 'min_value', 'placeholder')


# class DVCurrencyField(DVDecimalField):
#     placeholder = None
#
#     def __init__(self, max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
#                  localize=False, rounding=None, placeholder=None, prepend=None, append=None, input_class=None,
#                  size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         super(DVCurrencyField, self).__init__(max_digits, decimal_places, coerce_to_string, max_value, min_value,
#                                               localize, rounding, placeholder, DVComponent.DJVUE_INPUT_GROUP, size, *args, **kwargs)
#         self.append = append
#         self.prepend = prepend
#         self.input_class = input_class
#
#     class Meta(DVDecimalField.Meta):
#         dv_field = DVDecimalField.Meta.dv_field + ('append', 'prepend', 'input_class')


class DVDateTimeField(DateTimeField):
    """
    **DjVue** wrapper for DjangoRestFramework's :code:`DateTimeField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#datetimefield>`_)
    """

    def __init__(self, format=empty, input_formats=None, default_timezone=None, *args, **kwargs):
        """

        :param format:
        :param input_formats:
        :param default_timezone:
        :param str placeholder: form field placeholder
        :param str size: bootstrap form fiels size
        :param args:
        :param kwargs:
        """
        super(DVDateTimeField, self).__init__(format, input_formats, default_timezone, *args, **kwargs)

    def to_internal_value(self, value):
        if value == '':
            return None
        return super(DVDateTimeField, self).to_internal_value(value)


class DVDateField(DateField, DVField):
    """
    **DjVue** wrapper for DjangoRestFramework's :code:`DateField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#datefield>`_)
    """

    def __init__(self, format=empty, input_formats=None, *args, **kwargs):
        """

        :param format:
        :param input_formats:
        :param str placeholder: form field placeholder
        :param str size: bootstrap form fiels size
        :param args:
        :param kwargs:
        """
        super(DVDateField, self).__init__(format, input_formats, *args, **kwargs)

    def to_internal_value(self, value):
        if value == '':
            return None
        return super(DVDateField, self).to_internal_value(value)


class DVTimeField(TimeField, DVField):
    """
    **DjVue** wrapper for DjangoRestFramework's :code:`TimeField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#timefield>`_)
    """

    def __init__(self, format=empty, input_formats=None, *args, **kwargs):
        """

        :param format:
        :param input_formats:
        :param str placeholder: form field placeholder
        :param str size: bootstrap form fiels size
        :param args:
        :param kwargs:
        """
        super(DVTimeField, self).__init__(format, input_formats, *args, **kwargs)


# class DVDurationField(DurationField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`DurationField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#durationfield>`_)
#     """
#     pass


class DVMultipleChoiceField(MultipleChoiceField, DVField):
    """
    **DjVue** wrapper for DjangoRestFramework's :code:`MultipleChoiceField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#multiplechoicefield>`_)
    """
    many = True
    choices_serializer = None
    placeholder = None

    def __init__(self, choices, choice_serializer=ChoiceSerializer, placeholder=None, size=DEFAULT_DV_FORM_SIZE,
                 widget=None, *args, **kwargs):
        """
        
        :param choices: 
        :param choice_serializer: 
        :param str placeholder: form field placeholder
        :param str size: bootstrap form fiels size 
        :param widget: 
        :param args: 
        :param kwargs: 
        """
        super(DVMultipleChoiceField, self).__init__(choices, *args, **kwargs)
        # self.placeholder = placeholder
        self.choices_serializer = choice_serializer
        # self.size = size
        self.widget = widget or DVComponent.DJVUE_SELECT

    def serialize_choices(self):
        return [self.choices_serializer(s).data for s in self.choices]

    def get_dv_info(self):
        info = super().get_dv_info()
        info['options'] = self.serialize_choices()
        return info

    class Meta(DVField.Meta):
        dv_field = DVField.Meta.dv_field + ('many',)


# class DVFilePathField(FilePathField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`FilePathField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#filepathfield>`_)
#     """
#     pass


# class DVFileField(FileField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`FileField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#filefield>`_)
#     """
#     pass


# class DVImageField(ImageField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`ImageField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#imagefield>`_)
#     """
#     pass


# class DVListField(ListField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`ListField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#listfield>`_)
#     """
#     pass


# class DV_UnvalidatedField(_UnvalidatedField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`_UnvalidatedField`
#     """
#     pass


# class DVDictField(DictField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`DictField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#dictfield>`_)
#     """
#     pass


# class DVHStoreField(HStoreField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`HStoreField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#hstorefield>`_)
#     """
#     pass


# class DVJSONField(JSONField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`JSONField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#jsonfield>`_)
#     """
#     pass


# class DVReadOnlyField(ReadOnlyField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`ReadOnlyField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#readonlyfield>`_)
#     """
#     pass


# class DVHiddenField(HiddenField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`HiddenField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#hiddenfield>`_)
#     """
#     pass


# class DVSerializerMethodField(SerializerMethodField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`SerializerMethodField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield>`_)
#     """
#
#     def __init__(self, widget=None, placeholder=None, size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         """
#
#         :param widget:
#         :param placeholder:
#         :param size:
#         :param args:
#         :param kwargs:
#         """
#         super(DVSerializerMethodField, self).__init__(*args, **kwargs)
#         self.placeholder = placeholder
#         self.size = size
#         self.widget = widget
#
#     pass


# class DVModelField(ModelField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`ModelField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#modelfield>`_)
#     """
#     pass


# class DVCharField(CharField, DVField):
#     """
#     **DjVue** wrapper for DjangoRestFramework's :code:`CharField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#charfield>`_)
#     """
#     placeholder = None
#
#     def __init__(self, widget=DVComponent.B_FORM_INPUT, placeholder=None, size=DEFAULT_DV_FORM_SIZE, *args, **kwargs):
#         """
#
#         :param DVComponent widget: form field widget
#         :param str placeholder: form field placeholder
#         :param str size: bootstrap form fiels size
#         :param args:
#         :param kwargs:
#         """
#         super(DVCharField, self).__init__(*args, **kwargs)
#         self.placeholder = placeholder
#         self.size = size
#         self.widget = widget
#
#     class Meta(DVField.Meta):
#         dv_field = DVField.Meta.dv_field + ('max_length', 'min_length', 'placeholder')


class DVChoiceField(ChoiceField, DVField):
    """
    **DjVue** wrapper for DjangoRestFramework's :code:`ChoiceField` (`\U0001F517 <https://www.django-rest-framework.org/api-guide/fields/#choicefield>`_)
    """
    choices_serializer = None
    # placeholder = None

    def __init__(self, choices, choice_serializer=ChoiceSerializer, *args, **kwargs):
        """
        
        :param choices: 
        :param choice_serializer: 
        :param str placeholder: form field placeholder
        :param str size: bootstrap form fiels size 
        :param widget: 
        :param args: 
        :param kwargs: 
        """
        super(DVChoiceField, self).__init__(choices, *args, **kwargs)
        # self.placeholder = placeholder
        self.choices_serializer = choice_serializer
        # self.size = size
        # self.widget = widget or DVComponent.DJVUE_RADIO_GROUP

    def serialize_choices(self):
        return [self.choices_serializer(s).data for s in self.choices]

    def get_dv_info(self):
        info = super().get_dv_info()
        info['options'] = self.serialize_choices()
        return info
