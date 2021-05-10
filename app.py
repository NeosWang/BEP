import os 
from flask import Flask, request, render_template, jsonify, send_from_directory 
from backend import data_processor

from flask_fontawesome import FontAwesome

app = Flask(__name__)

app.config.from_object("settings.DevelopmentConfig")

fa = FontAwesome(app)
@app.route('/favicon.ico') 
def favicon(): 

    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'jads.png', 
                               mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    links, nodes = data_processor.get_data()
    return render_template("test.html", links=links, nodes=nodes)






if __name__ == '__main__':
    app.run()
