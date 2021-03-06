import random
import logging
import json
import threading

from flask import Flask
from datetime import datetime
from flask import url_for, request, send_from_directory

from orm_file import Ptir, User, Secret
from utils import get_response_object, check_all_files_present
from send_email import send_email

logging.basicConfig(filename="../logs/server.log", level=logging.DEBUG)

logger = logging.getLogger(__name__)
app = Flask(__name__)
CTR_VAR = 1

def send_email_thread_func(assignee, ptir_id, description):
    send_email(assignee, ptir_id, description) 

@app.route("/getPtirs/<filter>/<keyphrase>")
def get_ptirs(filter, keyphrase):
    print(filter)
    if (keyphrase != Secret.objects[0].secr):
        return app.response_class(
                    response=json.dumps(dict()),
                    status=200,
                    mimetype='application/json'
               )            
    if filter == 'OPEN' or filter == 'IN PROGRESS':
        data = get_response_object(Ptir.objects(status=filter))
    elif filter == 'OPEN,IN PROGRESS':
        data1 = get_response_object(Ptir.objects(status='OPEN'))
        data2 = get_response_object(Ptir.objects(status='IN PROGRESS'))
        data = data1 + data2
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

    if len(Ptir.objects(ptir_id=int(body["_id"]))) != 1:
        response = app.response_class(
                    response=json.dumps("{'status': 'error: PTIR with id: " + body["_id"] + " not found'}"),
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
    threading.Thread(target=send_email_thread_func, args=(ptir.assignee, ptir.ptir_id, ptir.description)).start()
    print "Returning response now"
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
ctr_2 = 0 # Global var, very bad idea need to be replaced
for item in Ptir.objects():
    ctr_2 = max(ctr_2, item.id)
CTR_VAR = ctr_2 + 1
print("PTIR number starting from : {}".format(CTR_VAR))

if check_all_files_present(["cert.pem", "key.pem"]):
    app.run(host="0.0.0.0", port=7421, ssl_context=('cert.pem', 'key.pem'))
else:
    app.run(host="0.0.0.0", port=7421)
