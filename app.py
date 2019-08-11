from flask import Flask, render_template, json, request, jsonify, session, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def main():
    import modules.create_new_form as create_new_form
    return create_new_form.create_new_form()

@app.route("/createReport", methods=['POST'])
def createReport():
    import modules.createReport as createReport
    return createReport.create_report()

@app.route("/generateReport", methods=['POST'])
def generateReport():
    import modules.generateReport as generateReport
    return generateReport.generateReport()

@app.route("/writeReport/<universityName>")
def writeReport(universityName):
    import modules.write_report as write_report
    return write_report.write_report(universityName)

@app.route("/userMode")
def userMode():
    import modules.userMode as userMode
    return userMode.userMode()

# app.config["IMAGE_UPLOADS"] = "static/data"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    from modules import upload_image as up
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if request.form['other-university']:
                uni = request.form['other-university']
            elif request.form['university']:
                uni = request.form['university']
            path_upload = "static/data/" + uni
            if image.filename == "":
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = up.create_file_name(path_upload)
                print filename
                try:
                    os.mkdir(path_upload)
                except:
                    # print "Folder already exists"
                    pass
                image.save(os.path.join(path_upload, filename))
                return up.transfer_data(path_upload + "/" + filename)
            else:
                return redirect(request.url)
    dirnames = up.get_all_folder()
    return render_template("upload-image.html", dirnames=dirnames)

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def to_pretty_json(value):
    return json.dumps(value)

app.jinja_env.filters['tojson_pretty'] = to_pretty_json

if __name__ == "__main__":
    app.run(debug=True)


