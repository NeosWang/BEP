import os
from flask import Flask, request, render_template,  send_from_directory, jsonify, redirect, url_for
import json5
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message



from backend.TTINT.SNT import SNT
import backend.uniuni_relabel as uniuni_relabel
import backend.snt_billing_repush as snt_billing_repush
import backend._config as _config


app = Flask(__name__)

app.config.update(_config.MAIL_SETTINGS)
app.config['UPLOAD_FOLDER'] = _config.UPLOAD_FOLDER

mail = Mail(app)

# app.config.from_object("settings.DevelopmentConfig")


def send_mail(subject, receiver, body, attached=None):
    with app.app_context():
        message = Message(
            subject=subject,
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[receiver],
            cc=["yichen.wang@postnl.nl"],
            body=body
        )
        if attached:
            with app.open_resource(f"{_config.UPLOAD_FOLDER}\{attached}") as fp:
                message.attach(attached, "text/csv", fp.read())
        return mail.send(message)


def form_content(form):
    kv = [(key, form[key]) for key in form.keys() if form]
    output = ""
    for k, v in kv:
        output += f"""key    ===>    {k}
value    ===>    {v}
        
"""
    return output


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in _config.ALLOWED_EXTENSIONS


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'cc.png',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/")
def index():
    return render_template("home.html")


# region[ /uniuni/relabel ]

@app.route("/uniuni/relabel")
def route_uniuni_relabel():
    return uniuni_relabel.home()


@app.route("/uniuni/relabel_async_post", methods=['POST'])
def route_uniuni_relabel_async_post():
    return uniuni_relabel.relabel()

# endregion


# region[ /snt/billing_repush ]

@app.route("/snt/billing_repush")
def route_snt_billing_repush():
    return snt_billing_repush.home()


@app.route('/snt/upload_billing_extra', methods=['POST'])
def route_snt_upload_billing_extra():
    return snt_billing_repush.repush_billing()
    


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


@app.route('/api', methods=['GET', 'POST'])
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

        # __mail_to(
        #     subject="Receive API call",
        #     mail_body=body,
        #     receiver="yichen.wang@postnl.nl"
        # )

        output = {"success": "true", "errorCode": None,
                  "errorMsg": None, "cbCode": None, "wayBillNo": None}
        output = {
            "success": "true",
            "errorCode": None,
            "errorMsg": None
        }
        output = "{\"success\":\"true\"}"

        return jsonify(output)

# endregion
    

# region [main]
    
if __name__ == '__main__':
    # app.run(debug=True)
    app.run()

# endregion
