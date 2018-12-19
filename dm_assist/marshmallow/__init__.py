import os
import json
from marshmallow import Schema, fields, post_load

from . import characters, music
from .. import util


class User:

    def __init__(self):
        self.db = None

        self.id = 0
        self.chars = list()
        self.playlist = None

        self.active_char = None
    
    def _on_load(self, db):
        self.db = db
        chars = db.characters

        ids = [x.id for x in self.chars]
        self.chars = [char for char in chars if char.id in ids]

        # Load the user's playlist
        for pl in db.playlists:
            if pl.user is self.id:
                self.playlist = pl
                break

        # Load the active character
        for char in self.chars:
            if char.id is self.active_char.id:
                self.active_char = char
    
    def create_character(self, name):
        # Check for duplicates
        for char in self.chars:
            if char.name == name:
                return False

        char = characters.Character()
        char.name = name
        char.id = self.db.uid
        char._on_load(self.db)

        self.db.characters.append(char)
        self.chars.append(char)
        return True

    def __repr__(self):
        ids = [x.id for x in self.chars]
        return '<User(id={self.id}, characters={chars})>'.format(self=self, chars=ids)


class UserSchema(Schema):
    id = fields.Integer()
    chars = fields.Nested(characters.CharacterSchema, only=['id'], many=True)
    active_char = fields.Nested(characters.CharacterSchema, only=['id'])

    @post_load
    def create_User(self, data):
        user = User()

        for key, val in data.items():
            setattr(user, key, val)
        
        return user


class Database:

    base_dir = "db.dat/"

    user_file = base_dir + "users.json"
    item_file = base_dir + "items.json"
    music_file = base_dir + "playlists.json"

    def __init__(self):
        self.users = list()
        self.items = list()
        self.characters = list()
        self.playlists = list()
        self.current_dm = None
        self.mods = list()
    
    @property
    def uid(self):
        # Create a random 10 digit number
        id = util.dice.roll(1000000000)
        
        ids = list()
        ids.extend([i.id for i in self.items])
        ids.extend([i.id for i in self.characters])

        if id in ids:
            # This probably won't happen, but just in case 
            # there is a duplicate, generate a new id
            return self.uid
        return id
    
    def item(self, id):
        for item in self.items:
            if item.id is id:
                return item
        return None

    def _load_json(self, name):
        from os import path
        from os.path import dirname as d
        path = d(d(d(__file__)))

        f = open(path.join(path, name), 'r')
        data = json.load(f)
        f.close()

        return data
    
    def _dump_json(self, name, data):
        from os import path
        from os.path import dirname as d
        path = d(d(d(__file__)))

        f = open(path.join(path, name), 'w')
        json.dump(data, f)
        f.close()
    
    def _load_schemas(self, schema, data: list) -> list:
        objects = list()
        for i in data:
            item = schema.load(i).data
            if hasattr(item, '_on_load'):
                item._on_load(self)
            objects.append(item)

        return objects
    
    def _dump_schemas(self, schema, data: list) -> list:
        objects = list()
        for i in data:
            objects.append(schema.dump(i).data)

        return objects
    
    def load(self):
        # Load the json files
        try:
            user = self._load_json(self.__class__.user_file)
            items = self._load_json(self.__class__.item_file)
            playlists = self._load_json(self.__class__.music_file)
        except OSError:
            print("Could not open database. dumping..")
            self.dump()
            return


        self.current_dm = user.get('dm')
        self.mods = user.get('mods')
        users = user.get('users', list())
        chars = user.get('chars', list())

        # load the items
        self.items = self._load_schemas(characters.ItemSchema(), items)
        # load the characters
        self.characters = self._load_schemas(characters.CharacterSchema(), chars)
        # load the playlists
        self.playlists = self._load_schemas(music.PlaylistSchema(), playlists)
        # load the users
        self.users = self._load_schemas(UserSchema(), users)
    
    def dump(self):
        # Create the base directory for the db if it doesn't exist
        if not os.path.isdir(self.__class__.base_dir):
            os.makedirs(self.__class__.base_dir)

        # dump the users
        users = self._dump_schemas(UserSchema(), self.users)
        # dump the playlists
        playlists = self._dump_schemas(music.PlaylistSchema(), self.playlists)
        # dump the characters
        chars = self._dump_schemas(characters.CharacterSchema(), self.characters)
        # dump the users
        items = self._dump_schemas(characters.ItemSchema(), self.items)
        
        # combine users and chars into one object
        user = dict(
            users=users,
            chars=chars,
            dm=self.current_dm,
            mods=self.mods
        )

        # write the json files
        self._dump_json(self.__class__.user_file, user)
        self._dump_json(self.__class__.item_file, items)
        self._dump_json(self.__class__.music_file, playlists)


db = Database()
