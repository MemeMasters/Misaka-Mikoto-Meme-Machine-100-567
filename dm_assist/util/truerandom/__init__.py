import random
from asyncio import Queue

# Urandom is used as a backup if your quota is used up.
# You however have a quota of 200K bits per day with a
# max(start) of 1M bits.
# So you probably wont run out

urandom = random.SystemRandom()

from dm_assist.config import config

from .randomwrapy import *

random_buffer = dict()

common_randoms = [2, 4, 6, 8, 10, 12, 20, 100]

def populate_random_buffer(max, prefetch=None, use_true_random=True):
    """
    Populate the random_buffer with random numbers.

    If the number is larger than 100, then urandom will be used.
    """

    num = prefetch if prefetch is not None else config.config.random.preFetchCount

    def urandom_list(count):
        return [urandom.randint(1, max) for _ in range(count)]

    if use_true_random and config.config.random.useRandomDotOrg:
        if max <= 100:

            if prefetch is None:
                num = config.config.random.preFetchCommonCount if max in common_randoms else config.config.random.preFetchCount

            try:
                print('TrueRandom: Fetching {} true Random numbers from 1 to {}'.format(num, max))
                numbers = rnumlistwithreplacement(10, max, 1)
            except NoQuotaError:
                print('TrueRandom: Daily quota has run out, using urandom instead')
            else:
                numbers = urandom_list(num)
        else:
            numbers = urandom_list(config.config.random.preFetchCount)
    else:
        numbers = urandom_list(config.config.random.preFetchCount)

    if str(max) in random_buffer:
        random_buffer[str(max)].extend(numbers)
    else:
        random_buffer[str(max)] = numbers

def randint(max, use_true_random=True):
    """
    Get a true random number.
    
    If you will be getting a large sum of random numbers, I
    suggest calling prefetch with the amount of numbers
    before collecting them.

    the range is [1-max] all inclusive

    :param max: the (inclusive) max number to get
    """
    index = str(max)

    ret = random_buffer.get(index)

    if ret is not None:
        try:
            ret = ret.pop(0)
        except IndexError:
            populate_random_buffer(max, use_true_random=use_true_random)
            ret = random_buffer[index].pop(0)

        return ret
    
    populate_random_buffer(max, use_true_random=use_true_random)
    
    return random_buffer[index].pop(0)


