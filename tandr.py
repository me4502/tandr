import random 
import json
from flask import Flask, render_template, url_for, request, redirect, session
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
        access_token_method='POST',
        authorize_url=tanda_url.format("api/oauth/authorize"),
        request_token_params={'scope':'me user'},
        consumer_key=oauth_key,
        consumer_secret=oauth_secret
        )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rate")
def rate():
    data = request.form
    if session.get("sorted_everyone"):
        return render_template("priorities.html")

    if not session.get("unsorted_list"):
        session['unsorted_list'] = tanda_login.request('/api/v2/users')

    if not session.get("comparisonsMade")
        session['comparisonsMade'] = [""]

    return render_template("rate.html")

@app.route("/api/rate", methods=["POST"])
def rate_api():
    # Append the unique set
    session['comparisonsMade'].append(set([data['up'], data['down']]))
    #Insert the 
    if data['upIsFirst']:
        session['sorted_everyone'].insert(
            session['sorted_everyone'].index(tanda_login.request('/api/v2/users/{}/'.format(data['up']))),
                session['unsorted_list'].pop()
        )
    elif data['down'] == session['sorted_everyone'][-1]['id']:
        session['sorted_everyone'].append(session['unsorted_list'].pop())
    return "OK"

@app.route("/api/burn", methods=["POST"])
def burn_handler():
    print(data)
    print(session)
    data = request.form
    if not session.get("sorted_everyone"):
        session['sorted_everyone'] = [tanda_login.request('api/v2/users/{}/'.
                                      format(data['id']).data]
    else:
        session['sorted_everyone'].append(tanda_login.request('api/v2/users/{}/'.format(data['id']).data)
    return "OK"


@app.route("/api/user")
def give_pair():
    if session.get("sorted_everyone"):
        return json.dumps(None)

    if not session.get("unsorted_list"):
        session['unsorted_list'] = tanda_login.request('/api/v2/users')
    
    for i in range(len(session.get('unsorted_list'))):
        possibleComparison = (session.get('unsorted_list')[-1], session.get('sorted_everyone')[i])
        if (set(possibleComparison) not in session.get('comparisonsMade')):
            comparison = possibleComparison
    return "[{},{}]".format(json.dumps(comparison[0]), json.dumps(comparison[1]))

@app.route("/api/result", methods=["POST"])
def result_handler():
    return ""

@app.route("/login")
def login():
    return tanda_login.authorize(
            #callback="https://aqueous-anchorage-15078.herokuapp.com/login/callback",
            callback=url_for('oauth_authorized',_external=True),
            state={ 'next': request.args.get('next') or request.referrer or None }
        )

@app.route("/login/callback")
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')
    resp = tanda_login.authorized_response()

    if resp is None:
        flash(u'Invalid login')
        return redirect(next_url)
    session['tanda_token'] = (resp['access_token'], '')
    session['user'] = tanda_login.request('api/v2/users/me').data
    return redirect(next_url)

@tanda_login.tokengetter
def get_tanda_token(token=None):
    return session.get('tanda_token')

if __name__ == "__main__":
    app.run(debug=True)
