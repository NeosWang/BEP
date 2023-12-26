import os 
from flask import Flask, request, render_template,  send_from_directory, jsonify,redirect, url_for
import json5
from backend import data_preview
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import pandas as pd



from backend.TTINT import UNIUNI
from backend.TTINT.SNT import SNT , process_billing_extra


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


def __mail_to(subject, mail_body,receiver, attachment=None):
    message= Message(
        subject=subject,
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[ receiver ],
        cc=["yichen.wang@postnl.nl"],
        body= mail_body        
    )
    if attachment:
        with app.open_resource(f"{UPLOAD_FOLDER}/{attachment}") as fp:
            message.attach(f"{UPLOAD_FOLDER}/{attachment}","application/vnd.ms-excel",fp.read())
    return mail.send(message)

def form_content(form):
    kv = [(key, form[key]) for key in form.keys() if form]
    output = ""
    for k,v in  kv:
        output +=f"""key    ===>    {k}
value    ===>    {v}
        
"""
    return output

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'cc.png', 
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
                
            df = process_billing_extra.process_billing_extra(file) 
            attachment ="output.xlsx"
            df.to_excel(f"{UPLOAD_FOLDER}/{attachment}", index=False)
            __mail_to("bill","check attachment","yichen.wang@postnl.nl",attachment=attachment)
            
        return  {
                    "status":"success",
                    'data': str(df.columns)
                }       


# endregion




# region[API]

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


        body = f"""-------data-------
{data}
--------headers---------
{headers}
--------form------------  
{form_content(request.form)}"""   # if any shit in www-form-urlencoded
        
        
        __mail_to(
            subject="Receive API call",
            mail_body= body,
            receiver= "yichen.wang@postnl.nl"
        )


        output = {"success":"true","errorCode":None,"errorMsg":None,"cbCode":None,"wayBillNo":None}
        output = {
            "success":"true",
            "errorCode":None,
            "errorMsg":None
        }
        output ="{\"success\":\"true\"}"
        
        return jsonify(output)




# endregion

# region [main]

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
    
    
# endregion