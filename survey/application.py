import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    
    # take the request the user made, access the form,
    name = request.values.get("name") 
    # and store the field called `name` in a Python variable also called `name`
    radio = request.values.get("radio") 
    menu = request.values.get("menu")
    if not name: 
        print("ou")
        print("<b> no name</b>")
        return render_template("error.html", message="Invalid missing name")
    if not radio:
        return render_template("error.html", message="Invalid radio")
#    if not menu:
#        return render_template("error.html", message="yakamtzan! bring somthing")
        
    # print("dfhdf")
    # csv file writing
    with open('survey.csv', 'a') as csvFile:
        fieldnames = ['name', 'attending', 'bringing']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
       # writer.writeheader()
        writer.writerow({"name": request.form.get("name"), "attending": request.form.get(
            "radio"), "bringing": request.form.get("menu")})
    csvFile.close()
    return redirect("/sheet")
    

@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open('survey.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        myinput = list(reader)
    return render_template("sheet.html", result=myinput)
