# Import from third-party
from flask import Flask, render_template, json, request, jsonify, session

def create_new_form():
    form_name = ["Full name", "Gender", "Date of birth", "Country of birth"]
    return render_template('index.html', form_name=form_name)