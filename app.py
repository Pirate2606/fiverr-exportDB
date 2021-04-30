from config import Config
from cli import create_db
import pandas as pd
from models import *

app.config.from_object(Config)
app.cli.add_command(create_db)
db.init_app(app)


@app.route('/')
def hello_world():
    main_function(['users', 'posts', 'stats'], [["age", "gender", "email"],
                                                ["id", "username", "text"],
                                                ["id", "userName", "likes", "followers"]])
    return 'Hello World!'


def main_function(obj_names, all_items):
    count = 0
    for obj_name in obj_names:
        data_frame = {}
        with app.app_context():
            all_data = eval(obj_name.capitalize() + '.query.all()')
        for i in all_items[count]:
            temp = []
            for data in all_data:
                temp.append(eval('data.' + i))
            temp.append(" ")
            data_frame[i] = temp
        count += 1
        df = pd.DataFrame({'Table: ' + obj_name: [" "]})
        df.to_csv('test.csv', mode='a', index=False, )
        df = pd.DataFrame(data_frame)
        df.to_csv('test.csv', mode='a', index=False)


if __name__ == '__main__':
    app.run(debug=True)
