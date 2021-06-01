from flask import render_template, request
from config import Config
from cli import create_db
import pandas as pd
from models import app, db, Questions, Users, Posts, Stats
from forms import LoginForm, MultiCheckboxField, CreateForm
from wtforms import StringField, TextAreaField, RadioField, SelectField, BooleanField
from wtforms.validators import DataRequired
import json
import copy


app.config['SECRET_KEY'] = 'verySecretCode'
app.config.from_object(Config)
app.cli.add_command(create_db)
db.init_app(app)

count = 1
created = 1


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # export_db()
    # record = {"question": ["What is your name?", "What is age?",
    #                         "What is class", "What is up?", "Agree",
    #                        "Select Multiple"],
    #           "type": ["StringField", "RadioField", "TextAreaField",
    #                     "SelectField", "BooleanField",
    #                    "MultiCheckboxField"],
    #           "choices": [
    #               [],
    #               [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
    #               [],
    #               [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
    #               [],
    #               [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]
    #           ]}
    # login = copy.deepcopy(LoginForm)
    # json_record = json.dumps(record)
    # create_form_object(json_record, login)
    # form = LoginForm()
    
    # if "addField" in request.form:
    #     field = form_.dropdown.data.replace(" ", "")

    global created
    global count
    # record = '{"question": [], "type": [],"choices": []}'
    # r = json.loads(record)
    # question = Questions(questions=str(r))
    # db.session.add(question)
    # db.session.commit()
    
    record = json.loads(Questions.query.get(1).questions.replace("'", '"'))
    # record = json.loads(record)
    login = copy.deepcopy(LoginForm)
    r = json.dumps(record)
    create_form_object(r, login)
    form = LoginForm()
    
    if request.method == "POST":
        created += 1
        count += 1
        field_name = request.form.get("select-field")
        question = request.form.get("question")
        record["question"].append(question)
        record["type"].append(field_name)
        record["choices"].append([])
        r = json.dumps(record)
        login = copy.deepcopy(LoginForm)
        create_form_object(r, login)
        form = LoginForm()
        Questions.query.get(1).questions = str(r)
        db.session.commit()
        return render_template('create-form.html', count=count, created=created, form=form)
    
    return render_template('create-form.html', count=count, created=created, form=form)


def create_form_object(json_obj, login_obj):
    record = json.loads(json_obj)
    for i in range(len(record["question"])):
        variable_name = 'question' + str(i)
        if "Radio" not in record["type"][i] and "Select" not in record["type"][i] and "Checkbox" not in record["type"][i]:
            obj = record["type"][i] + f"('{record['question'][i]}', validators=[DataRequired()])"
        else:
            obj = record["type"][i] + \
                  f"('{record['question'][i]}', validators=[DataRequired()], choices={record['choices'][i]})"
        setattr(login_obj, variable_name, eval(obj))


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
