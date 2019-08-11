# Import from standard library
import os

# Import from third-party
from flask import Flask, render_template, json, request, jsonify, session

def userMode():
    path = './static/data'
    files = []
    # r=root, d=directories, f = files
    directories = []
    for r, d, f in os.walk(path):
        directories.extend(d)
    print(directories)
    return render_template('userMode.html', universities=directories)