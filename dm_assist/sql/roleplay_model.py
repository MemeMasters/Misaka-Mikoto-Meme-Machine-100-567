from sqlalchemy import Column, Integer, BigInteger, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

# bigint    8 bytes     +-2^63-1    +-9,223,372,036,854,775,807
# int       4 bytes     +-2^61-1    +-2,147,483,647
# smallint  2 bytes     +-2^15-1    +-32,767

from dm_assist.sql import sql
from dm_assist.handbook import experience

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

    xp = Column(Integer, nullable=False, default=0)
    classname = Column(String(10))

    user_id = Column(BigInteger, ForeignKey('user.id'))

    def get_class(self):
        return experience.classes.get(self.classname)

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

