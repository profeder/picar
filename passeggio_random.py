import logging
import random
import time

import picar_4wd as fc

SCAN_SLEEP = 0.1
MIN_DIST_FOLLOW = 30


def lettura_media(angolo):
    res = 0
    for i in range(1, 3):
        res = res + fc.get_distance_at(angolo)
        time.sleep(0.1)
    logging.warning('score media: ' + str(res/3))
    return res / 3


def scan_dx():
    score = 0
    for i in range(30, 91, 10):
        score = lettura_media(i)
        time.sleep(SCAN_SLEEP)
    return score


def scan_sx():
    score = 0
    for i in range(-30, -91, -10):
        score = lettura_media(i)
        time.sleep(SCAN_SLEEP)
    return score


def main_loop():
    if lettura_media(0) > MIN_DIST_FOLLOW:
        fc.forward(20)
        while lettura_media(0) > MIN_DIST_FOLLOW:
            pass
    fc.stop()
    lval = scan_sx()
    rval = scan_dx()
    turn_time = 0.5 + random.random()*1
    if rval < lval:
        fc.turn_right(20)
    else:
        fc.turn_left(20)
    time.sleep(turn_time)


if __name__ == '__main__':
    while True:
        main_loop()
