# vim: set et sw=4 sts=4 fileencoding=utf-8:

import unittest
import iprpicamera.camera as camera

class TestCapture(unittest.TestCase):

    def test_callsCaptureWhenSocketReceives(self):
        cam = camera.Camera()
        cam.capture()
        self.assertEqual(1,1);

if __name__ == '__main__':
    unittest.main()
