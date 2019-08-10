# Import from third-party
from flask import Flask, render_template, json, request, jsonify, session, redirect, url_for

webApp = Flask(__name__)

@webApp.route("/")
def main():
    import modules.create_new_form as create_new_form
    return create_new_form.create_new_form()


@webApp.route("/createReport", methods=['POST'])
def createReport():
    import modules.createReport as createReport
    return createReport.create_report()

if __name__ == "__main__":
    webApp.run(debug=True)