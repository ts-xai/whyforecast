from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
import os


import click
import falcon
import tomli
from beaker.middleware import SessionMiddleware
from falcon_sqla import Manager as DatabaseMiddleware

from study_server.db_definitions import db_engine, DBConfiguration
from study_server.resources import ConsentResource, StudyResource, SurveyResource, CompleteResource, TutorialResource, \
    TutorialResource2,RecordResource
from falcon.routing import static

try:
    from bjoern import run as run_server  # noqa
except (ImportError, ModuleNotFoundError):
    from cheroot.wsgi import Server as HTTPServer


    def run_server(app: SessionMiddleware, host: str, port: int):  # pylint: disable=missing-function-docstring
        HTTPServer((host, port), app).start()


@dataclass
class StudyConfiguration:
    debug: bool
    db: str
    # pages
    consent: str
    tutorial: str
    tutorial2: str
    study: str
    survey: str
    complete: str
    # # server settings
    # host: str
    # port: int
    # session management
    encrypt: str
    validate: str
    expiration: int


def load_config(config_path: str) -> StudyConfiguration:
    try:
        with open(config_path, "rb") as file:
            toml_config = tomli.load(file)
    except Exception as e:
        logging.error(f"Failed to load configuration file: {e}")
        sys.exit(1)


    # Cookie settings
    toml_cookie = toml_config.get("cookie")
    expiration = toml_cookie.get("expiration", 86400)
    encrypt = toml_cookie and toml_cookie.get("encrypt")
    validate = toml_cookie and toml_cookie.get("validate")

    debug = False
    db= 'study.db'
    # Initialize and return the configuration data class with values from the TOML file
    return StudyConfiguration(debug=debug, db=db,
                              consent='consent.html', tutorial='tutorial.html', tutorial2='tutorial2.html',
                              study='study.html', survey='survey.html', complete='complete.html',
                              encrypt=encrypt, validate=validate, expiration=expiration)

# Example usage
config_path = 'template.toml'  # Adjust the path as necessary
config = load_config(config_path)


session_options = dict()
session_options["session.auto"] = True  # automatically save changes to the session
session_options["session.httponly"] = True  # boost security: https://owasp.org/www-community/HttpOnly
if config.expiration:
    session_options["session.cookie_expires"] = config.expiration

if config.debug:
    session_options["session.type"] = "memory"
else:
    session_options["session.type"] = "cookie"
    session_options["session.secure"] = False
    session_options["session.crypto_type"] = "cryptography"
    session_options["session.encrypt_key"] = config.encrypt
    session_options["session.validate_key"] = config.validate

# create a database session middleware
db_config = DBConfiguration(config.debug, config.db)
engine = db_engine(db_config)
db_middleware = DatabaseMiddleware(engine).middleware

# create the Falcon app
falcon_app = falcon.App(cors_enable=config.debug, middleware=[db_middleware])
falcon_app.add_route("/consent", ConsentResource(config.consent))
falcon_app.add_route("/study", StudyResource(config.study))
falcon_app.add_route("/survey", SurveyResource(config.survey))
falcon_app.add_route("/complete", CompleteResource(config.complete))
falcon_app.add_route('/tutorial', TutorialResource(config.tutorial))
falcon_app.add_route('/tutorial2', TutorialResource2(config.tutorial2))
falcon_app.add_route('/record', RecordResource())

current_directory = os.path.dirname(os.path.realpath(__file__))
print(current_directory)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
print(parent_directory)
figure_directory = os.path.join(parent_directory, 'figure')
print(figure_directory)
falcon_app.add_static_route("/figure", figure_directory)

# wrap the app in the Beaker middleware
app = SessionMiddleware(falcon_app, session_options)
