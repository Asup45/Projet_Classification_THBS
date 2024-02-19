import flask
import pickle
from flask import Flask, render_template, request

app=Flask(__name__)
@app.route('/')
def index():
    return flask.render_template('index.html')
@app.route('/predict',methods = ['POST'])
def result():
    if request.method == 'POST':
        # logique de prediction
        return render_template('predict.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)