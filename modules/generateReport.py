#import from standard library
import json
import math
import textwrap

# import from 3rd party library
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from flask import Flask, render_template, json, request, jsonify, session, send_file, redirect

def countVerticalLine(img, left, top, width, height):
    area = (left, top, left + width, top + height)
    cropped_img = img.crop(area)
    res = 0
    verLine = []
    for i in range(width):
        r, g, b = cropped_img.getpixel((i, height / 2))
        print(r, b, g)
        if (r < 220 or b < 220 or g < 220) and (len(verLine) > 0 and verLine[len(verLine) - 1] == False):
            res += 1
            verLine.append(True)
        else:
            verLine.append(False)
    print res
    return res

def process(path, userData):
    image_path = path[:-4] + "jpg"
    img = Image.open(image_path)
    jsonData = ""
    with open(path, "r") as f:
        jsonData = f.read()
    jsonData = json.loads(jsonData)
    server_data = jsonData.get('forms')
    draw = ImageDraw.Draw(img)
    
    for formText, formValue in userData.items():
        curServerData = {}
        for data in server_data:
            if data['label'] == formText:
                curServerData = data
        form_type = curServerData.get("type")
        print("form_type = ", form_type)
        if form_type == "text":
            userText = formValue
            pos = curServerData.get("position")
            x = pos.get('left')
            y = pos.get('top')
            verticalLines = countVerticalLine(img, pos.get('left'), pos.get('top'), pos.get('width'), pos.get('height'))
            
            if verticalLines > 1:
                width = pos.get('width')
                eachOWith = width / verticalLines
                for char in userText:
                    font_size = eachOWith
                    font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
                    text_size_width, text_size_height = draw.textsize(char, font=font)
                    draw.text((x + 4, y + (pos.get('height') - text_size_height) / 2), char, (0,0,0), font=font)
                    x = x + eachOWith
            else:
                font_size = pos.get('height')
                font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
                text_size_width, text_size_height = draw.textsize(formValue, font=font)
                x = x + (pos.get('width') - text_size_width) / 2
                draw.text((x, y), userText, (0,0,0), font=font)
        elif form_type == "radio":
            user_choice = formValue
            server_data_choice = curServerData.get("choices").get(user_choice)

            pos = server_data_choice.get("position")
            x = pos.get('left')
            y = pos.get('top')
            font_size = pos.get('height')
            font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
            text_size_width, text_size_height = draw.textsize("X", font=font)
            x = x + (pos.get('width') - text_size_width) / 2
            draw.text((x, y), 'X', (0,0,0), font=font)
        elif form_type == "checkbox":
            user_choices = formValue
            print "user_choices = ", user_choices
            for user_choice in user_choices:
                server_data_choice = curServerData.get("choices").get(user_choice)
                pos = server_data_choice.get("position")
                x = pos.get('left')
                y = pos.get('top')
                font_size = pos.get('height')
                font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
                text_size_width, text_size_height = draw.textsize("X", font=font)
                x = x + (pos.get('width') - text_size_width) / 2
                draw.text((x, y), 'X', (0,0,0), font=font)
        elif form_type == "multiline_text":
            userText = formValue
            pos = curServerData.get("position")
            x = pos.get('left')
            y = pos.get('top')
            for numOfCharPerLine in range(1, 1000):
                lines = textwrap.wrap(userText, width=numOfCharPerLine)
                if (len(lines) == 0): 
                    continue
                font_size = pos.get('height') / len(lines)
                font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
                text_size_width, text_size_height = draw.textsize(lines[0], font=font)
                # print ("text_size_width = ", text_size_width ,"numOfCharPerLine = ", numOfCharPerLine, "font_size = ", font_size, len(lines))
                if text_size_width <= pos.get('width') and ((text_size_width >= pos.get('width') * (0.6)) or (len(lines) == 1)):
                    break
                
            for line in lines:
                width, height = font.getsize(line)
                text_size_width, text_size_height = draw.textsize(line, font=font)
                x0 = x + (pos.get('width') - text_size_width) / 2
                draw.text((x0, y), line, (0,0,0), font=font)
                y += height

    # img.save('sample-out.jpg')
    # img.show()
    return img
    

def generateReport():
    # print(request.form)
    form_names = []
    for form in request.form:
        print("form ", form, request.form.get(form))
        if '_source' not in form:
            form_names.append(form)
            
    res = dict()

    for form_name in form_names:
        filePath = request.form.get(form_name + "_source")
        if filePath not in res:
            res[filePath] = {}
        if form_name not in res[filePath]:
            if '_checkbox_' in form_name:
                _form_name = form_name[:form_name.find("_checkbox_")]
                print "form_name = ", form_name, "|| request.form.get(form_name) = ", request.form.get(form_name)
                if _form_name not in res[filePath]:
                    res[filePath][_form_name] = [request.form.get(form_name)]
                else:
                    res[filePath][_form_name].append(request.form.get(form_name))
            else:
                print "form_name = ", form_name
                res[filePath][form_name] = request.form.get(form_name)
    
    list_imgs = []
    list_paths = []
    print filePath
    for filePath in res:
        list_paths.append(filePath)
        list_imgs.append(process(filePath, res[filePath]))
    # Sort the page
    for i in range(len(list_paths)):
        for j in range(i + 1, len(list_paths)):
            if (list_paths[i] > list_paths[j]):
                list_paths[i], list_paths[j] = list_paths[j], list_paths[i]
                list_imgs[i], list_imgs[j] = list_imgs[j], list_imgs[i]
    list_imgs[0].save("./static/outputPDF/output.pdf", save_all=True, append_images=list_imgs[1:])
    return redirect("/static/outputPDF/output.pdf", code=302)