from marshmallow import Schema, fields, post_load


class Character:

    def __init__(self):
        self.db = None

        self.name = ""
        self.id = 0
        self.cls = ""
        self.race = ""
        self.stats = dict()
        self.body = dict()
        self.items = list()

        self.base_ac = 0
    
    def _on_load(self, db):
        self.db = db
    
    def __repr__(self):
        return "<Character(id={self.id}, name={self.name})>".format(self=self)


class CharacterSchema(Schema):
    name = fields.String()
    id = fields.Integer()
    stats = fields.Dict()
    body_ids = fields.Dict()
    items_ids = fields.List(fields.Integer())

    @post_load
    def make_character(self, data):
        char = Character()

        for key, val in data.items():
            setattr(char, key, val)
        
        return char


class Item:

    def __init__(self):
        self.db = None

        self.id = 0
        self.name = ""

        # The modifiers that affect the character when active.
        self.modifiers = dict()
        # The body parts that this item covers to be worn.
        self.wear_parts = list()
        # The body parts that need to be free in order for the item to be active.
        self.free_parts = list()
        # This item can be worn with other items at the same time when set
        self.stackable = False
        # The wear_parts become a list of possible places the item can be worn when set
        self.optional_wear = False

        self.is_weapon = False
        self.to_hit = ""
        self.damage = ""
    
    def _on_load(self, db):
        self.db = db
    
    def active(self, character: Character) -> (bool, str):
        """
        Return true if the item is active. for the given character.

        An error message is returned if the item is not active.

        :param character: the character to check.

        :returns (bool, str): is active, error message
        """

        wear = dict()
        free = dict()
        for key, val in character.body.items():
            if key in self.wear_parts:
                if self in val:
                    wear[key] = val
            if key in self.free_parts:
                free[key] = val
        
        # Find how many items are in the free items list.
        length = 0
        for val in free.values():
            length += len(val)
        if length is not 0:
            return False, ", ".join(free) + " needs to be empty"

        if len(wear) is 0:
            return False, "not being worn"

        return True, ""

    def donnable(self, character: Character) -> (bool, list):
        """
        returns true if the item can be put on.

        :param character: the character to check

        :returns (bool, list): whether the item can be donned, a list of parts the item can be donned on
        """
        
        wear = dict()
        for key, val in character.body.items():
            if key in self.wear_parts:
                wear[key] = val
        
        possible = list()
        for key, val in wear.items():
            # If there are no items being worn, it can be put on
            if len(val) is 0:
                possible.append(key)
                continue
            
            # If this item is stackable, it can be put on.
            if self.stackable:
                possible.append(key)
                continue
            
            # If every other item being worn is stackable, then it can be worn.
            for id in val:
                item = self.db.item(id)
                if not item or not item.stackable:
                    continue
            possible.append(key)

        if self.optional_wear:
            return len(possible) is not 0, possible
        else:
            donable = len(possible) is len(self.wear_parts)
            return donable, possible if donable else list()

    def __repr__(self):
        return '<Item({self.id}, {self.name})>'.format(self=self)


class Weapon(Item):
    pass


class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    modifiers = fields.Dict()
    wear_parts = fields.List(fields.String())
    free_parts = fields.List(fields.String())
    stackable = fields.Boolean()
    optional_wear = fields.Boolean()

    # Weapon schema
    is_weapon = fields.Boolean()
    to_hit = fields.String()
    damage = fields.String()

    @post_load
    def make_item(self, data):
        if data.get("is_weapon"):
            item = Weapon()
        else:
            item = Item()
        
        for key, val in data.items():
            setattr(item, key, val)
        
        return item

