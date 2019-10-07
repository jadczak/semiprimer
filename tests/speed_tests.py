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


class TestSmallPrimes(unittest.TestCase):
    @unittest.skip("skipping carol.  Runs too fast for speed testing.")
    def test_carol(self):
        # pypy3
        # i5 2500k
        #        10.7 seconds
        #   962,434   nodes processed
        # 8,661,798   nodes rejected
        # 17,549,235,333,121 <- semi-prime.  14 digits.
        carol_1 = 1046527
        carol_2 = 16769023
        carol_semi = carol_1 * carol_2
        semiprime = SemiPrime(carol_semi)
        semiprime.factor()
        self.assertIn(carol_1, semiprime.factors)
        self.assertIn(carol_2, semiprime.factors)
        del semiprime

    @unittest.skip("Skipping baby test.  Runs too fast for speed testing")
    def test_baby(self):
        baby_1 = 101
        baby_2 = 191
        baby_semi = baby_1 * baby_2
        semiprime = SemiPrime(baby_semi)
        semiprime.factor()
        self.assertIn(baby_1, semiprime.factors)
        self.assertIn(baby_2, semiprime.factors)
        del semiprime

    # TODO: find a new ~100 second test.

    @unittest.skip("Skipping factorial test.  Takes too long currently.")
    def test_factorial(self):
        # pypy3
        # i5 2500k
        #       1,898.9 seconds
        #  46,380,744   nodes processed
        # 417,426,580   nodes rejected
        # 41,758,540,882,408,627,201 <- semi-prime.  20 digits.
        factorial_1 = 479001599
        factorial_2 = 87178291199
        factorial_semi = factorial_1 * factorial_2
        semiprime = SemiPrime(factorial_semi)
        semiprime.factor()
        self.assertIn(factorial_1, semiprime.factors)
        self.assertIn(factorial_2, semiprime.factors)
        del semiprime


if __name__ == "__main__":
    unittest.main()
