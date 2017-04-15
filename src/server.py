from flask import Flask
from flask import url_for
from orm_file import Ptir, User
from utils import get_response_object
import json

app = Flask(__name__)

@app.route("/getPtirs")
def get_ptirs():
	data = get_response_object(Ptir.objects)
	response = app.response_class(
        			response=json.dumps(data),
        			status=200,
        			mimetype='application/json'
    		   )
	return response

@app.route("/getUsers")
def get_users():
	data = get_response_object(User.objects)
	response = app.response_class(
        			response=json.dumps(data),
        			status=200,
        			mimetype='application/json'
    		   )
	return response

app.run(host="0.0.0.0", port=7421)
