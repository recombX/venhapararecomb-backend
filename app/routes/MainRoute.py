from flask import jsonify
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({"api_version": "1.0.0",
                    "developed by": "Eduardo Henrique", 
                    "email": "duvrdx@gmail.com"})