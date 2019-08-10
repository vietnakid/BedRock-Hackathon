import vision_api as vapi
from flask import Flask, render_template, json, request, jsonify, session, redirect, url_for

def transfer_data(path):
    json_text = vapi.detect_text(path)
    result = vapi.convert_data(json_text)
    return render_template('add-template.html', result=result)