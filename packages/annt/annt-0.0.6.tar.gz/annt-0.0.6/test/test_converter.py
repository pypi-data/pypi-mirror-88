

from unittest import TestCase
import pkg_resources
import os
import numpy as np
import cv2

from annt import converter
from annt.box import Box


def load_testdata(filename):
    path = pkg_resources.resource_string(__name__, filename)
    return path

def generate_testdata_loader(image_dir):
    def __loader(filename, flags):
        filepath = os.path.join(image_dir, filename)
        with pkg_resources.resource_stream(__name__, filepath) as fp:
            b = fp.read()
        arr = np.frombuffer(b, dtype=np.int8)
        return cv2.imdecode(arr, flags)
    return __loader

class TestConverter(TestCase):
    
    def test_pascal(self):
        """ Load pascalVOC 2007 and check all attributes are appropriate.
        """
        image_dir = 'test_data'
        filename = 'test_data/voc2007.xml'
        pascal_text = load_testdata(filename)
        annotation = converter.load_pascal_voc(pascal_text, generate_testdata_loader(image_dir))
        self.assertEqual(annotation.filename, "voc2007.jpg")
        self.assertEqual(annotation.get_option("folder"), "VOC2007")
        for box in annotation.boxes:
            self.assertIsNotNone(box.get_option("pose"))
            self.assertIsNotNone(box.get_option("difficult"))
            self.assertIsNotNone(box.get_option("truncated"))
        annotation.show()
