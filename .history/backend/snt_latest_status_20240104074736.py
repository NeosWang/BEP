from flask import render_template

def home():
    return render_template('snt_latest_status.html')