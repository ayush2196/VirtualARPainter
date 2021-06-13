import os
from flask import Flask, render_template, request, send_from_directory, Response
from gestureVolumeControl import get_frame
from arPainter import Painter

app = Flask(__name__)

app.config["CACHE_TYPE"] = "null"


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(Painter(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route("/arPainter")
# def arPainter():
#     # file = open(r'/arPainter.py', 'r').read()
#     # return exec(file)
#     return arPainter.Painter()


if __name__ == "__main__":
    app.run(port=4998, debug=True)
