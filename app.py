import os 
from flask import Flask, request, render_template, jsonify, send_from_directory 
import requests,json
from backend import data_processor, data_preview
import pandas as pd
from werkzeug.utils import secure_filename

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




UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['pdf','txt','csv','tsv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/preview', methods=['GET', 'POST'])
def ajax_preview():
    if request.method == 'POST':

        
        file = request.files['file']

        data = json.loads(request.form.get('param'))

        
        sep = data['sep']
        header = None if data['noneHeader']=='1' else 0
        is_relationships = data['isRelationships']
        

        path = "backend/data/"

        data_links = 'primaryschool.csv'

        data_nodes = 'metadata_primaryschool.txt'
        
        raw_data  = data_links if is_relationships else data_nodes             
        
        result = data_preview.preview(path=path, data=raw_data, sep = sep, header=header)
        

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return  result
        return  result
    return ''



if __name__ == '__main__':
    app.run()
