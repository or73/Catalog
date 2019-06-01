"""
File Path: application/modules/auth/methods.py
Description: Auth methods for App - Define auth/login methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from wtforms import Field, FieldList, Form, StringField, validators
from wtforms.validators import DataRequired, InputRequired


class ValidateCreateUpdateForm(Form):
    """ Validate Create/Update form fields """
    name = StringField('Name',
                       validators=[DataRequired('Input a Name, min=5'),
                                   InputRequired('Input a Name, min=5'),
                                   validators.Length(min=5, max=35)])
    description = StringField('Description',
                              validators=[DataRequired('Input a Description, min=5'),
                                          InputRequired('Input a Description, min=5'),
                                          validators.Length(min=5, max=35)])
    price = StringField('Price',
                        validators=[DataRequired('Input a Price'),
                                    InputRequired('Input a Price')])
    items_list = FieldList(StringField('item_list'))
