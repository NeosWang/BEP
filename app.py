import os 
from flask import Flask, request, render_template, jsonify, send_from_directory 
import requests,json
from backend import data_processor, data_preview
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.from_object("settings.DevelopmentConfig")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt','csv','tsv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'jads.png', 
                               mimetype='image/vnd.microsoft.icon')

# @app.route("/")
# def index():
#     links, nodes = data_processor.get_data()
#     return render_template("test.html", links=links, nodes=nodes)
@app.route("/")
def index():
    return render_template("home.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process', methods=['GET', 'POST'])
def ajax_process():
    if request.method=='POST':
        param = json.loads(request.form.get('param'))
 
    result ={
        'success':200,
        'msg': 'success',  
        'entities': data_preview.process(param['entities'],0),
        'relationships': data_preview.process(param['relationships'],1) 
    } 
    return result
        


@app.route('/preview', methods=[ 'GET','POST'])
def ajax_preview():
    if request.method == 'POST':  
        if 'file' not in request.files:
            return {
                'status': 206,
                'msg': 'no selected file'
            }           
        file = request.files['file']
        
        if file.filename == '':
            return {
                'status': 206,
                'msg': 'no selected file'
            }  
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return {
                'status': 415,
                'msg': 'only allow txt, csv, tsv'
            }
        

        param = json.loads(request.form.get('param'))

        dct = {
            'filename':filename,
            'path': app.config['UPLOAD_FOLDER'],
            'noneHeader': param['noneHeader'],
            'sep' :param['sep'],

        }

        is_relationships = param['isRelationships']
        title = 'relationships' if is_relationships else 'entities'
        
        return  {
            'status':200,
            'table': data_preview.process(dct, is_relationships, True),
            'title': title,
            'param': dct,
            'msg': 'success'
        } 




if __name__ == '__main__':
    app.run()
