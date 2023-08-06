
from unittest import TestCase
from annt import Loader

class TestLoader(TestCase):

    def test_loader(self):
        path = "/Users/keisuke/Dropbox/アプリ/annt/test2/"
        loader = Loader(path)

        load_generator = loader.load()
        for annotation in load_generator:
            pass