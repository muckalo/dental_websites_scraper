import time
import random


def make_short_pause():
    return time.sleep(random.uniform(2.1, 5.3))


def make_medium_pause():
    return time.sleep(random.uniform(5.4, 8.7))


def make_long_pause():
    return time.sleep(random.uniform(9.1, 15.5))
