# Handbook __init__

class ValidationError(Exception):
    pass

class Stats:

    def __init__(self, stren=10, intel=10, wis=10, dex=10, con=10, cha=10, com=10):
        self.str = stren
        self.int = intel
        self.wis = wis
        self.dex = dex
        self.con = con
        self.cha = cha
        self.com = com


class Character:

    def __init__(self, stats=None, stats_mod=None, xp=None, classs=None, race=None, gender=False):
        if stats is None:
            stats = Stats()
        
        if stats_mod is None:
            if race is not None:
                stats_mod = race.get_Stat_modifiers()
            else:
                stats_mod = Stats(0, 0, 0, 0, 0, 0, 0)
        
        self.stats = stats
        self.stats_mod = stats_mod
        self.xp = xp
        self.race = race
        self.classs = classs
        self.gender = gender
    
    @property
    def level(self):
        if self.classs is not None:
            return self.classs.get_level(self.xp)
        return None
    
