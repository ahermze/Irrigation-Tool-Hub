from backend.func_new import *
import os
from lib2to3.pgen2.pgen import DFAState
from flask import Flask, request, redirect, url_for, render_template, flash, Blueprint, abort
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import openweather
from backend.wiseprocess import *
from backend.ETrprocess import *
from backend.Kc_process import *
from backend.wiseET import *

from backend.merged_process import *

app = Flask(__name__)
Bootstrap(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
OUTPUT_DIR = "static"
upload_dir = "./excel_files/"
app.config["UPLOAD_FOLDER"] = "./excel_files/"

@app.route("/")
def index():
    return render_template("/base/index.html")

@app.route("/return_upload")
def return_upload():
    return render_template("/base/upload.html")

@app.route("/upload")
def upload():
    return render_template("/base/upload.html")

@app.route("/both")
def both():
    return render_template("/base/both.html")

@app.route("/wiseupload")
def wiseupload():
    return render_template("/base/WISE_upload.html")

@app.route("/merge_upload")
def merge_upload():
    return render_template("/base/merge_upload.html")


# Not used :(
@app.route("/themap")
def themap():
    # if request.method == ["POST"]:
    return render_template("/base/themap.html")

# Not used :(
@app.route("/aftermap")
def aftermap():
    if request.method == "GET":
        # print(request.cookies.get('radius'))
        # weather_data = noaa.get_weather(request.cookies.get('latitude'), request.cookies.get('longitude'))
        # noaa.find_station(request.cookies.get('latitude'), request.cookies.get('longitude'))
        # return render_template("/base/aftermap.html", weather_data=weather_data)
        result = openweather.get_weather(request.cookies.get('latitude'), request.cookies.get('longitude'))
        # print(result)
        return render_template("/base/aftermap.html", weather_data=result)


@app.route("/upload", methods=["POST"])
def upload_file():
    global filename_
    if request.method == "POST":
        if "file" not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            print("No selected file")
            return redirect(request.url)
        if file:
            filename_ = file.filename
            file_ext = os.path.splitext(filename_)[1]
            if file_ext != ".xlsx":
                abort(400)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_))

        return render_template("/base/upload_success_2nd.html")


@app.route("/upload_success_2nd", methods=["GET", "POST"])
def upload_success_2nd():
    try:    
        if request.method == "POST":
            full_name = upload_dir + filename_
            global treatment    
            treatment = request.form["treatment"]

            global start_DOY
            start_DOY = request.form["start_DOY"]
            start_DOY = int(start_DOY)

            global end_DOY
            end_DOY = request.form["end_DOY"]
            end_DOY = int(end_DOY)

            start_hour = request.form["start_hour"]
            start_hour = int(start_hour)
            end_hour = request.form["end_hour"]
            end_hour = int(end_hour)
            select_hour = request.form["select_hour"]
            select_hour = int(select_hour)
            print("NEXT")
            plot_buttons(
                full_name, start_DOY, end_DOY, treatment, start_hour, end_hour, select_hour
            )
            return render_template("/base/result.html")

        return render_template("/base/upload_success_2nd.html")
    except Exception as e:
        error_message = str(e)
        return render_template("/base/upload_success_2nd.html", error_message=error_message)


@app.route("/merge_upload", methods=["POST"])
def merge_upload_file():
    global filename_
    if request.method == "POST":
        if "file" not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            print("No selected file")
            return redirect(request.url)
        if file:
            filename_ = file.filename
            file_ext = os.path.splitext(filename_)[1]
            if file_ext != ".xlsx":
                abort(400)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_))

        return render_template("/base/merge_success.html")

@app.route("/merge_success", methods=["GET", "POST"])
def merge_success():
    try:    
        if request.method == "POST":
            full_name = upload_dir + filename_
            global treatment    
            treatment = request.form["treatment"]

            global start_DOY
            start_DOY = request.form["start_DOY"]
            start_DOY = int(start_DOY)

            global end_DOY
            end_DOY = request.form["end_DOY"]
            end_DOY = int(end_DOY)

            start_hour = request.form["start_hour"]
            start_hour = int(start_hour)
            end_hour = request.form["end_hour"]
            end_hour = int(end_hour)
            select_hour = request.form["select_hour"]
            select_hour = int(select_hour)
            print("NEXT")
            plot_the_buttons(
                full_name, start_DOY, end_DOY, treatment, start_hour, end_hour, select_hour
            )
            return render_template("/base/merge_result.html")

        return render_template("/base/merge_success.html")
    except Exception as e:
        error_message = str(e)
        return render_template("/base/merge_success.html", error_message=error_message)


@app.route("/wiseupload", methods=["POST"])
def upload_wise_file():
    global filename_
    if request.method == "POST":
        if "file" not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            print("No selected file")
            return redirect(request.url)
        if file:
            filename_ = file.filename
            file_ext = os.path.splitext(filename_)[1]
            if file_ext != ".xlsx":
                abort(400)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_))

        wiseET_processfile()
        return render_template("/base/wiseET.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, threaded=False, debug=True)