# Import from third-party
from flask import Flask, render_template, json, request, jsonify, session

def create_report():
    ids = []
    print(request.form)
    for form in request.form:
        if 'form-name-' in form:
            ids.append(form[len('form-name-')])
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
        form_possition = json.loads(form_possition)
        if form_type == "text" or form_type == "multiline_text":
            form_possition = request.form[str_form_possition + index]
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
            sub_ids = []
            for form in request.form:
                if 'form-possition-'+index in form:
                    sub_ids.append(form[len('form-possition-'+index)])
            for sub_id in sub_ids:
                
            res = {
                    "type": form_type,
                    "choices": {
                        "left": int(form_possition['x']),
                        "top": int(form_possition['y']),
                        "width": int(form_possition['width']),
                        "height": int(form_possition['height'])
                    }
                }
            output['forms'][form_name]= res
    print output
    return render_template('index.html', form_names=[])