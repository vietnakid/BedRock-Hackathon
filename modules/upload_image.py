import vision_api as vapi
from flask import Flask, render_template, json, request, jsonify, session, redirect, url_for
import numpy as np
import cv2

def detectLine_AcuracyResult(_result, path):
    
    gray = cv2.imread(path)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    minLineLength=70
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=2)

    a,b,c = lines.shape
    line_detected = []
    for i in range(a):
        line_detected.append(((lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3])))
        print((((lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]))))

    # print _result
    result = []
    for rindex in range(len(_result)):
        res = _result[rindex]
        curmin = 99999999999999
        minLine = -1
        pos = res.get('position')
        x0 = pos.get('x') + pos.get('width')
        y0 = pos.get('y') + pos.get('height')
        for index in range(len(line_detected)):
            line = line_detected[index]
            x1 = line[0][0]
            y1 = line[0][1]
            distance = (x1-x0)*(x1-x0) + (y1-y0)*(y1-y0)
            if distance < curmin:
                curmin = distance
                minLine = index

        if minLine != -1:
            _result[rindex]['position']['x'] = int(line_detected[minLine][0][0])
            _result[rindex]['position']['y'] = int(line_detected[minLine][0][1]) - int(_result[rindex]['position']['height'])
            _result[rindex]['position']['width'] = int(abs((line[0][0] - line[1][0])))
    return _result

def transfer_data(path, folder_path=""):
    json_text = vapi.detect_text(path)
    result = vapi.convert_data(json_text)
    result = detectLine_AcuracyResult(result, path)
    return render_template('index.html', results=result, path=path)

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

def check_not_complete_form(folder_path):
    from os import walk
    f = []
    for (dirpath, dirnames, filenames) in walk(folder_path):
        f.extend(filenames)
        break
    for file_name in f:
        if 'jpg' in file_name and file_name.replace('jpg', 'json') not in f:
            return transfer_data(folder_path + "/" + file_name, folder_path)
    dirnames = get_all_folder()
    return render_template('check-form.html', dirnames=dirnames)