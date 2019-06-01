"""
File Path: application/modules/auth/methods.py
Description: Auth methods for App - Define auth/login methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
from wtforms import BooleanField, Form, PasswordField, StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, InputRequired


class ValidateLoginForm(Form):
    """ Validate login form fields """
    print('ValidateLoginForm: validating fields...')
    email = StringField('Email',
                        validators=[Email(),
                                    DataRequired(message='Enter a valid email'),
                                    InputRequired(message='Enter a valid email'),
                                    validators.Length(min=5, max=35)])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Enter a password min=3'),
                                         InputRequired(message='Enter a password min=3'),
                                         validators.Length(min=3, max=35)])
    remember = BooleanField('Remember')


class ValidateSignUpForm(Form):
    """ Validate sighup form fields """
    email = StringField('Email',
                        validators=[Email(),
                                    DataRequired(message='Enter a valid email'),
                                    InputRequired(message='Enter a valid email'),
                                    validators.Length(min=5, max=35)])
    first_name = StringField('First Name',
                             validators=[DataRequired('Enter a First Name, min=5'),
                                         InputRequired('Enter a First Name, min=5')])
    last_name = StringField('Last Name',
                            validators=[DataRequired('Enter a Last Name, min=5'),
                                        InputRequired('Enter a Last Name, min=5')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Enter a password, min=3'),
                                         InputRequired(message='Enter a password, min=3'),
                                         validators.Length(min=3, max=35)])
    username = StringField('Username',
                           validators=[DataRequired(message='Enter a user name, min=5'),
                                       InputRequired(message='Enter a user name, min=5'),
                                       validators.Length(min=5, max=10)])
