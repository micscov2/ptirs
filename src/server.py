from flask import Flask
from flask import url_for
from orm_file import Ptir, User
from utils import get_response_object
import logging
import json

logging.basicConfig(filename="server.log", level=logging.DEBUG)

logger = logging.getLogger(__name__)
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
