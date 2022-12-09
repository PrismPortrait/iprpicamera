import os
import socket
from threading import RLock, Thread

from flask import Flask, send_from_directory
from picamera import PiCamera

app = Flask(__name__)

# Pull camera number from hostname.
camera_num = socket.gethostname()[-1]
# Init camera where both API and udp can use.
camera = PiCamera()
camera_lock = RLock()

img_dir='/tmp/prismportrait/'
os.makedirs(img_dir)

@app.route("/")
def home():
    return "I'm a camera!"


@app.route("/capture/<filename>")
def capture(filename):
    fullname = filename + '.jpg'
    with camera_lock:
        camera.capture(img_dir + fullname)
    return "Captured: " + fullname


@app.route("/download/<filename>")
def download(filename):
    try:
        return send_from_directory(img_dir, filename + '.jpg')
    except:
        return filename + " not found."


@app.route("/delete/<filename>")
def delete(filename):
    try:
        os.remove(img_dir + filename + '.jpg')
        return "Deleted: " + filename
    except OSError:
        return filename + " not found."


def udp_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 40000))

    while True:
        # Capture image to received filename.
        # TODO: Investigate faster options than just calling .capture
        sock.recv(1024)
        with camera_lock:
            camera.capture(img_dir + camera_num + ".jpg")


if __name__ == "__main__":
    try:
        # Start receiver as daemon, it will close if main thread closes.
        udp_thread = Thread(target=udp_receiver)
        udp_thread.daemon = True
        udp_thread.start()
        app.run(host='0.0.0.0', port=80, debug=False)
    finally:
        if camera is not None:
            camera.close()
