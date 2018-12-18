import random
import asyncio

from . import truerandom


class Dice:

    def __init__(self):
        self._low = False
        self._rolled_dice = list()
        self._enable_logging = False

    @property
    def logging_enabled(self):
        return self._enable_logging

    @logging_enabled.setter
    def logging_enabled(self, value):
        """
        Setting this to True will clear the current log.
        """
        if value is True:
            self._rolled_dice = list()
        self._enable_logging = bool(value)

    @property
    def low(self):
        return self._low
    
    @property
    def rolled_dice(self):
        """
        This is a log of all the dice rolled.

        To enable the logging of dice, the variable logging_enabled 
        should be set to True. That way, any unintentional dice rolls 
        will not be logged.

        Reading from rolled_dice will clear the list.
        """
        dice = self._rolled_dice
        self._rolled_dice = list()
        return dice

    async def load_random_buffer(self):
        asyncio.ensure_future(truerandom.populate_random_buffer(120, 30, True))
        self._low = False

    def __log_roll(self, value):
        if self._enable_logging:
            self._rolled_dice.append(value)

    def _roll(self, sides: int) -> int:
        if sides is 1:
            self.__log_roll((1, 1))
            return 1

        if 120 % sides is 0:
            rand, self._low = truerandom.randint(120, use_true_random=True)
            die = rand % sides + 1
            self.__log_roll((die, sides))
            return die
        die = truerandom.randint(sides, use_true_random=False)[0]
        self.__log_roll((die, sides))
        return die
    
    def roll(self, sides: int) -> int:
        # "Authentically" roll percentile dice
        if sides % 100 is 0:
            dice = len(str(sides)) - 1
            result = 0
            for i in reversed(range(dice)):
                roll = self._roll(10)
                roll = 0 if roll is 10 else roll
                result += 10 ** i * roll
            if result is 0:
                result = sides
            return result

        return self._roll(sides)


    def roll_sum(self, sides: int, times=1) -> (int, int, int):
        """
        Roll a number of dice, and return the sum.

        The number of crits, and fails, are also returned

        :param int sides: number of sides on the dice

        :param int times: number of times to roll the dice

        :returns (int, int, int): (sum, num_crits, num_fails)
        """

        rolls = self.roll_dice(sides, times)

        crits = len([r for r in rolls if r is sides])
        fails = len([r for r in rolls if r is 1])

        return sum(rolls), crits, fails

    def roll_dice(self, sides: int, times=1) -> list:
        """
        Roll a number of dice.

        The returned value is a list of all the values of the dice.

        :param int sides: the number of sides on the dice
        :param int times: the number of times to roll the dice

        :returns list: a list of all the rolled dice
        """
        return [self.roll(sides) for _ in range(times)]
    
    def roll_top(self, sides: int, top_rolls=3, times=4, best=True) -> int:
        """
        Roll a number of dice, only counting the highest values.

        Example:
        ```
        roll_top(6, 3, 4)
        # Rolled dice:
        [3, 6, 4, 2]
        # Returned value:
        12
        ```

        This is usefull for improving the odds of dice, orrolling advantage/
        disadvantage dice

        :param int sides: number of sides of the dice

        :param int top_rolls: the number of dice to take

        :param int times: the number of times to roll the dice

        :param bool best: Whether to take the highest, or lowest rolls.

        """

        top_rolls = min(top_rolls, times)

        if top_rolls is times:
            return self.roll_sum(sides, times)[0]
        
        top_rolls = [0 if best else sides + 1] * top_rolls

        rolls = self.roll_dice(sides, times)

        for roll in rolls:
            for i, top in enumerate(top_rolls):
                if (roll > top and best) or (roll < top and not best):
                    # Insert the new top roll, and pop the lowest current high roll
                    top_rolls.pop()
                    top_rolls.insert(i, roll)

                    # The roll has been inserted, we don't need look for any other insertion points
                    break
        
        return sum(top_rolls)
