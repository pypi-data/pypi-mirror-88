
from unittest import TestCase
from annt import load, hsv_to_rgb
from annt.box import Box

class TestAnnt(TestCase):

    def test_load(self):
        path = "/Users/keisuke/Dropbox/アプリ/annt/test2/"
        annotations = load(path)
        for annotation in annotations:
            for box in annotation.boxes:
                f = "left-top-right-bottom: {}-{}-{}-{}"

    def test_preprocess(self):
        path = "/Users/keisuke/Dropbox/アプリ/annt/test2/"
        annotations = load(path)
        for a in annotations:
            a = a.rotate(5)
            a = a.resize(500, 500)
            a = a.flip(True, True)
            a.show()

class TestColor(TestCase):

    def test_hsv_to_rgb(self):
        colors = [
            ((255, 0, 0), (0, 1, 1)),
            ((255, 255, 255), (0, 0, 1)),
            ((85, 89, 153), (237, 0.44, 0.60)),
        ]
        for rgb, hsv in colors:
            self.assertTupleEqual(rgb, hsv_to_rgb(*hsv))

if __name__ == "__main__":
    unittest.main()