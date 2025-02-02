import random
import datetime
import os
import sys
from flask import Flask, render_template, send_file
import json

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("02_02/13_31_53/latexFile.html")

@app.route("/pdf", methods=['GET', 'POST'])
def pdf():
    return render_template("02_02/13_31_53/render_pdf.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
