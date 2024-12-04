from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


@app.route('/Home')
def Home():
    return render_template('index.html')

@app.route('/About')
def About():
    return render_template('about.html')


@app.route('/Packages')
def Packages():
    return render_template('packages.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)


