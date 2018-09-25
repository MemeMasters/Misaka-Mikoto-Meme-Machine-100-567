from sqlalchemy import Column, Integer, BigInteger, String, SmallInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# bigint    8 bytes     +-2^63-1    +-9,223,372,036,854,775,807
# int       4 bytes     +-2^61-1    +-2,147,483,647
# smallint  2 bytes     +-2^15-1    +-32,767

from dm_assist.sql import sql
from dm_assist.handbook import experience, races
from dm_assist import handbook

base = sql.getBase()

class Character(base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)

    strength = Column(SmallInteger, nullable=False, default=10)
    intelligence = Column(SmallInteger, nullable=False, default=10)
    wisdom = Column(SmallInteger, nullable=False, default=10)
    dexterity = Column(SmallInteger, nullable=False, default=10)
    constitution = Column(SmallInteger, nullable=False, default=10)
    charisma = Column(SmallInteger, nullable=False, default=10)
    comeliness = Column(SmallInteger, nullable=False, default=10)

    str_mod = Column(SmallInteger, nullable=False, default=0)
    int_mod = Column(SmallInteger, nullable=False, default=0)
    wis_mod = Column(SmallInteger, nullable=False, default=0)
    dex_mod = Column(SmallInteger, nullable=False, default=0)
    con_mod = Column(SmallInteger, nullable=False, default=0)
    cha_mod = Column(SmallInteger, nullable=False, default=0)
    com_mod = Column(SmallInteger, nullable=False, default=0)

    xp = Column(Integer, nullable=False, default=0)
    classname = Column(String(10))

    race = Column(String(10))
    gender = Column(Boolean, nullable=False, default=True)

    user_id = Column(BigInteger, ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_class(self):
        return experience.classes.get(self.classname)(race=self.get_race())
    
    def get_level(self):
        clss = self.get_class()
        if clss is not None:
            return clss.get_level(self.xp)

    def get_race(self):
        return races.races.get(self.race)

    @property    
    def stats(self):
        return handbook.Stats(self.strength, self.intelligence, self.wisdom, self.dexterity, self.constitution, self.charisma, self.comeliness)

    @stats.setter
    def stats(self, value: handbook.Stats):
        self.strength = value.str
        self.intelligence = value.int
        self.wisdom = value.wis
        self.dexterity = value.dex
        self.constitution = value.con
        self.charisma = value.cha
        self.comeliness = value.com

    @property
    def stats_mod(self):
        return handbook.Stats(self.str_mod, self.int_mod, self.wis_mod, self.dex_mod, self.con_mod, self.cha_mod, self.com_mod)

    @stats_mod.setter
    def stats_mod(self, value: handbook.Stats):
        self.str_mod = value.str
        self.int_mod = value.int
        self.wis_mod = value.wis
        self.dex_mod = value.dex
        self.con_mod = value.con
        self.cha_mod = value.cha
        self.com_mod = value.com

    def get_character(self):
        return handbook.Character(
            stats=self.stats,
            stats_mod=self.stats_mod,
            xp=self.xp,
            classs=self.get_class(),
            race=self.get_race(),
            gender=self.gender
        )

    def __repr__(self):
        return "<Character(name='{}', id='{}', player_id='{}', str={}, int={}, wis={}, dex={}, con={}, cha={}, com={})>".format(
            self.name, self.id, self.user_id,
            self.strength,
            self.intelligence,
            self.wisdom,
            self.dexterity,
            self.constitution,
            self.charisma,
            self.comeliness)

class TooManyCharactersError(Exception):
    pass

class User(base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True, autoincrement=False)

    characters = relationship("Character")

    def get_character(self, name=None, id=None):
        """
        Find a character that this owns.

        If no parameters are given, it will try to get only one character.
        If the user has more than one character, an exception will be thrown

        You should only give one of the optional parameters.

        :param str name: (optional) the name of the character

        :param int id: (optional) the id of the character
        """

        if name is None and id is None:
            if len(self.characters) > 1:
                raise TooManyCharactersError("There are too many characters to choose from")
            if len(self.characters) is 0:
                return None
            return self.characters[0]

        for character in self.characters:
            if name is not None and character.name == name:
                print("{} is {}".format(character.name, name))
                return character
            
            if id is not None and character.id == id:
                print("{} is {}".format(character.id, id))
                return character
        
        return None

    def __repr__(self):
        return "<User(id='{}', characters={})>".format(
            self.id,
            [char.id for char in self.characters]
        )

