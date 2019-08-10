# Import from third-party
from flask import Flask, render_template, json, request, jsonify, session

def create_report():
    ids = []
    print(request.form)
    for form in request.form:
        if 'form-name-' in form:
            ids.append(form[len('form-name-'):])
    print ids
    str_form_name = 'form-name-'
    str_form_possition = 'form-possition-'
    str_input_type = 'input-type-'
    output = {
        "forms": {}
    }
    for index in ids:
        form_name = str(request.form[str_form_name + index])
        form_type = str(request.form[str_input_type + index])
        if form_type == "text" or form_type == "multiline_text":
            form_possition = request.form[str_form_possition + index]
            form_possition = json.loads(form_possition)
            print("form_name = ", form_name, " | form_type = ", form_type, " | form_possition = ", form_possition)
            res = {
                    "type": form_type,
                    "position": {
                        "left": int(form_possition['x']),
                        "top": int(form_possition['y']),
                        "width": int(form_possition['width']),
                        "height": int(form_possition['height'])
                    }
                }
            output['forms'][form_name]= res
        elif form_type == "radio" or form_type == "checkbox":
            res = {
                    "type": form_type,
                    "choices": {
                        
                    }
                }
            sub_ids = []
            for form in request.form:
                if 'option-possition-'+index in form:
                    sub_ids.append(form[len('option-possition-'+index+'-'):])
            print sub_ids
            for sub_id in sub_ids:
                option_possition = request.form["option-possition-" + index + "-" + sub_id]
                option_possition = json.loads(option_possition)
                option_name = str(request.form["option-name-" + index + "-" + sub_id])
                sub_res = {
                    "position": {
                        "left": int(option_possition['x']),
                        "top": int(option_possition['y']),
                        "width": int(option_possition['width']),
                        "height": int(option_possition['height'])
                    },
                    "description": {
                        "haveDescription": False
                    }
                }
                res['choices'][option_name] = sub_res
            output['forms'][form_name]= res
    print output
    return render_template('index.html', form_names=[])