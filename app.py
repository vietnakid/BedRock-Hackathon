from flask import Flask, render_template, json, request, jsonify, session, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

app.config["IMAGE_UPLOADS"] = "static/data"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image saved")
                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                return redirect(request.url)
    return render_template("upload-image.html")

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(debug=True)


