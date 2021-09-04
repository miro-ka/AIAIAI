import unittest
from exchange.poloniex.poloniex import Poloniex


class TestPoloniex(unittest.TestCase):

    def test_get_ticker(self):
        res = Poloniex().get_ticker()
        self.assertEqual(res, 2)


if __name__ == '__main__':
    unittest.main()
