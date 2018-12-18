

class BadEquation(Exception):
    pass


# dice needs to be setup first, as calculator depends on dice
from . import _dice
dice = _dice.Dice()


from . import _calculator
calculator = _calculator.Calculator()


def get_random_line(messages: list):
    return (messages[dice.roll(len(messages)) - 1])


def format_name(name: str) -> str:
    """
    Capitalize every word in the given string.
    For some reason capitalize only capitalizes the first letter.

    This capitallizes every word.
    """
    return ' '.join([w.capitalize() for w in name.split(' ')])
