import math
from collections import Sequence

"""
The experience module contains all the XP tables for each class

Each XP table is a tuple with the required xp for each level (starting at second)

"""

def multiply(val, number, index, last_value):
    return val * number + last_value

def extendableTitle(val, number, index, last_value):
    return "{} ({}th Level)".format(val, index + 1)


class ExtendableTuple(Sequence):
    """
    The extendable tuple is an infinite tuple.  It is made of a standard tuple, then 
    is extended infinitely with an extension value, and an equation for retreiving
    the nth value

    The equation is given 3 parameters: extension, number beyond tuple's max, index number, last value

    
    ``len(tuple) is 5``
    ``index is 7``
    ``then number is 2 (7 - 5)``
    """

    def __init__(self, tup, extension, equation=multiply, maximum=-1):
        super().__init__()
        if tup is not None:
            self._data = tup
        else:
            self._data = tuple()
        self._ext = extension

        self._equation = equation
        self._max = max(maximum, -1)

    def __getitem__(self, index):
        if self._max is not -1 and index > self._max:
            return self.__getitem__(self._max)

        if abs(index) < len(self._data):
            return self._data[index]
        
        return self._equation(self._ext,
                              index - len(self._data),
                              index,
                              self._data[-1])

    def __contains__(self, value):
        return value in self._data
    
    def __iter__(self):
        if self._max is -1:
            return ExtendableIterator(self, self._max)
        return iter(self._data)
    
    def __len__(self):
        return max(len(self._data), self._max)
    
    def get_infinite_iterator(self):
        return ExtendableIterator(self, self._max)

class ExtendableIterator:
    """
    Warning this will iterate infinitely
    """
    def __init__(self, extendable: ExtendableTuple, maximum=-1):
        self._ext = extendable
        self._index = 0
        self._max = maximum
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._max > -1 and self._index > self._max:
            raise StopIteration
        else:
            self._index += 1
            return self._ext[self._index]


class XP:

    def __init__(self, xp: tuple, title: tuple, hitdice: int, num_hitdice: tuple,
                 mod_hitdice: tuple, final_xp_perlevel=-1, final_title='',
                 final_hitdice_perlevel=-1, final_mod_hitdice_perlevel=-1, max_level=-1):
        self.xp = ExtendableTuple(xp, final_xp_perlevel, maximum=max_level-2)
        self.title = ExtendableTuple(title, final_title, extendableTitle, maximum=max_level-1)
        self.hitdice = hitdice
        self.num_hitdice = ExtendableTuple(num_hitdice, final_hitdice_perlevel, maximum=max_level-1)
        self.mod_hitdice = ExtendableTuple(mod_hitdice, final_mod_hitdice_perlevel, maximum=max_level-1)
        self.max_level = max_level
        self.final_hitdice_perlevel = final_hitdice_perlevel
        self.final_mod_hitdice_perlevel = final_mod_hitdice_perlevel
        self.max_level = max_level
        self.final_xp_perlevel = final_xp_perlevel
    
    def get_level(self, xp):
        level = 1

        # This will go to the max number without infinite possibilities
        for xp_level in self.xp:
            if xp <= xp_level:
                return level
            level += 1

        # Check if the loop reached its actual limit
        if self.max_level is not -1:
            return level

        # Calculate the xp quickly
        calc_xp = xp - self.xp[level - 2]
        calc_level = math.floor(calc_xp / self.final_xp_perlevel) + level

        return calc_level
    
    def get_xp(self, level):
        """
        Get the xp required for the given level.  The level starts at 1
        """
        level = level - 2

        if level < 0:
            return 0
        
        return self.xp[level]
    
    def get_level_index(self, xp):
        return self.get_level(xp) - 1


cleric = XP(
    xp=(1500, 3000, 6000, 13000, 27500, 55000, 110000, 225000, 450000, 675000, 900000),
    title=('Acolyte', 'Adept', 'Priest', 'Curate', 'Curate', "Canon", 'Lama', 'Patriarch', 'High Priest'),
    hitdice=8,
    num_hitdice=tuple(x for x in range(1, 10)),
    mod_hitdice=(0,) * 9,
    final_xp_perlevel=225000,
    final_title='High Priest',
    final_hitdice_perlevel=0,
    final_mod_hitdice_perlevel=2
)


def __get_initiate(number):
    initiate = "initiate of the {} circle"

    init = str(number)
    if number is 1:
        init += "st"
    elif number is 2:
        init += 'nd'
    elif number is 3:
        init += 'rd'
    else:
        init += 'th'

    return initiate.format(init)


druid = XP(
    xp=(2000, 4000, 7500, 12500, 20000, 35000, 60000, 90000, 125000, 200000, 300000, 750000, 1500000),
    title=("Aspirant", 'Ovate') + tuple(__get_initiate(x) for x in range(1, 10)) + ("Druid", "ArchDruid", "The Great Druid"),
    hitdice=8,
    num_hitdice=tuple(x for x in range(1, 15)),
    mod_hitdice=(0,) * 14,
    max_level=14
)

fighter = XP(
    xp=(2000, 4000, 8000, 18000, 35000, 70000, 125000, 250000, 500000, 750000),
    title=("Veteran", "Warrior", 'Swordsman', 'Hero', 'Swashbuckler', 'Myrmidon', 'Champion', 'Superhero', 'Lord'),
    hitdice=10,
    num_hitdice=tuple(x for x in range(1, 10)),
    mod_hitdice=(0,) * 10,
    final_title='Lord',
    final_xp_perlevel=250000,
    final_hitdice_perlevel=0,
    final_mod_hitdice_perlevel=3
)


paladin = XP(
    xp=(2750, 5500, 12000, 24000, 45000, 95000, 175000, 350000, 700000, 1050000, 1400000),
    title=('Gallant', 'Keeper', 'Protector', 'Defender', 'Warder', 'Guardian', 'Chevalier', 'Justiciar', 'Paladin'),
    hitdice=10,
    num_hitdice=tuple(x for x in range(1, 10)),
    mod_hitdice=(0,) * 9,
    final_xp_perlevel=350000,
    final_hitdice_perlevel=0,
    final_title='Paladin',
    final_mod_hitdice_perlevel=3
)


ranger = XP(
    xp=(2250, 4500, 10000, 20000, 40000, 90000, 150000, 225000, 325000, 650000, 975000, 1300000),
    title=('Runner', 'Strider', 'Scout', 'Courser', 'Tracker', 'Guide', 'Pathfinder', 'Ranger', 'Ranger Knight', 'Ranger Lord'),
    hitdice=8,
    num_hitdice=tuple(x for x in range(2, 12)),
    mod_hitdice=(0,) * 10,
    final_title='Ranger Lord',
    final_hitdice_perlevel=0,
    final_mod_hitdice_perlevel=2,
    final_xp_perlevel=325000
)


magic_user = XP(
    xp=(2500, 5000, 10000, 22500, 40000, 60000, 90000, 135000, 250000, 375000, 750000, 1125000, 1500000, 1875000, 2250000, 2625000, 3000000, 3375000),
    title=('Prestidigitator', 'Evoker', 'Conjurer', 'Theurgist', 'Thaumaturgist', 'Magicician', 'Enchanter', 'Warlock', 'Sorcerer', 'Necromancer', 'Wizard'),
    hitdice=4,
    num_hitdice=tuple(x for x in range(1, 12)),
    mod_hitdice=(0,) * 11,
    final_title='Wizard',
    final_xp_perlevel=375000,
    final_hitdice_perlevel=0,
    final_mod_hitdice_perlevel=1
)


illusionist = XP(
    xp=(2250, 4500, 9000, 18000, 35000, 60000, 95000, 145000, 220000, 440000, 660000, 880000),
    title=('Prestidigitator', 'Minor Trickster', 'Trickster', 'Master Trickster', 'Cabalist', 'Visionist', 'Phantasmist', 'Spellbinder', 'Illusionist'),
    hitdice=4,
    num_hitdice=tuple(x for x in range(1, 11)),
    mod_hitdice=(0,) * 10,
    final_title='Illusionist',
    final_xp_perlevel=220000,
    final_hitdice_perlevel=0,
    final_mod_hitdice_perlevel=1
)


thief = XP(
    xp=(1250, 2500, 5000, 10000, 20000, 42500, 70000, 110000, 160000, 220000, 440000, 660000),
    title=('Rogue (Apprentice)', 'Footpad', 'Cutpurse', 'Robber', 'Burglar', 'Filcher', 'Sharper', 'Magsman', 'Thief', 'Master Thief'),
    hitdice=6,
    num_hitdice=tuple(x for x in range(1, 11)),
    mod_hitdice=(0,) * 10,
    final_title='Master Thief',
    final_hitdice_perlevel=0,
    final_mod_hitdice_perlevel=2
)


assassin = XP(
    xp=(1500, 3000, 6000, 12000, 25000, 50000, 100000, 200000, 300000, 425000, 575000, 75000, 1000000, 1500000),
    title=('Bravo (Apprentice)', 'Rutterkin', 'Waghalter', 'Murderer', 'Thug', 'Killer', 'Cutthroat', 'Executioner', 'Assassin', 'Expert Assassin', 'Senior Assassin', 'Chief Assassin', 'Prime Assassin', 'Guildmaster Assassin', 'Grandfather of Assassins'),
    hitdice=6,
    num_hitdice=tuple(x for x in range(1, 16)),
    mod_hitdice=(0,) * 15,
    max_level=15
)


monk = XP(
    xp=(2250, 4750, 10000, 22500, 47500, 98000, 200000, 350000, 500000, 700000, 950000, 1250000, 1750000, 2250000, 2750000, 3250000),
    title=('Novice', 'Initiate', 'Brother', 'Disciple', 'Immaculate', 'Master', 'Superior Master', 'Master of Dragons', 'Master of the North Wind', 'Master of the West Wind', 'Master of the South Wind', 'Master of the East Wind', 'Master of Winter', 'Master of Autumn', 'Master of Summer', 'Master of Spring', 'Grand Master of Flowers'),
    hitdice=4,
    num_hitdice=tuple(x for x in range(2, 19)),
    mod_hitdice=(0,) * 17,
    max_level=17
)


classes = dict(cleric=cleric, druid=druid, fighter=fighter, paladin=paladin, ranger=ranger, magic_user=magic_user, illusionist=illusionist, thief=thief, assassin=assassin, monk=monk)
