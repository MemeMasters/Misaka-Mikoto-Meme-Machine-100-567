from marshmallow import Schema, fields, post_load


class Playlist:

    def __init__(self):
        self.user = 0
        
        self.genres = dict()
    

class PlaylistSchema(Schema):
    user = fields.Integer()
    genres = fields.Dict()

    @post_load
    def create_playlist(self, data):
        pl = Playlist()

        for atr, val in data.items():
            setattr(pl, atr, val)
        
        return pl
