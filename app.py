from config import Config
from cli import create_db
import pandas as pd
from models import *

app.config.from_object(Config)
app.cli.add_command(create_db)
db.init_app(app)


@app.route('/')
def hello_world():
    export_db()
    return 'Hello World!'


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
