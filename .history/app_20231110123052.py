import os 
from flask import Flask, request, render_template,  send_from_directory, jsonify
import json5
from backend import data_preview
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


# import requests
# from random import randint
# import hashlib
# import base64
# import urllib3


from backend.TTINT import SNT

app = Flask(__name__)

mail_settings={
    "MAIL_SERVER": 'smtp.qq.com',
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME":"180762556@qq.com",
    "MAIL_PASSWORD": "vdqzlvhldwxkcaah"
}

app.config.update(mail_settings)
mail = Mail(app)

# app.config.from_object("settings.DevelopmentConfig")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['txt','csv','tsv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def form_content(form):
    kv = [(key, form[key]) for key in form.keys() if form]
    output = ""
    for k,v in  kv:
        output +=f"""key    ===>    {k}
value    ===>    {v}
        
"""
    return output


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'jads.png', 
                               mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/bep")
def bep():
    return render_template("bep.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/mawb")
def mawb():
    return render_template('mawb.html')


@app.route('/process', methods=['GET', 'POST'])
def ajax_process():
    if request.method=='POST':
        param = json5.loads(request.form.get('param'))
 
    result ={
        'success':200,
        'msg': 'success',  
        'entities': data_preview.process(param['entities'],0),
        'relationships': data_preview.process(param['relationships'],1) 
    } 
    return result
        

@app.route('/ttint_api',methods=['GET','POST'])
def ttint_api():
    return render_template("ttint.html")

@app.route('/preview', methods=[ 'GET','POST'])
def ajax_preview():
    if request.method == 'POST':  
        
        param = json5.loads(request.form.get('param'))
        if param['demo']:
            filename = 'primaryschool.csv' if param['isRelationships'] else 'metadata_primaryschool.txt'
            
        else:           
            if 'file' not in request.files:
                return {
                    'status': 206,
                    'msg': 'no selected file'
                }           
            file = request.files['file']
            
            print(file)
            
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
        

        # param = json5.loads(request.form.get('param'))

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
            'table': data_preview.process(dct, is_relationships, True, param['demo']),
            'title': title,
            'param': dct,
            'msg': 'success'
        } 




@app.route('/api/test/SNT/item', methods=['POST'])
def SNT_item():

    req_data_obj = json5.loads(request.data)
    res = SNT.declare_item(req_data_obj)
    return jsonify(res)



@app.route('/api/test/SNT/manifest', methods=['POST'])
def SNT_manifest():
    return "1"
    return request.data
    # req_data_obj = json5.loads(request.data)
    # print(request.data)
    # res = SNT.declare_manifest(req_data_obj)
    return jsonify(res)



@app.route('/api',methods=['GET','POST'])
def showAPI():
    if request.method == "POST":
        data = request.data   # json data in bytes
        headers = request.headers

        message = Message(
        subject="Receive API call",
        sender=app.config.get("MAIL_USERNAME"),
        recipients=["yichen.wang@postnl.nl"],
        body = f"""-------data-------
{data}
--------headers---------
{headers}
--------form------------  
{form_content(request.form)}""",    # if any shit in www-form-urlencoded
        )
        mail.send(message)

        output = {"success":"true","errorCode":None,"errorMsg":None,"cbCode":None,"wayBillNo":None}
        output = {
            "success":"true",
            "errorCode":None,
            "errorMsg":None
        }
        output ="{\"success\":\"true\"}"
        
        return jsonify(output)






if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
