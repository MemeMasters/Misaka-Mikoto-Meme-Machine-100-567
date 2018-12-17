from . import random, _calculator

calculator = _calculator.Calculator()

def get_random_line(messages: list):
    return (messages[random.roll_die(len(messages), False) - 1])


def format_name(name: str) -> str:
    """
    Capitalize every word in the given string.
    For some reason capitalize only capitalizes the first letter.

    This capitallizes every word.
    """
    return ' '.join([w.capitalize() for w in name.split(' ')])
