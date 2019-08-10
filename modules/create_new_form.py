# Import from third-party
from flask import Flask, render_template, json, request, jsonify, session

def create_new_form():
    # for res in resp:
    form_names = ["Full name", "Gender", "Date of birth", "Country of birth"]
    return render_template('index.html', form_names=form_names)