from flask import Flask, send_from_directory
from picamera import PiCamera

app = Flask(__name__)

@app.route("/")
def home():
	return "I'm a camera!"

@app.route("/capture/<filename>")
def capture(filename):
	try:
		camera = PiCamera()
		fullname = filename + '.jpg'
		camera.capture(fullname)
	finally:
		camera.close()
	return "Captured: " + fullname

@app.route("/download/<filename>")
def download(filename):
	return send_from_directory('.', filename + '.jpg')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)


