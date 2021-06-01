from wtforms import SelectMultipleField, widgets, SubmitField, StringField, SelectField, RadioField
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    pass


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CreateForm(FlaskForm):
    form_name = StringField(render_kw={"placeholder": "Untitled Form", "class": "h5 mb-0 lh-1 text-center form-title"})
    input_field = StringField(render_kw={"placeholder": "Untitled Question"})
    dropdown = SelectField(choices=["Radio Field", "String Field", "Text Area Field", "Select Field", "Boolean Field", "Multi Checkbox Field"], 
                            render_kw={"class": "form-select answer-type", "onchange": "addField()"})
    radio_field = RadioField(choices=[('value','description')], render_kw={"class": "form-check-input mt-2"})
    radio_input_field = StringField(render_kw={"class": "option", "placeholder": "Option 1"})
    submit = SubmitField("Add a Question", render_kw={"class": "btn btn-purple btn-lg"})
