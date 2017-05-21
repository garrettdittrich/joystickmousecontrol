from flask import Flask, make_response, request, current_app
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)



@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():

    jsdata = request.form['javascript_data']
    return jsdata



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def hello2():
    return "Hello World!"

if __name__ == "__main__":
    app.run()