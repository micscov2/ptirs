from flask import Flask

app = Flask(__name__)

@app.route("/getPtirs")
def get_ptirs():
	return "ret: /getPtirs"

app.run(host="0.0.0.0", port=7421)
