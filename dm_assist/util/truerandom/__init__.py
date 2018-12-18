import random
import asyncio
from asyncio import Queue

# Urandom is used as a backup if your quota is used up.
# You however have a quota of 200K bits per day with a
# max(start) of 1M bits.
# So you probably wont run out

urandom = random.SystemRandom()

from .randomwrapy import *

random_buffer = dict()


def urandom_list(count, max):
    return [urandom.randint(1, max) for _ in range(count)]

async def populate_random_buffer(max, prefetch=None, use_true_random=True):
    """
    Populate the random_buffer with random numbers.

    If the number is larger than 100, then urandom will be used.
    """

    num = prefetch if prefetch is not None else 30

    if use_true_random:
        try:
            print('TrueRandom: Fetching {} true Random numbers from 1 to {}'.format(num, max))
            numbers = rnumlistwithreplacement(num, max, 1)
        except NoQuotaError:
            print('TrueRandom: Daily quota has run out, using urandom instead')
        else:
            numbers = urandom_list(num, max)
    else:
        numbers = urandom_list(num, max)

    if str(max) not in random_buffer:
        random_buffer[str(max)] = Queue()
    
    queue = random_buffer[str(max)]
    for value in numbers:
        await queue.put(value)


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

    buf = random_buffer.get(index)

    if buf is not None:
        try:
            ret = buf.get_nowait()
        except asyncio.QueueEmpty:
            ret = urandom_list(1, max)[0]
    else:
        ret = urandom_list(1, max)[0]

    return ret, buf is None or buf.qsize() < 10
