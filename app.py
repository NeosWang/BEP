import os 
from flask import Flask, request, render_template, jsonify, send_from_directory 
from backend import data_processor

app = Flask(__name__)

app.config.from_object("settings.DevelopmentConfig")

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'jads.png', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    links, nodes = data_processor.get_data()
    return render_template("test.html", links=links, nodes=nodes)


@app.route("/login")
def login_main():
    name = request.values.get("name")
    pwd = request.values.get("pwd")
    return f"name={name}, pwd={pwd}"


@app.route("/request")
def request_main():
    id = request.values.get("id")
    return f"""
    <form action="/login">
        id:<input name="name" value="{id}"><br>
        pwd:<input name = "pwd">
        <input type="submit">
    <form>
    """


if __name__ == '__main__':
    app.run()
