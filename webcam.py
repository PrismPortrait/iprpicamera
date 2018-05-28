from flask import Flask, send_from_directory
from picamera import PiCamera
import os

app = Flask(__name__)


@app.route("/")
def home():
	return "I'm a camera!"


@app.route("/capture/<filename>")
def capture(filename):
	camera = PiCamera()
	try:
		fullname = filename + '.jpg'
		camera.capture(fullname)
	finally:
		camera.close()
	return "Captured: " + fullname


@app.route("/download/<filename>")
def download(filename):
    try:
        return send_from_directory('.', filename + '.jpg')
    except:
        return filename + " not found."


@app.route("/delete/<filename>")
def delete(filename):
    try:
        os.remove(filename + '.jpg')
        return "Deleted: " + filename
    except OSError:
        return filename + " not found."


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
