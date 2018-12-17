import random

from . import truerandom


def pre_fetch_rolls(times, sides):
    from dm_assist.config import config
    
    base_times = config.config.random.preFetchCommonCount \
        if sides in truerandom.common_randoms \
        else config.config.random.preFetchCount

    if times > base_times:
        truerandom.populate_random_buffer(sides, times)


def roll_die(sides: int, use_true_random=True) -> int:
    if sides is 1:
        return 1
    return truerandom.randint(sides, use_true_random=use_true_random)


def roll(times: int, sides: int) -> (int, int, int):
    """
    Roll a n-sided die x number of times

    :returns tuple: (total, critical successes, critical fails)
    """

    print("Rolling {count} {sides} sided dice.".format(
        count=times, sides=sides))

    pre_fetch_rolls(times, sides)

    total = 0
    crit_fail = 0
    crit_succ = 0

    for _ in range(times):
        roll = roll_die(sides)
        total += roll
        if roll is sides:
            crit_succ += 1
        elif roll is 1:
            crit_fail += 1
    
    print("total {} with {} crits and {} fails".format(
        total, crit_succ, crit_fail))

    return total, crit_succ, crit_fail


def roll_top(times: int, top_rolls: int, sides: int) -> int:
    pre_fetch_rolls(times, sides)

    rolls = list()

    for _ in range(times):
        roll = roll_die(sides)
        rolls.append(roll)

    top_x = [-1] * top_rolls

    for roll in rolls:
        # Check if the roll is greater than any of the current top rolls
        for i, top in enumerate(top_x):
            if roll > top:
                # shift each top roll down
                for ii in reversed(range(i, len(top_x) - 1)):
                    top_x[ii + 1] = top_x[ii]
                top_x[i] = roll
                break
    
    return sum(top_x)


class BadFormat(Exception):

    def __init__(self, message):
        super().__init__(message)


def parse_die_roll(text: str) -> dict:
    """
    Parse a die roll string, then roll the dice.

    The format of the text is: xdy xdy xdy

    In the future the format might support addition and subraction

    :returns dict: {
        total int,
        crits int,
        fails int,
        rolls int,
        sides list
    }
    """

    dice = text.split(' ')

    total = 0
    crit_fail = 0
    crit_succ = 0

    num_rolls = 0
    num_sides = list()

    for die in dice:
        die = die.lower()
        if 'd' in die:
            die_roll = die.split('d')

            try:
                count = int(die_roll[0])
                sides = int(die_roll[1])


                if sides is 0:
                    raise BadFormat("Can't roll a 0 sided die")

                num_rolls += count
                num_sides.append(sides)

                value, succ, fail = roll(count, sides)
                total += value
                crit_succ += succ
                crit_fail += fail
            except ValueError:
                raise BadFormat("I don't understand how to read that")
        else:
            raise BadFormat("The format is <rolls>d<sides>")

    print("rolled {} rolls.  Got {} with {} crits and {} fails".format(
        len(dice), total, crit_succ, crit_fail))

    data = dict(
        total=total,
        crits=crit_succ,
        fails=crit_fail,
        rolls=num_rolls,
        sides=num_sides
    )

    return data
