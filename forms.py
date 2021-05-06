from wtforms import SelectMultipleField, widgets, SubmitField
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    submit = SubmitField("Submit")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ExampleRadioForm(FlaskForm):
    choices = MultiCheckboxField('Routes', coerce=int)
    submit = SubmitField("Set User Choices")
