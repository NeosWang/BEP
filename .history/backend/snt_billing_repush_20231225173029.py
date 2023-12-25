from flask import render_template, request
from datetime import datetime
import json5
import json
import requests
import re

def home():
    return render_template('snt_billing_repush.html')

def repush_billing():
    if request.method == 'POST':
        
        # if 'file' not in request.files:
        #     return {
        #         "status": "fail",
        #         "data": 'no selected file'
        #     }
        file = request.files['file']

        # if file.filename == '':
        #     return {
        #         "status": "fail",
        #         'data': 'no selected file'
        #     }

        # if file and allowed_file(file.filename):
        #     pass
        #     # filename = secure_filename(file.filename)
        #     # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # else:
        #     return {
        #         "status": "fail",
        #         'data': f"only allow {str(_config.ALLOWED_EXTENSIONS)}"
        #     }

        df = process_billing_extra.process_billing_extra(file)
        attachment = "output.xlsx"
        df.to_excel(f"{_config.UPLOAD_FOLDER}/{attachment}", index=False)
        __mail_to("bill", "check attachment",
                    "yichen.wang@postnl.nl", attachment=attachment)

        return {
            "status": "success",
            'data': str(df.columns)
        }