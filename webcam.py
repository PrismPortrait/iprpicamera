import os
import socket
from threading import RLock, Thread

from flask import Flask, send_from_directory
from picamera import PiCamera

app = Flask(__name__)


@app.route("/")
def home():
    return "I'm a camera!"


@app.route("/capture/<filename>")
def capture(filename):
    fullname = filename + '.jpg'
    with camera_lock:
        camera.capture(fullname)
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


def udp_receiver(camera, camera_num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 40000))

    while True:
        # Capture image to received filename.
        # TODO: Investigate faster options than just calling .capture
        sock.recv(1024)
        with camera_lock:
            camera.capture(camera_num + ".jpg")


if __name__ == "__main__":
    camera = None
    try:
        # Pull camera number from hostname.
        camera_num = socket.gethostname()[-1]
        # Init camera where both API and udp can use.
        camera = PiCamera()
        camera_lock = RLock()
        # Start receiver as daemon, it will close if main thread closes.
        udp_thread = Thread(target=udp_receiver, args=(camera, camera_num))
        udp_thread.daemon = True
        udp_thread.start()
        app.run(host='0.0.0.0', port=80, debug=True)
    finally:
        if camera is not None:
            camera.close()
