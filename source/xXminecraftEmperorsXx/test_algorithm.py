from unittest import TestCase
from xXminecraftEmperorsXx.algorithm import Algorithm


class TestAlgorithm(TestCase):
    def test_init(self):
        self.algorithm = Algorithm()
        self.algorithm.__init__()
        self.assertEqual(self.algorithm.weights, (1,2,3,4,5), "not equal" )
        pass

if __name__ == "__main__":
    test = TestAlgorithm()
    test.test_init()
