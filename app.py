from flask import Flask, request, render_template

app = Flask(__name__)

app.config.from_object("settings.DevelopmentConfig")

@app.route("/")
def index():
    return render_template("index.html")

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