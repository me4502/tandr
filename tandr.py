from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html");

@app.route("/login")
def login():
    return "ayy lmao"

if __name__ == "__main__":
    app.run()
