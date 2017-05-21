from flask import Flask, make_response, request, current_app, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)



@app.route('/postmethod', methods = ['GET','POST'])
def get_post_javascript_data():
	mydata = request.json
	print mydata
	return 'It worked'



@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/test")
def hello2():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='192.168.1.7')
