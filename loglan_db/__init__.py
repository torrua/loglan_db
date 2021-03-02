# -*- coding: utf-8 -*-
# pylint: disable=R0903
"""
This module contains functions and variables for initializing application and db
"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = "torrua"
__copyright__ = "Copyright 2020, loglan_db project"
__email__ = "torrua@gmail.com"

db = SQLAlchemy()
log = logging.getLogger(__name__)


class CLIConfig:
    """
    Configuration object for remote database
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL', None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config, database):
    """
    Create app
    """

    # app initialization
    app = Flask(__name__)

    app.config.from_object(config)

    # db initialization
    database.init_app(app)

    # database.create_all(app=app) when use need to re-initialize db
    return app


def app_lod(config_lod=CLIConfig, database=db):
    """
    Create LOD app with specified Config
    :param config_lod: Database Config
    :param database: SQLAlchemy() Database
    :return: flask.app.Flask
    """
    return create_app(config=config_lod, database=database)


def run_with_context(function):
    """Context Decorator"""
    def wrapper(*args, **kwargs):

        db_uri = os.environ.get('LOD_DATABASE_URL', None)

        if not db_uri:
            log.error("Please, specify 'LOD_DATABASE_URL' variable.")
            return

        context = app_lod().app_context()
        context.push()
        function(*args, **kwargs)
        context.pop()

    return wrapper
