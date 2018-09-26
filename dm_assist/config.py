import os
from os.path import dirname

from ruamel import yaml

__config_file = os.path.join(dirname(dirname(__file__)), 'config.yaml')
VERSION = 1

_conf = dict()

def save():
    """
    Save the config file
    """
    print("Saving config file..")

    res = yaml.round_trip_dump(_conf, indent=2, block_seq_indent=1)

    with open(__config_file, 'w', encoding='utf-8') as stream:
        stream.write(res)


def load():
    """
    Load the config file.
    """
    print("Loading Configuration file..")

    def load_defaults():
        global _conf
        _conf = get_defaults()
        save()

    if not os.path.exists(__config_file):
        load_defaults()
        return

    global _conf
    with open(__config_file, 'r', encoding='utf-8') as stream:
        _conf = yaml.round_trip_load(stream)
    
    if _conf is None:
        load_defaults()
        return
    
    version = _conf.get('_conf', -1)
    if version != VERSION:
        migrate(version)
        _conf['_conf'] = VERSION
        save()

    def mergeDict(old: dict, new: dict, layer=1) -> dict:
        """
        Merge a dictionary into another while prefering the old values over the new

        :param old: original dictionary
        :param new: new dictionary to merge
        """
        
        from collections import Mapping
        changed = False
        for key, val in new.items():
            # print("{} ({})".format(key, type(old.get(key))))
            if not key in old:
                print("{}Adding new value {}".format('  ' * layer, key))
                changed = True
                old[key] = val
            elif issubclass(type(old[key]), Mapping) and issubclass(type(val), Mapping):
                print("{}Merging dict {}".format('  ' * layer, key))
                changed = changed or mergeDict(old[key], val, layer + 1)

        return changed
    
    defaults = get_defaults()
    if mergeDict(_conf, defaults):
        save()


def get_defaults():
    defaults = dict()

    defaults['config'] = dict(
        voice=dict(
            opus='opus',
            default_volume=50
        ),
        prefix='!',
        token='Insert Token Here',
        random=dict(
            useRandomDotOrg=True,
            preFetchCount=20,
            preFetchCommonCount=30
        )
    )

    defaults['lines'] = dict(
        crits=[u"Headshot!", u"Critical Hit!", u"Booyeah!", u"Crit!", u"Finish him!", u"Get pwn'd!"],
        critFails=[u"Oof", u"Fatality!", u"Ouch, ooch, oof your bones!", u"That'll hurt in the morning..."],
        dumb=[u"...What did you think would happen?", u"...Why?", u"Are you ok?",  u"Do you need a doctor?",
              u"What else did you think it would do?"],
        memes=[u"You.", u"I'm running out of memes...", u"This entire project.", u"Ay, aren't you a funny guy.",
               u"<Insert something cringy here>",u"tElL mE a mEmE!1!111!!1!!!!one!111!11", u"Are you feeling it now mr. crabs?",
               u"1v1 me on rust, howbou dah?"],
        startup=[u"*Yawn* Hello friends!", u"おはようございます!", u"おはよう、お父さん", u"Ohayō, otōsan!",
                 "Alright, who's ready to die?", u"Greetings humans.", u"My body is Reggie."],
        shutdown=[u"Bye!", u"Farewell comrades!", u"さようなら、お父さん!", u"Misaka doesn't wish to leave."],
        on_roll={
            '69': [u'Nice.'],
            '7': [u'Seben is my FABORIT number! But my faborit FABORIT number is seben BILLION!'],
            '77': [u'Seben is my FABORIT number! But my faborit FABORIT number is seben BILLION!'],
            '777': [u'Seben is my FABORIT number! But my faborit FABORIT number is seben BILLION!'],
            '7777': [u'Seben is my FABORIT number! But my faborit FABORIT number is seben BILLION!'],
            '420': [u'(insert bad weed joke here)', u'Quick! someone call the weed!']
        },
        user_error=dict(
            no_user=[u"You don't even have a character!", u"You aren't registered in the system."],
            no_char=[u"You don't have any characters!", u"Why would you try to do this when you don't even have a character?"],
            wrong_char=[u"It looks like we have a missing character.  Let's start a search party", u":wave: This isn't the character you are looking for."],
            too_many_char=[u"You have too many characters, specify your character next time.", u"Do you expect me to do all the work around here!  Tell me which character next time."]
        )
    )

    defaults['music'] = dict(
        majestic=["https://soundcloud.com/vindsvept/at-the-edge-of-the-world", "https://soundcloud.com/vindsvept/castle-in-the-sky", "https://soundcloud.com/vindsvept/vindsvept-moments-respite", "https://soundcloud.com/vindsvept/conjuration", "https://soundcloud.com/vindsvept/vindsvept-vasaloppet", "https://soundcloud.com/vindsvept/ruthless", "https://soundcloud.com/vindsvept/vindsveptfallen", "https://soundcloud.com/vindsvept/vindsvept-quests-end", "https://soundcloud.com/vindsvept/heart-of-ice"],
        tavern=["https://soundcloud.com/vindsvept/through-the-woods-we-ran", "https://soundcloud.com/vindsvept/light-of-the-sea", "https://soundcloud.com/vindsvept/a-new-adventure", "https://soundcloud.com/vindsvept/vindsvept-unsung-heroes", "https://soundcloud.com/vindsvept/vindsvept-from-afar", "https://soundcloud.com/vindsvept/vindsvept-dryads-dream", "https://soundcloud.com/vindsvept/vindsvept-spellbound-part-two", "https://soundcloud.com/vindsvept/gjallarhorn-awaken-the-gods-feat-gaute-ohrn", "https://soundcloud.com/vindsvept/vindsvept-across-the-plains", "https://soundcloud.com/vindsvept/vindsvept-hearthfire", "https://soundcloud.com/vindsvept/untamed", "https://soundcloud.com/vindsvept/seven-flowers", "https://soundcloud.com/vindsvept/the-forgotten-forest", "https://soundcloud.com/vindsvept/nightfall", "https://soundcloud.com/vindsvept/skymning"],
        quest=["https://soundcloud.com/vindsvept/vindsvept-one-step-too-far", "https://soundcloud.com/vindsvept/into-the-unknown", "https://soundcloud.com/vindsvept/i-kvallsljus", "https://soundcloud.com/vindsvept/to-vigrith-the-field-of-battle", "https://soundcloud.com/vindsvept/fimbulwinter-winter-following-winter", "https://soundcloud.com/vindsvept/vindsvept-across-the-plains", "https://soundcloud.com/vindsvept/a-song-from-the-deep", "https://soundcloud.com/vindsvept/over-the-mountain"],
        travel=["https://soundcloud.com/vindsvept/into-silence-part-two", "https://soundcloud.com/vindsvept/keeper-of-the-forest", "https://soundcloud.com/vindsvept/into-the-unknown", "https://soundcloud.com/vindsvept/wildkin-glade", "https://soundcloud.com/vindsvept/vindsvept-dryads-dream", "https://soundcloud.com/vindsvept/vindsvept-across-the-plains", "https://soundcloud.com/vindsvept/vindsvept-westward"],
        calm=["https://soundcloud.com/vindsvept/into-silence", "https://soundcloud.com/vindsvept/evenfall", "https://soundcloud.com/vindsvept/keeper-of-the-forest", "https://soundcloud.com/vindsvept/vindsvept-moments-respite", "https://soundcloud.com/vindsvept/the-shapers-realm", "https://soundcloud.com/vindsvept/winters-night", "https://soundcloud.com/vindsvept/vindsvept-crystal-forest", "https://soundcloud.com/vindsvept/vindsvept-daylights-end", "https://soundcloud.com/vindsvept/the-fae", "https://soundcloud.com/vindsvept/the-journey-home", "https://soundcloud.com/vindsvept/chasing-shadows", "https://soundcloud.com/vindsvept/winters-tale", "https://soundcloud.com/vindsvept/moonless-night", "https://soundcloud.com/vindsvept/fall-of-the-leaf"],
        battle=["https://soundcloud.com/vindsvept/throat-of-the-world", "https://soundcloud.com/vindsvept/ruthless", "https://soundcloud.com/vindsvept/ragnarok-fate-of-the-gods", "https://soundcloud.com/vindsvept/naglfar-ship-of-the-dead", "https://soundcloud.com/vindsvept/the-fall", "https://soundcloud.com/vindsvept/last-stand", "https://soundcloud.com/vindsvept/guardian", "https://soundcloud.com/vindsvept/a-world-divided", "https://soundcloud.com/vindsvept/chasing-the-traitor-part-two", "https://soundcloud.com/vindsvept/heart-of-ice", "https://soundcloud.com/vindsvept/the-sirens-cadence", "https://soundcloud.com/vindsvept/on-the-other-side", "https://soundcloud.com/vindsvept/as-we-march"],
        sneak=["https://soundcloud.com/vindsvept/sons-of-loki-vanagandr-jormungandr", "https://soundcloud.com/vindsvept/mimers-advice-allfathers-hope", "https://soundcloud.com/vindsvept/vindsvept-season-unending", "https://soundcloud.com/vindsvept/wherever-the-path-may-lead", "https://soundcloud.com/vindsvept/over-the-mountain", "https://soundcloud.com/vindsvept/hollow", "https://soundcloud.com/vindsvept/clockwork", "https://soundcloud.com/vindsvept/lycanthropy", "https://soundcloud.com/vindsvept/illuminate"]
    )


    return defaults


def migrate(version):
    print("Migrating old config version from v{} to v{}..".format(version, VERSION))
    if version is -1:
        # There was no previous version, so there isn't anything we really can do
        return

class SettingDict:

    def __init__(self, config):
        self._conf = config
    
    def __getitem__(self, index):
        return self._conf[index]
    
    def __setitem__(self, index, value):
        self._conf[index] = value
    
    def __contains__(self, value):
        return value in self._conf
    
    def __iter__(self):
        return iter(self._conf)
    
    def __len__(self):
        return len(self._conf)
    
    def get(self, value, default=None):
        try:
            return self[value]
        except KeyError:
            return default

class Conf(SettingDict):

    def __init__(self, config):
        super().__init__(config)
        self._conf = config
        self._lines = Lines(self._conf['lines'])
        self._config = Config(self._conf['config'])
    
    @property
    def config(self):
        return self._config
    
    @property
    def lines(self):
        return self._lines
    
    @property
    def music(self):
        return self._conf['music']


class Lines(SettingDict):

    def __init__(self, lines):
        super().__init__(lines)
        self._lines = lines
        self._user_error = UserError(self._lines['user_error'])
    
    @property
    def critFails(self):
        return self._lines['critFails']
    
    @property
    def shutdown(self):
        return self._lines['shutdown']
    
    @property
    def startup(self):
        return self._lines['startup']
    
    @property
    def dumb(self):
        return self._lines['dumb']
    
    @property
    def crits(self):
        return self._lines['crits']
    
    @property
    def memes(self):
        return self._lines['memes']
    
    @property
    def on_roll(self):
        return self._lines['on_roll']
    
    @property
    def user_error(self):
        return self._user_error


class UserError(SettingDict):

    def __init__(self, config):
        super().__init__(config)
        self._error = config
    
    @property
    def no_user(self):
        return self._error['no_user']
    
    @property
    def no_char(self):
        return self._error['no_char']
    
    @property
    def wrong_char(self):
        return self._error['wrong_char']
    
    @property
    def too_many_char(self):
        return self._error['too_many_char']


class Config(SettingDict):

    def __init__(self, config):
        super().__init__(config)
        self._config = config
        self._voice = Voice(self._config['voice'])
        self._random = Random(self._config['random'])
    
    @property
    def voice(self):
        return self._voice
    
    @property
    def prefix(self):
        return self._config['prefix']
    
    @property
    def token(self):
        return self._config['token']

    @property
    def random(self):
        return self._random


class Voice(SettingDict):

    def __init__(self, voice):
        super().__init__(voice)
        self._voice = voice
    
    @property
    def opus(self):
        return self._voice['opus']
    
    @property
    def default_volume(self):
        return self._voice['default_volume']


class Random(SettingDict):

    def __init__(self, random):
        super().__init__(random)
        self._random = random
    
    @property
    def useRandomDotOrg(self):
        return self._random['useRandomDotOrg']

    @property
    def preFetchCount(self):
        return self._random['preFetchCount']
    
    @property
    def preFetchCommonCount(self):
        return self._random['preFetchCommonCount']

# Load the config on import
load()

config = Conf(_conf)
