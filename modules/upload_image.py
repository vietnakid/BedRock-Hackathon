import vision_api as vapi
from flask import Flask, render_template, json, request, jsonify, session, redirect, url_for

def transfer_data(path):
    json_text = vapi.detect_text(path)
    result = vapi.convert_data(json_text)
    _result = json.loads(result)
    return render_template('index.html', results=_result, path=path)

def create_file_name(folder_path):
    from os import walk
    f = []
    for (dirpath, dirnames, filenames) in walk(folder_path):
        f.extend(filenames)
        break
    laggest_number = 0
    for file_name in f:
        if ('jpg') in file_name:
            _file_name = file_name.replace('.png', '').replace('.jpg', '')
            _int_name = int(_file_name)
            if _int_name > laggest_number:
                laggest_number = _int_name
    if len(str(laggest_number)) == 2 or laggest_number == 9:
        return str(laggest_number + 1) + ".jpg"
    elif len(str(laggest_number)) == 1:
        return "0" + str(laggest_number + 1) + ".jpg"

def get_all_folder():
    path = 'static/data'
    from os import walk
    d = []
    for (dirpath, dirnames, filenames) in walk(path):
        d.extend(dirnames)
        break
    return d