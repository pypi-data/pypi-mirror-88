

from unittest import TestCase
from annt import load, hsv_to_rgb
from annt.box import Box

class TestAnnt(TestCase):

    def test_box_edge(self):
        new_box = Box(1, 'tag', 100, 200, 10, 10, 50, 50)
        self.assertEqual(new_box.left, 10)
        self.assertEqual(new_box.top, 10)
        self.assertEqual(new_box.right, 40)
        self.assertEqual(new_box.bottom, 140)

        new_box.right = 10
        self.assertEqual(new_box.w, 80)
        new_box.bottom = 10
        self.assertEqual(new_box.h, 180)
        new_box.top = 10
        self.assertEqual(new_box.y, 10)
        self.assertEqual(new_box.bottom, 10)
        new_box.left = 30
        self.assertEqual(new_box.x, 30)
        self.assertEqual(new_box.right, 10)

    def test_box_norm(self):
        # Normalzied values
        new_box = Box(1, 'tag', 100, 200, 10, 10, 50, 50)

        self.assertEqual(new_box.nx, 0.1)
        self.assertEqual(new_box.ny, 0.05)
        self.assertEqual(new_box.nw, 0.5)
        self.assertEqual(new_box.nh, 0.25)

        new_box.nx = 0.2
        new_box.ny = 0.1
        new_box.nw = 0.6
        new_box.nh = 0.3

        self.assertEqual(new_box.x, 20)
        self.assertEqual(new_box.y, 20)
        self.assertEqual(new_box.w, 60)
        self.assertEqual(new_box.h, 60)

