import os
from os.path import dirname

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import alembic.config

class NotInitializedError(Exception):
    
    def __init__(self, message):
        super().__init__(message)


class Sql:
    
    _sql_file = os.path.join(dirname(__file__), 'sql.db')

    

    def __init__(self):
        self._base = declarative_base()

        self._engine = None
        self._session = None
    
    def _migrate_db(self):
        alembic_args = [
            '--raiseerr',
            'upgrade', 'head'
        ]
        curr_dir = os.getcwd()
        migrate_dir = dirname(os.path.realpath(__file__))

        # migrate the database to the latest version
        os.chdir(migrate_dir)
        alembic.config.main(argv=alembic_args)
        os.chdir(curr_dir)


    def init(self):

        self._migrate_db()

        # Create the database engine
        self._engine = create_engine('sqlite:///{}'.format(self.__class__._sql_file), pool_pre_ping=True)

        # Create the database file
        self._base.metadata.create_all(self._engine)

        # Create the sessionmaker
        self._session = sessionmaker(bind=self._engine, autoflush=False)

        session = self._session()
        session.commit()
        

    def getSession(self):
        if self._session is None:
            raise NotInitializedError("Sql object is not yet initialized.  Call init() first")
        return self._session()
    
    def getBase(self):
        return self._base

sql = Sql()

import dm_assist.sql.roleplay_model
