import os
import logging

from . import logger

from contextlib import contextmanager
import signal

from . import config, marshmallow
from .config import config as conf
from .bot import Bot

_logger = logging.getLogger(__name__)

bot = Bot()

def create_token():
    if conf.config.get('token') is None or conf.config.get('token') == 'Insert Token Here':

        _logger.error("No token exists!")
        
        token = input("Enter Token (press enter to skip): ")
        if token == '':
            token = 'Insert Token Here'

        conf.config['token'] = token

        config.save()
        
        if token == 'Insert Token Here':
            _logger.info("** insert the token the token in '{}' before starting the bot again **".format(os.path.relpath(config.__config_file)))
            raise SystemExit


@contextmanager
def sigint_shutdown():

    original_sigint_handler = signal.getsignal(signal.SIGINT)

    def on_shutdown_req():
        _logger.info("Shutting down Bot..")
        bot.stop()
        marshmallow.db.dump()
        raise SystemExit

    signal.signal(signal.SIGINT, lambda sig, frame: on_shutdown_req())

    try:
        _logger.info("Press Ctrl-C to stop the Bot")
        yield
    except Exception:
        raise
    finally:
        signal.signal(signal.SIGINT, original_sigint_handler)

def serve(test=False):
    
    _logger.info("Loading configuration..")
    if not test:
        try:
            create_token()
        except SystemExit:
            return
    
    _logger.info("Loading Database..")
    marshmallow.db.load()
    
    if not test:
        _logger.info("Starting Bot..")
        with sigint_shutdown():
            bot.setup()
            bot.run()
        