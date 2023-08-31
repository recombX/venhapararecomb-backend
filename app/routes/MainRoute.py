from flask import jsonify, render_template
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")