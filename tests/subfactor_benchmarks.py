import timeit
import os
import sys

here = os.path.realpath(__file__)
root = os.path.split(os.path.split(here)[0])[0]
sys.path.append(root)

setup = """
from semiprimer.semiprimer import SemiPrime
semiprime = SemiPrime("527")  # 17*31
"""


def main():
    print(timeit.timeit('semiprime.sub_factor("7")', setup=setup, number=100000))


if __name__ == "__main__":
    main()
