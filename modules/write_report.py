# Import from standard library
import os
import json

# Import from third-party
from flask import Flask, render_template, json, request, jsonify, session

def write_report(universityName):
    path = './static/data/' + universityName
    form_datas = []
    for r, d, f in os.walk(path):
        for fs in f:
            if "json" in fs:
                filePath = path + '/' + fs
                with open(filePath, 'r') as f:
                    data = f.read()
                    jdata = json.loads(data)
                    for form in jdata["forms"]:
                        form["source"] = filePath
                        form_datas.append(form)
    return render_template('write_report.html', form_datas=form_datas)