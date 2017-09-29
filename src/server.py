from flask import Flask
from flask import url_for, request, send_from_directory
from orm_file import Ptir, User
from utils import get_response_object
import random
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
	print(response)
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

@app.route("/updatePtir", methods=['POST'])
def update_ptir():
    body = json.loads(request.data)
    print("update : {}".format(body))
    if body["assignee"] in [None, ""] or body["reporter"] in [None, ""]:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: assignee/reporter is empty'}"),
                    status=400,
                    mimetype="application/json"
               )
        return response

    ptir = Ptir(
                    ptir_id=int(body["_id"]),
                    description=body["description"],
                    reporter=body["reporter"],
                    assignee=body["assignee"],
                    status=body["status"],
                    severity=body["severity"]
               )
    try:
        ptir.save()
    except Exception:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: validation error'}"),
                    status=400,
                    mimetype="application/json"
               )
        return response
        
    response = app.response_class(
                response=json.dumps("{'status': 'ok'}"),
                status=200,
                mimetype="application/json"
           )
    return response

@app.route("/addPtir", methods=['POST'])
def add_ptir():
    body = json.loads(request.data)
    if body["assignee"] in [None, ""] or body["reporter"] in [None, ""]:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: assignee/reporter is empty'}"),
                    status=400,
                    mimetype="application/json"
               )
        return response

    ptir = Ptir(
                    ptir_id=random.randint(1, 100000), 
                    description=body["description"],
                    reporter=body["reporter"],
                    assignee=body["assignee"],
                    status=body["status"],
                    severity=body["severity"]
               )
    try:
        ptir.save()
    except Exception:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: validation error'}"),
                    status=400,
                    mimetype="application/json"
               )
        return response
        
    response = app.response_class(
                response=json.dumps("{'status': 'ok'}"),
                status=200,
                mimetype="application/json"
           )
    return response


@app.route("/addUser", methods=['POST'])
def add_user():
	body = json.loads(request.data)
	user = User(body["name"], body["password"])
	user.save()

	response = app.response_class(
				response=json.dumps("{'status': 'ok'}"),
				status=200,
				mimetype="application/json"
		   )

	return response

@app.route("/<path:path>")
def home_index(path):
    return send_from_directory("static", path)


print("Server listening on port 7421")
app.run(host="0.0.0.0", port=7421)
