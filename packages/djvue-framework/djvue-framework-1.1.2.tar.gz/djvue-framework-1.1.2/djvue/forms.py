from enum import Enum

from django.conf import settings

from djvue.fields import DVComponent


class DVGlobalFormProps(Enum):
    DEFAULT_DV_FORM_SIZE = 'size'
    DV_FORM_LABEL_ALIGN = 'labelAlign'
    DV_FORM_LABEL_ALIGN_SM = 'labelAlignSm'
    DV_FORM_LABEL_ALIGN_MD = 'labelAlignMd'
    DV_FORM_LABEL_ALIGN_LG = 'labelAlignLg'
    DV_FORM_LABEL_ALIGN_XL = 'labelAlignXl'
    DV_FORM_LABEL_COLS = 'labelCols'
    DV_FORM_LABEL_COLS_SM = 'labelColsSm'
    DV_FORM_LABEL_COLS_MD = 'labelColsMd'
    DV_FORM_LABEL_COLS_LG = 'labelColsLg'
    DV_FORM_LABEL_COLS_XL = 'labelColsXl'


class PropsComponent:
    props = {}

    def __init__(self, **kwargs):
        self.props = dict(kwargs)

    def to_dict(self):
        return self.props


class Component:
    props = PropsComponent()

    def __init__(self, **kwargs):
        self.props = PropsComponent(**kwargs)


class ComponentList:
    fields = []

    def __init__(self, *children, **kwargs):
        self.fields = list(children)

    @staticmethod
    def mapfun(x):
        if isinstance(x, str):
            return x
        else:
            return x.to_dict()

    def to_dict(self):
        return list(map(self.mapfun, self.fields))


class Div(Component):
    tag = DVComponent.DIV

    def __init__(self, *children, **kwargs):
        self.fields = ComponentList(*children)
        super(Div, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'children': self.fields.to_dict(),
            'tag': self.tag,
            'props': self.props.to_dict()
        }


class Row(Div):
    tag = DVComponent.B_ROW

    def __init__(self, *children, **kwargs):
        super(Row, self).__init__(*children, **kwargs)


class Col(Div):
    tag = DVComponent.B_COL

    def __init__(self, *fields, **kwargs):
        super(Col, self).__init__(*fields, **kwargs)


class InvalidFieldType(Exception):
    message = 'Field is not specified or is not a string'

    def __str__(self):
        return '{}'.format(self.message)


class Widget(Component):
    tag = DVComponent.B_FORM_INPUT
    field = None

    def __init__(self, field, **kwargs):
        if 'tag' in kwargs:
            self.tag = kwargs.pop('tag')
        super(Widget, self).__init__(**kwargs)
        if field is None or not isinstance(field, str):
            raise InvalidFieldType()
        self.field = field

    def to_dict(self):
        return {
            'name': self.field,
            'tag': self.tag,
            'props': self.props.to_dict()
        }


class HiddenField(Widget):
    tag = DVComponent.DJVUE_HIDDEN


class Form(Component):
    css_class = ''

    def __init__(self, *children, **kwargs):
        self.fields = ComponentList(*children)
        super(Form, self).__init__(**kwargs)

    def get_form_global_prop(self):
        ret = {}
        for e in DVGlobalFormProps:
            val = getattr(settings, e.name, None)
            if getattr(settings, e.name, None) is not None:
                ret[e.value] = val

        ret.update(self.props.to_dict())
        return ret

    def to_dict(self):
        return {
            'children': self.fields.to_dict(),
            'props': self.props.to_dict(),
            'defaults': self.get_form_global_prop()
        }


class DVFormLayout:
    def get_form(self):
        if self.Meta.fields == '__all__':
            return Form(*(list(self.fields.keys()))).to_dict()
        else:
            filtered = list(filter(lambda x: x in set(self.Meta.fields), list(self.fields.keys())))
            return Form(*filtered).to_dict()
