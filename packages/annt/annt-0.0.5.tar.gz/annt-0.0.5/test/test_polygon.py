

from unittest import TestCase
from annt import load, hsv_to_rgb
from annt.polygon import Polygon


class TestCase(TestCase):

    def test_load(self):
        points = [[0,0],[100,20],[100,120],[0,120],[0,100]]
        tags = {1: "dog", 2: "cat"}
        obj = {"typ":2,"tagIdx":6,"pose":0,"truncated":0,"difficult":0, "position": points}
        pol = Polygon.load(obj, 200, 200, tags)

        # First point
        for i, p in enumerate(points):
            self.assertEqual(pol.points[i][0], points[i][0])
            self.assertEqual(pol.points[i][1], points[i][1])

    def test_resize(self):
        points = [[0,0],[100,20],[100,120],[0,120],[0,100]]
        tags = {1: "dog", 2: "cat"}
        obj = {"typ":2,"tagIdx":6,"pose":0,"truncated":0,"difficult":0, "position": points}
        pol = Polygon.load(obj, 200, 200, tags)
        pol_res = pol.resize(160, 140)

        answer = [[0, 0], [80, 14], [80, 84], [0, 84], [0, 70]]
        for i, p in enumerate(answer):
            self.assertEqual(pol_res.points[i][0], answer[i][0])
            self.assertEqual(pol_res.points[i][1], answer[i][1])

if __name__ == "__main__":
    unittest.main()