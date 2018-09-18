import random


def roll(times: int, sides: int) -> (int, int, int):
    """
    Roll a n-sided die x number of times

    :returns tuple: (total, critical successes, critical fails)
    """

    print("Rolling {count} {sides} sided dice.".format(
        count=times, sides=sides))

    total = 0
    crit_fail = 0
    crit_succ = 0

    for _ in range(times):
        roll = random.randint(1, sides)
        total += roll
        if roll is sides:
            crit_succ += 1
        elif roll is 1:
            crit_fail += 1
    
    print("total {} with {} crits and {} fails".format(
        total, crit_succ, crit_fail))

    return total, crit_succ, crit_fail


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


def get_random_line(messages: list):
    return (messages[random.randint(0, len(messages)-1)])


def format_name(name: str) -> str:
    """
    Capitalize every word in the given string.
    For some reason capitalize only capitalizes the first letter.

    This capitallizes every word.
    """
    return ' '.join([w.capitalize() for w in name.split(' ')])
