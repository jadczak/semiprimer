import unittest

try:
    from semiprimer.semiprimer import SemiPrime
except ModuleNotFoundError:
    import os
    import sys

    here = os.path.realpath(__file__)
    root = os.path.split(os.path.split(here)[0])[0]
    sys.path.append(root)
    from semiprimer.semiprimer import SemiPrime


class MyTestCase(unittest.TestCase):
    def test_carol(self):
        carol_1 = 1046527
        carol_2 = 16769023
        carol_semi = carol_1 * carol_2
        semiprime = SemiPrime(carol_semi)
        semiprime.factor()
        self.assertIn(carol_1, semiprime.factors)
        self.assertIn(carol_2, semiprime.factors)


if __name__ == "__main__":
    unittest.main()
