import os
from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
      LONG_DESCRIPTION = fh.read()


# All the pip dependencies required for installation.
INSTALL_REQUIRES = [
      'discord.py[voice]',
      'ruamel.yaml'
      # TODO setup voice dependencies
]


def params():

      name = "Dm's Assistant"

      version = "0.1"

      description = "A discord bot that helps you play Dungeons & Dragons with Discord"

      long_description = LONG_DESCRIPTION
      long_description_content_type = "text/markdown"

      install_requires = INSTALL_REQUIRES

      # https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers = [
            "Development Status :: 2 - Pre-Alpha",
            "Environment :: Console",
            "Intended Audience :: Other Audience",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Communications :: Chat",
            "Topic :: Games/Entertainment :: Role-Playing",
            "Topic :: Multimedia :: Sound/Audio"
      ]
      author = 'Noobot9k, TheVoiceInsideYourHead, Benjamin Jacobs'
      url = 'https://github.com/MemeMasters/Misaka-Mikoto-Meme-Machine-100-567'

      packages = ['dm_assist']

      entry_points = {
            'console_scripts': [
                  'dm_assist = dm_assist:serve'
            ]
      }

      return locals()


setup(**params())