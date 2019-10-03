import random


def roll_random(percentage):

    p = percentage * 10000

    roll = random.randint(0, 10000)

    if roll < p:
        return True
    else:
        return False
