from flask import Flask, jsonify, render_template
from model import db, Melon, MelonType, connect_to_db
from time import sleep

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
def home():

    return render_template('index.html')