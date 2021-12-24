import random
import time

import flask
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/do_something', methods=['GET'])
def api_do_something():
    time.sleep(random.uniform(2, 5))
    return jsonify()


app.run()
