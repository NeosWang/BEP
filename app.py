import os 
from flask import Flask, request, render_template, jsonify, send_from_directory 
import requests,json
from backend import data_processor, data_preview
import pandas as pd

app = Flask(__name__)

app.config.from_object("settings.DevelopmentConfig")

@app.route('/favicon.ico') 
def favicon(): 

    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'jads.png', 
                               mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    links, nodes = data_processor.get_data()
    return render_template("test.html", links=links, nodes=nodes)


@app.route("/table")
def html_table():
    df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                   'Patient ID': [5, 6, 7, 8, 9],
                   'C': ['a', 'fuck', 'c--', 'd', 'e']})
    return render_template("table.html", column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="Patient ID", zip=zip)



@app.route("/preview", methods=['GET','POST'])
def ajax_preview():
        data = json.loads(request.form.get('data1'))
        sep = data['sep']
        header = None if data['noneHeader']==1 else 0

        
        
        path = "backend/data/"

        data_links = 'primaryschool.csv'

        data_nodes = 'metadata_primaryschool.txt'               
        
        result = data_preview.preview(path=path, data=data_links, sep = sep, header=header)
        

        return result

if __name__ == '__main__':
    app.run()
