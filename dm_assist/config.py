import os

from ruamel import yaml

TOKEN = 'token'
PREFIX = 'prefix'

__config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
config = dict()

def save():
    """
    Save the config file
    """
    print("Saving config file..")

    res = yaml.round_trip_dump(config, indent=2, block_seq_indent=1)

    with open(__config_file, 'w', encoding='utf-8') as stream:
        stream.write(res)


def load():
    """
    Load the config file.
    """
    print("Loading Configuration file..")

    def load_defaults():
        global config
        config = get_defaults()
        save()

    if not os.path.exists(__config_file):
        load_defaults()
        return

    global config
    with open(__config_file, 'r', encoding='utf-8') as stream:
        config = yaml.round_trip_load(stream)
    
    if config is None:
        load_defaults()
        return

    def mergeDict(old: dict, new: dict) -> dict:
        """
        Merge a dictionary into another while prefering the old values over the new

        :param old: original dictionary
        :param new: new dictionary to merge
        """
        changed = False
        for key, val in new.items():
            if not key in old:
                changed = True
                old[key] = val
            elif isinstance(old[key], dict) and isinstance(val, dict):
                changed = changed or mergeDict(old[key], val)

        return changed
    
    defaults = get_defaults()
    if mergeDict(config, defaults):
        save()


def get_defaults():
    defaults = dict()
    defaults[PREFIX] = '!'

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
        shutdown=[u"Bye!", u"Farewell comrades!", u"さようなら、お父さん!", u"Misaka doesn't wish to leave."]
    )

    defaults['voice'] = dict(
        opus='opus'
    )

    return defaults


# Load the config on import
load()