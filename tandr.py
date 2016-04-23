from flask import Flask, render_template, url_for, request
from flask_oauthlib.client import OAuth
app = Flask(__name__)

app.secret_key = "Ayy lmao"

oauth_key="763519b5c8d1c478f44296c2b6c82dcb772dc4b0fbafa66b68d889cd41da4d71"
oauth_secret="6ecb90487aaf53377f8a0e536c7a4a4ba3b142bb972d838b1034858bd5e670e5"

tanda_url = "https://my.tanda.co/{}"
oauth = OAuth()

tanda_login = oauth.remote_app('tanda',
        base_url=tanda_url.format(""),
        request_token_url=None,
        access_token_url=tanda_url.format("api/oauth/token"),
        authorize_url=tanda_url.format("api/oauth/authorize"),
        request_token_params={'scope':'me'},
        consumer_key=oauth_key,
        consumer_secret=oauth_secret)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/rate")
def rate():
    return render_template("rate.html")

@app.route("/login")
def login():
    return tanda_login.authorize(callback="https://aqueous-anchorage-15078.herokuapp.com/login/callback",
        next=request.args.get('next') or request.referrer or None)

@app.route("/login/callback")
def oauth_authorized():
    return "Ayy lmao"

if __name__ == "__main__":
    app.run(debug=True)
