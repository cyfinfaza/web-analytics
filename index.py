from datetime import datetime, timedelta
from flask import Flask, request, session, Response
import pymongo
from uuid import uuid4
import dotenv
from os import environ

dotenv.load_dotenv()
MONGODB_SECRET = environ.get("PVT_MONGODB")

client = pymongo.MongoClient(MONGODB_SECRET)
db = client.analytics
sessionsCollection = db.sessions
requestsCollection = db.requests

app = Flask(__name__)
app.secret_key = '--------' # DO NOT CHANGE THIS UNLESS YOU WANT ALL REGISTERED SESSIONS TO BREAK
app.permanent_session_lifetime = timedelta(days=365)
app.session_cookie_name = 'pvt_s'

@app.before_request
def make_session_permanent():
    session.permanent = True 

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
	if request.method == 'POST':
		if not 'track_id' in session:
			session['track_id'] = str(uuid4())
		url = request.data.decode('utf-8')
		agent = str(request.user_agent)
		if len(url)>200 or len(agent)>200:
			return Response("length limit exceeded", 400)
		sessionsCollection.update_one({'_id':session['track_id']}, {'$set':{'agent':agent}}, upsert=True)
		requestsCollection.insert_one({'track_id':session['track_id'], 'url':url, 't':datetime.utcnow()})
		return Response('ok', 201)
	if request.method == 'GET':
		if 'track_id' not in session:
			return Response("<code>invalid pvt_s</code>", 404)
		sess = sessionsCollection.find_one({'_id':session['track_id']})
		reqsC = requestsCollection.count_documents({'track_id':session['track_id']})
		if sess:
			return Response(f"<code>{sess['agent']}<br>{reqsC}</code>", 200)
		return Response("<code>no data</code>", 404)

if __name__ == "__main__":
	app.run(debug=True)