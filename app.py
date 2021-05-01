from config import Config
from cli import create_db
import pandas as pd
from models import *

app.config.from_object(Config)
app.cli.add_command(create_db)
db.init_app(app)


@app.route('/')
def hello_world():
    export_db(["users"])
    return 'Hello World!'


def export_db(obj_names=None):
    if obj_names is None:
        obj_names = list(db.metadata.tables.keys())
    count = 0
    writer = pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter')  # Remove this if you want CSV file
    for obj_name in obj_names:
        data_frame = {}
        with app.app_context():
            all_data = eval(obj_name.capitalize() + '.query.all()')
        all_items = eval(obj_name.capitalize() + '.__searchable__')
        for i in all_items:
            temp = []
            for data in all_data:
                temp.append(eval('data.' + i))
            data_frame[i] = temp
        count += 1
        # EXCEL FILE CODE STARTS (3 Lines)
        df = pd.DataFrame(data_frame)
        df.to_excel(writer, sheet_name=obj_name, index=False)
    writer.save()
    # EXCEL FILE CODE ENDS

    # CSV FILE CODE STARTS

    # df = pd.DataFrame({'Table: ' + obj_name: [" "]})
    # df.to_csv('test.csv', mode='a', index=False, )
    # df = pd.DataFrame(data_frame)
    # df.to_csv('test.csv', mode='a', index=False)

    # CSV FILE CODE ENDS


if __name__ == '__main__':
    app.run(debug=True)
