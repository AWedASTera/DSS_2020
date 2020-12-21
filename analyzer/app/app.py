import json

from flask import Flask, render_template

app = Flask(__name__)

dfdata = []
@app.route('/')
def hello():
	print(dfdata[0])
	return render_template('index.html', dfdata=dfdata)

if __name__ == "__main__":
    with open("data_file.json", "r") as read_file:
        dfdata = json.load(read_file)
    app.run(host='0.0.0.0', port=4000)