from flask import render_template,request
import json5

def home():
    return render_template('uniuni_relabel.html')

def uniuni_relabel_post():
    if request.method=='POST':
        param = json5.loads(request.form.get('param'))
        res = UNIUNI.relabel(param)
    return res