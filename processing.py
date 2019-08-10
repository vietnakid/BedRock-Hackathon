#import from standard library
import json
import math
import textwrap

# import from 3rd party library
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def process(userData):
    path = "./data/{}/".format(data.get('university'))
    img = Image.open(path + "04.jpg")
    jsonData = ""
    with open(path + "04.json", "r") as f:
        jsonData = f.read()
    jsonData = json.loads(jsonData)
    server_data = jsonData.get('forms')
    draw = ImageDraw.Draw(img)
    
    for formText, formValue in userData.get('forms').items():
        curServerData = server_data.get(formText)
        form_type = curServerData.get("type")
        if form_type == "text":
            userText = formValue

            pos = curServerData.get("position")
            x = pos.get('left')
            y = pos.get('top')
            font_size = pos.get('height')
            font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
            text_size_width, text_size_height = draw.textsize(formValue, font=font)
            x = x + (pos.get('width') - text_size_width) / 2
            draw.text((x, y), userText, (0,0,0), font=font)
        elif form_type == "radio":
            user_choice = formValue.get("choice")
            user_description = formValue.get("description")
            server_data_choice = curServerData.get("choices").get(user_choice)

            pos = server_data_choice.get("position")
            x = pos.get('left')
            y = pos.get('top')
            font_size = pos.get('height')
            font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
            text_size_width, text_size_height = draw.textsize("X", font=font)
            x = x + (pos.get('width') - text_size_width) / 2
            draw.text((x, y), "X", (0,0,0), font=font)

            if server_data_choice.get("description").get("haveDescription"):
                pos = server_data_choice.get("description").get("position")
                x = pos.get('left')
                y = pos.get('top')
                font_size = pos.get('height')
                font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
                text_size_width, text_size_height = draw.textsize(user_description, font=font)
                x = x + (pos.get('width') - text_size_width) / 2
                draw.text((x, y), user_description, (0,0,0), font=font)
        elif form_type == "checkbox":
            user_choices = formValue.get("choice")
            for user_choice_dict in user_choices:
                user_choice = user_choice_dict.get('value')
                user_description = user_choice_dict.get("description")
                server_data_choice = curServerData.get("choices").get(user_choice)

                pos = server_data_choice.get("position")
                x = pos.get('left')
                y = pos.get('top')
                font_size = pos.get('height')
                font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
                text_size_width, text_size_height = draw.textsize("X", font=font)
                x = x + (pos.get('width') - text_size_width) / 2
                draw.text((x, y), "X", (0,0,0), font=font)

                if server_data_choice.get("description").get("haveDescription"):
                    pos = server_data_choice.get("description").get("position")
                    x = pos.get('left')
                    y = pos.get('top')
                    font_size = pos.get('height')
                    font = ImageFont.truetype(r'./font/times-new-roman.ttf', font_size)
                    text_size_width, text_size_height = draw.textsize(user_description, font=font)
                    x = x + (pos.get('width') - text_size_width) / 2
                    draw.text((x, y), user_description, (0,0,0), font=font)
        elif form_type == "multiline_text":
            userText = formValue
            pos = curServerData.get("position")
            x = pos.get('left')
            y = pos.get('top')
            for numOfCharPerLine in range(1, 1000):
                lines = textwrap.wrap(userText, width=numOfCharPerLine)
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
    img.show()


if __name__ == "__main__":
    data = {
        "university": "Washington AndLeeUniversity",
        "forms": {
            "Full name": "Nguyen Anh Viet",
            "Gender": "Male",
            "Primary source of family income": {
                "choice": "Other",
                "description": "Hello"
            }
        }
    }
    data = {
        "university": "SOKA",
        "forms": {
            "Full name": "Text is preferably wrapped on whitespaces and right after the hyphens in.",
            "Born on or after": {
                "choice": [
                    {"value": "Yes", "description": ""},
                    {"value": "No", "description": ""}
                ]
            }
        }
    }
    process(data)
    