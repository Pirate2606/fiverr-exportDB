from flask import render_template
from wtforms.validators import DataRequired
from config import Config
from cli import create_db
import pandas as pd
from models import *
from forms import LoginForm, MultiCheckboxField
from wtforms import StringField, TextAreaField, RadioField, SelectField, BooleanField
import json

app.config['SECRET_KEY'] = 'verySecretCode'
app.config.from_object(Config)
app.cli.add_command(create_db)
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # export_db()
    record = {"question": ["What is your name?", "What is age?", "What is class", "What is up?", "Agree",
                           "Select Multiple"],
              "type": ["StringField", "RadioField", "TextAreaField", "SelectField", "BooleanField",
                       "MultiCheckboxField"],
              "choices": [
                  [],
                  [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
                  [],
                  [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
                  [],
                  [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]
              ]}
    json_record = json.dumps(record)
    create_form_object(json_record)
    form = LoginForm()
    return render_template('form.html', form=form)


def create_form_object(json_obj):
    record = json.loads(json_obj)
    for i in range(len(record["question"])):
        variable_name = 'question' + str(i)
        if "Radio" not in record["type"][i] and "Select" not in record["type"][i] and "Checkbox" not in record["type"][i]:
            obj = record["type"][i] + f"('{record['question'][i]}', validators=[DataRequired()])"
        else:
            obj = record["type"][i] + \
                  f"('{record['question'][i]}', validators=[DataRequired()], choices={record['choices'][i]})"
        setattr(LoginForm, variable_name, eval(obj))
        login = LoginForm()


def export_db(obj_names=None):
    if obj_names is None:
        obj_names = list(db.metadata.tables.keys())
    writer = pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter')
    for obj_name in obj_names:
        data_frame = {}
        all_items = eval(obj_name.capitalize() + '.__searchable__')
        query_str = obj_name.capitalize() + '.query.with_entities('
        for item in all_items:
            data_frame[item] = []
            query_str += obj_name.capitalize() + '.' + item + ','
        query_str += ')'
        all_data = eval(query_str)
        count = 0
        for data in all_data:
            for d in data:
                data_frame[all_items[count]].append(d)
                count += 1
            count = 0
        df = pd.DataFrame(data_frame)
        df.to_excel(writer, sheet_name=obj_name, index=False)
    writer.save()


if __name__ == '__main__':
    app.run(debug=True)
