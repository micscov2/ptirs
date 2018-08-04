from flask import Flask
from flask import url_for, request, send_from_directory
from datetime import datetime
from orm_file import Ptir, User, Secret
from utils import get_response_object
from send_email import send_email
import random
import logging
import json

logging.basicConfig(filename="server.log", level=logging.DEBUG)

logger = logging.getLogger(__name__)
app = Flask(__name__)
CTR_VAR = 1

@app.route("/getPtirs/<filter>/<keyphrase>")
def get_ptirs(filter, keyphrase):
    print(filter)
    if (keyphrase != Secret.objects[0].secr):
        return app.response_class(
                    response=json.dumps(dict()),
                    status=200,
                    mimetype='application/json'
               )            
    if filter in ['OPEN', 'IN PROGRESS']:
        data = get_response_object(Ptir.objects(status=filter))
    else:
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
                    severity=body["severity"],
                    modified_on=str(datetime.now()),
                    created_on=body.get('created_on')
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
    global CTR_VAR
    print("Adding PTIR ID: {}".format(CTR_VAR))
    body = json.loads(request.data)
    if body["assignee"] in [None, ""] or body["reporter"] in [None, ""]:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: assignee/reporter is empty'}"),
                    status=400,
                    mimetype="application/json"
               )
        return response

    if User.objects(name=body["assignee"]) and User.objects(name=body["reporter"]):
        pass
    else:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: assignee/reporter is not registered'}"),
                    status=400,
                    mimetype="application/json"
               )
        return response
        

    ptir = Ptir(
                    ptir_id=CTR_VAR,
                    description=body["description"],
                    reporter=body["reporter"],
                    assignee=body["assignee"],
                    status=body["status"],
                    severity=body["severity"],
                    created_on=str(datetime.now()),
                    created_by=body['reporter']
               )
    try:
        ptir.save()
        CTR_VAR += 1
    except Exception:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: validation error'}"),
                    status=400,
                    mimetype="application/json"
               )
        return response
    send_email(ptir.assignee, ptir.ptir_id, ptir.description) 
    response = app.response_class(
                response=json.dumps("{'status': 'ok'}"),
                status=200,
                mimetype="application/json"
           )
    return response


@app.route("/addUser", methods=['POST'])
def add_user():
    body = json.loads(request.data)
    user = User(
                name=body["name"],
                password=body["password"],
                email=body["email"],
                role=body["role"]
               )
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


print("Server listening on port 7421/index.html")
CTR_VAR = len(Ptir.objects()) + 1
app.run(host="0.0.0.0", port=7421)
