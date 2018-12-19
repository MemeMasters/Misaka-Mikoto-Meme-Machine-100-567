import os
import json
from marshmallow import Schema, fields, post_load

from . import characters


class User:

    def __init__(self):
        self.id = 0
        self.characters = list()
    
    def _on_load(self, db):
        chars = db.characters

        ids = [x.id for x in self.characters]
        self.characters = list()

        for char in chars:
            if char.id in ids:
                self.characters.append(char)
    
    def __repr__(self):
        ids = [x.id for x in self.characters]
        return '<User(id={self.id}, characters={chars})>'.format(self=self, chars=ids)


class UserSchema(Schema):
    id = fields.Integer()
    characters = fields.Nested(characters.CharacterSchema, only=['id'], many=True)

    @post_load
    def create_User(self, data):
        user = User()

        for key, val in data.items():
            setattr(user, key, val)
        
        return user


class Database:

    user_file = "db.dat/users.json"
    item_file = "db.dat/items.json"

    def __init__(self):
        self.users = list()
        self.items = list()
        self.characters = list()
    
    def item(self, id):
        for item in self.items:
            if item.id is id:
                return item
        return None
    
    def load(self):
        from os import path
        from os.path import dirname as d
        path = d(d(d(__file__)))

        # Load the json files
        user_f = open(path.join(path, self.__class__.user_file), 'r')
        user = json.load(user_f)
        user_f.close()

        item_f = open(path.join(path, self.__class__.item_file), 'r')
        items = json.load(item_f)
        item_f.close()

        users = user.get('users', list())
        chars = user.get('chars', list())

        # load the items
        self.items = list()
        item_schema = characters.ItemSchema()
        for i in items:
            item = item_schema.load(i).data
            item._on_load(self)
            self.items.append(item)

        # load the characters
        self.characters = list()
        char_schema = characters.CharacterSchema()
        for c in chars:
            char = char_schema.load(c).data
            char._on_load(self)
            self.characters.append(char)

        # load the users
        self.users = list()
        user_schema = UserSchema()
        for u in users:
            user = user_schema.load(u).data
            # Load the characters into the user data
            user._on_load(self)
            self.users.append(user)
        
    
    def dump(self):
        from os import path
        from os.path import dirname as d
        path = d(d(d(__file__)))

        users = list()
        chars = list()
        items = list()

        # dump the users
        user_schema = UserSchema()
        for u in self.users:
            users.append(user_schema.dump(u).data)
        
        # dump the characters
        char_schema = characters.CharacterSchema()
        for c in self.characters:
            chars.append(char_schema.dump(c).data)
        
        # dump the users
        item_schema = characters.ItemSchema()
        for i in self.items:
            items.append(item_schema.dump(i).data)
        
        # combine users and chars into one object
        user = dict(users=users, chars=chars)

        # write the json files
        user_f = open(path.join(path, self.__class__.user_file), 'w')
        json.dump(user, user_f)
        user_f.close()

        item_f = open(path.join(path, self.__class__.item_file), 'w')
        json.dump(items, item_f)
        item_f.close()


db = Database()
