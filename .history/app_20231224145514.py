import os 
from flask import Flask, request, render_template,  send_from_directory, jsonify,redirect, url_for
import json5
from backend import data_preview
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import pandas as pd



from backend.TTINT import SNT, UNIUNI


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
ALLOWED_EXTENSIONS = set(['txt',
                          'csv',
                          'tsv',
                          'xlsx'
                          ])
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








# region[UniUni - relabel]
@app.route("/uniuni_relabel")
def uniuni_relabel():
    return render_template('uniuni_relabel.html')


@app.route("/uniuni_relabel_post", methods=['POST'])
def uniuni_relabel_post():
    if request.method=='POST':
        param = json5.loads(request.form.get('param'))
        res = UNIUNI.relabel(param)
    return res
# endregion


# region[excel]
@app.route("/excel")
def upload_excel():
    return render_template('excel.html')


@app.route('/upload_manifest', methods=['POST'])
def upload_manifest():
    if request.method == 'POST':  
        if 1:      
            if 'file' not in request.files:
                return {
                    "status":"fail",
                    "data": 'no selected file'
                }           
            file = request.files['file']
            
            
            if file.filename == '':
                return {
                    "status":"fail",
                    'data': 'no selected file'
                }  
            
            if file and allowed_file(file.filename):
                pass
                # filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return  {
                    "status":"fail",
                    'data': f"only allow {str(ALLOWED_EXTENSIONS)}"
                }    
                
            df = pd.read_excel(file)
            
        


        
        return  {
                    "status":"success",
                    'data': str(df.columns)
                }       


# endregion






@app.route('/api/test/SNT/item', methods=['POST'])
def SNT_item():

    req_data_obj = json5.loads(request.data)
    res = SNT.declare_item(req_data_obj)
    return jsonify(res)



@app.route('/api/test/SNT/manifest', methods=['POST'])
def SNT_manifest():


    req_data_obj = json5.loads(request.data)
    res = SNT.declare_manifest(req_data_obj)
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




# region [main]

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
    
    
# endregion
