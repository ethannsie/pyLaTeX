import random
import datetime
import os
import sys
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import json

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html", )

if __name__ == '__main__':
    app.debug = True
    app.run()
