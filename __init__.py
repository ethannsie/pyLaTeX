import random
import datetime
import os
import sys
from flask import Flask, render_template, send_file
import json

app = Flask(__name__)
app.secret_key = os.urandom(32)
file_name = "02_03/10_59_23/"

@app.route("/", methods=['GET', 'POST'])
def home():
    global file_name
    return render_template(file_name + "latexFile.html")

@app.route("/pdf", methods=['GET', 'POST'])
def pdf():
    global file_name
    return render_template(file_name + "render_pdf.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
