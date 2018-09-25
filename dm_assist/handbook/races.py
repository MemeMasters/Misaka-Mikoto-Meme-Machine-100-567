from . import Stats, ValidationError


class StatIssue:

    def __init__(self, message, max=None, min=None):
        self.message = message
        self._max = max
        self._min = min
    
    def is_min(self):
        return self._min is not None
    
    def is_max(self):
        return self._max is not None
    
    @property
    def limit(self):
        if self.is_min():
            return self._min
        if self.is_max():
            return self._max


class MinMax:

    def __init__(self,
                 minstr, maxstr,
                 minint, maxint,
                 minwis, maxwis,
                 mindex, maxdex,
                 mincon, maxcon,
                 mincha, maxcha):
        self.minstr = minstr
        self.maxstr = maxstr
        self.minint = minint
        self.maxint = maxint
        self.minwis = minwis
        self.maxwis = maxwis
        self.mindex = mindex
        self.maxdex = maxdex
        self.mincon = mincon
        self.maxcon = maxcon
        self.mincha = mincha
        self.maxcha = maxcha


class ClassLimits:

    def __init__(self,
                 cleric,
                 druid,
                 fighter,
                 paladin,
                 ranger,
                 magic_user,
                 illusionist,
                 thief,
                 assassin,
                 monk):
        self.cleric = cleric
        self.druid = druid
        self.fighter = fighter
        self.paladin = paladin
        self.ranger = ranger
        self.magic_user = magic_user
        self.illusionist = illusionist
        self.thief = thief
        self.assassin = assassin
        self.monk = monk


class Race:

    @staticmethod
    def _validate_stat(minim, maxim, stat, name):
        """
        Validates a stat.  Nothing is returned if successful

        Validation error with a propper
        """
        if stat > maxim:
            return StatIssue('{} cannot be higher than {}'.format(
                name, maxim
            ), max=maxim)
        if stat < minim:
            return StatIssue('{} cannot be lower than {}'.format(
                name, minim
            ), min=minim)
        return None
    @staticmethod
    def _validate_stats(minmax: MinMax, stats: Stats):
        ret = dict()
        ret['str'] = Race._validate_stat(minmax.minstr, minmax.maxstr, stats.str, 'Strength')
        ret['int'] = Race._validate_stat(minmax.minint, minmax.maxint, stats.int, 'Intelligence')
        ret['wis'] = Race._validate_stat(minmax.minwis, minmax.maxwis, stats.wis, 'Wisdom')
        ret['dex'] = Race._validate_stat(minmax.mindex, minmax.maxdex, stats.dex, 'Dexterity')
        ret['con'] = Race._validate_stat(minmax.mincon, minmax.maxcon, stats.con, 'Constitution')
        ret['cha'] = Race._validate_stat(minmax.mincha, minmax.maxcha, stats.cha, 'Charisma')
        ret['com'] = None
        return ret
    
    @staticmethod
    def _validate_class(class_limit, classs, race):
        if class_limit is None:
            raise ValidationError('{} cannot be a {}'.format(race, classs))
        if class_limit is -1:
            return None
        return class_limit
        
    @staticmethod
    def _validate_classes(class_limit:ClassLimits, classs, race):
        clss = classs.lower()[:3]
        if clss == 'cle':
            return Race._validate_class(class_limit.cleric, classs, race)
        if clss == 'dru':
            return Race._validate_class(class_limit.druid, classs, race)
        if clss == 'fig':
            return Race._validate_class(class_limit.fighter, classs, race)
        if clss == 'pal':
            return Race._validate_class(class_limit.paladin, classs, race)
        if clss == 'ran':
            return Race._validate_class(class_limit.ranger, classs, race)
        if clss == 'mag':
            return Race._validate_class(class_limit.magic_user, classs, race)
        if clss == 'ill':
            return Race._validate_class(class_limit.illusionist, classs, race)
        if clss == 'thi':
            return Race._validate_class(class_limit.thief, classs, race)
        if clss == 'ass':
            return Race._validate_class(class_limit.assassin, classs, race)
        if clss == 'mon':
            return Race._validate_class(class_limit.monk, classs, race)
        

    def validate_stats(self, stats: Stats):
        """
        Validate the stats for the given race

        Returns a dictionary of StatIssue for each stat if there is anissue with that stat.
        If there is no issue, then the value for the stat will be None
        """
        pass
    
    def validate_class(self, classs: str):
        """
        Validate the class for the given race

        Nothing is returned if successful, and there is no level limitation

        If there is a level limitation, then the max level is returned
        """
        pass
    
    def get_Stat_modifiers(self):
        """
        Get the modifiers for the race
        """
        pass


class Dwarf(Race):

    _Male_minmax = (
        8, 18,
        3, 18,
        3, 18,
        3, 17,
        12, 19,
        3, 16
    )

    _Female_minmax = (
        8, 17,
        3, 18,
        3, 18,
        3, 17,
        12, 19,
        3, 16
    )

    _Class_limits = (
        None,
        -1,
        9,
        -1,
        -1,
        -1,
        -1,
        -1,
        9,
        -1
    )

    def validate_stats(self, stats: Stats, gender):
        minmax = MinMax(*(self.__class__._Male_minmax if gender else self.__class__._Female_minmax))
        
        return Race._validate_stats(minmax, stats)
    
    def validate_class(self, classs):
        return Race._validate_classes(ClassLimits(*self.__class__._Class_limits), classs, 'Dwarf')
    
    def get_Stat_modifiers(self):
        return Stats(stren=0, intel=0, wis=0, dex=0, con=1, cha=-1, com=0)


class Elf(Race):

    _Male_minmax = (
        3, 18,
        8, 18,
        3, 18,
        7, 19,
        6, 18,
        8, 18
    )

    _Female_minmax = (
        3, 16,
        8, 18,
        3, 18,
        7, 19,
        6, 18,
        8, 18
    )

    _Class_limits = (
        None,
        -1,
        7,
        -1,
        -1,
        11,
        -1,
        -1,
        10,
        -1
    )

    def validate_stats(self, stats: Stats, gender):
        minmax = MinMax(*(self.__class__._Male_minmax if gender else self.__class__._Female_minmax))
        
        return Race._validate_stats(minmax, stats)
    
    def validate_class(self, classs):
        return Race._validate_classes(ClassLimits(*self.__class__._Class_limits), classs, 'Elf')
    
    def get_Stat_modifiers(self):
        return Stats(stren=0, intel=0, wis=0, dex=1, con=-1, cha=0, com=0)


class Gnome(Race):

    _Male_minmax = (
        6, 18,
        7, 18,
        3, 18,
        3, 18,
        8, 18,
        3, 18
    )

    _Female_minmax = (
        6, 15,
        7, 18,
        3, 18,
        3, 18,
        8, 18,
        3, 18
    )

    _Class_limits = (
        None,
        -1,
        6,
        -1,
        -1,
        -1,
        7,
        -1,
        8,
        -1
    )

    def validate_stats(self, stats: Stats, gender):
        minmax = MinMax(*(self.__class__._Male_minmax if gender else self.__class__._Female_minmax))
        
        return Race._validate_stats(minmax, stats)
    
    def validate_class(self, classs):
        return Race._validate_classes(ClassLimits(*self.__class__._Class_limits), classs, 'Elf')
    
    def get_Stat_modifiers(self):
        return Stats(stren=0, intel=0, wis=0, dex=0, con=0, cha=0, com=0)


class HalfElf(Race):

    _Male_minmax = (
        3, 18,
        4, 18,
        3, 18,
        6, 18,
        6, 18,
        3, 18
    )

    _Female_minmax = (
        3, 17,
        4, 18,
        3, 18,
        6, 18,
        6, 18,
        3, 18,
    )

    _Class_limits = (
        5,
        -1,
        8,
        -1,
        8,
        8,
        -1,
        -1,
        11,
        -1,
    )

    def validate_stats(self, stats: Stats, gender):
        minmax = MinMax(*(self.__class__._Male_minmax if gender else self.__class__._Female_minmax))
        
        return Race._validate_stats(minmax, stats)
    
    def validate_class(self, classs):
        return Race._validate_classes(ClassLimits(*self.__class__._Class_limits), classs, 'Elf')
    
    def get_Stat_modifiers(self):
        return Stats(stren=0, intel=0, wis=0, dex=0, con=0, cha=0, com=0)
        

class Halfling(Race):

    _Male_minmax = (
        6, 17,
        6, 18,
        3, 17, 
        8, 18,
        10, 19,
        3, 18
    )

    _Female_minmax = (
        6, 14,
        6, 18,
        3, 17, 
        8, 18,
        10, 19,
        3, 18
    )

    _Class_limits = (
        -1,
        None,
        6,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
    )

    def validate_stats(self, stats: Stats, gender):
        minmax = MinMax(*(self.__class__._Male_minmax if gender else self.__class__._Female_minmax))
        
        return Race._validate_stats(minmax, stats)
    
    def validate_class(self, classs):
        return Race._validate_classes(ClassLimits(*self.__class__._Class_limits), classs, 'Elf')
    
    def get_Stat_modifiers(self):
        return Stats(stren=-1, intel=0, wis=0, dex=1, con=0, cha=0, com=0)
        

class HalfOrc(Race):

    _Male_minmax = (
        6, 18,
        3, 17, 
        3, 14,
        3, 17,
        13, 19,
        3, 12
    )

    _Female_minmax = (
        6, 18,
        3, 17,
        3, 14,
        3, 17,
        13, 19,
        3, 12
    )

    _Class_limits = (
        4,
        -1,
        10,
        -1,
        -1,
        -1,
        -1,
        8,
        -1,
        -1,
    )

    def validate_stats(self, stats: Stats, gender):
        minmax = MinMax(*(self.__class__._Male_minmax if gender else self.__class__._Female_minmax))
        
        return Race._validate_stats(minmax, stats)
    
    def validate_class(self, classs):
        return Race._validate_classes(ClassLimits(*self.__class__._Class_limits), classs, 'Elf')
    
    def get_Stat_modifiers(self):
        return Stats(stren=1, intel=0, wis=0, dex=0, con=1, cha=-2, com=0)


class Human(Race):

    def validate_stats(self, stats: Stats, gender):
        return dict(str=None, int=None, wis=None, dex=None, con=None, cha=None, com=None)
    
    def validate_class(self, classs):
        return None
    
    def get_Stat_modifiers(self):
        return Stats(stren=0, intel=0, wis=0, dex=0, con=0, cha=0, com=0)


races = dict(dwarf=Dwarf(), elf=Elf(), gnome=Gnome(), halfelf=HalfElf(), halfling=Halfling(), halforc=HalfOrc(), human=Human())