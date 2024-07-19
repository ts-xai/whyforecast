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

from db_definitions import db_engine, DBConfiguration
from resources import ConsentResource, StudyResource, SurveyResource, CompleteResource, TutorialResource, \
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
    tutorial2:str
    study: str
    survey: str
    complete: str
    # server settings
    host: str
    port: int
    # session management
    encrypt: str
    validate: str
    expiration: int


@click.command()
@click.option("--config", required=True, type=click.Path(exists=True), help="Path to the TOML configuration file.")
@click.option("--db", required=True, type=click.Path(exists=True), help="Path to the SQLite database file.")
@click.option("--consent", required=True, type=click.Path(exists=True), help="Path to the consent form HTML template.")
@click.option("--tutorial2", required=True, type=click.Path(exists=True), help="Path to the tutorial HTML template.")
@click.option("--tutorial", required=True, type=click.Path(exists=True), help="Path to the tutorial HTML template.")
@click.option("--study", required=True, type=click.Path(exists=True), help="Path to the study HTML template.")
@click.option("--survey", required=True, type=click.Path(exists=True), help="Path to the survey HTML template.")
@click.option("--complete", required=True, type=click.Path(exists=True), help="Path to the completed HTML template.")
@click.option("--host", default=None,
              help="The server host address. Defaults to 127.0.0.1 if debug is False, 0.0.0.0 otherwise.")  # noqa
@click.option("--port", default=None, help="The server port number. Defaults to 8080.")
@click.option('--debug', is_flag=True, default=False, help="Whether the server runs is debug mode. Defaults to False.")
def cli(config: str, db: str, consent: str, tutorial: str, tutorial2: str, study: str, survey: str, complete: str, host: str | None, port: int, debug: bool):  # noqa, pylint: disable=invalid-name
    # load the TOML config file
    with open(config, "rb") as file:
        toml_config = tomli.load(file)

    # parse all the options
    toml_server = toml_config.get("server")
    host = host or (toml_server and toml_server.get("host")) or "127.0.0.1" if debug else "0.0.0.0"
    port = port or (toml_server and toml_server.get("port")) or 8080

    toml_cookie = toml_config.get("cookie")
    expiration = (toml_cookie and toml_cookie.get("expiration")) or 0 if debug else 60 * 60 * 24
    if debug:
        # no user cookie being used; set the encryption and validation keys to empty strings
        encrypt = ""
        validate = ""
    else:
        # user cookie is being used; check that the encryption and validation keys are set
        encrypt = toml_cookie and toml_cookie.get("encrypt")
        validate = toml_cookie and toml_cookie.get("validate")
        # if either key is not set, log and exit with an error code
        if not encrypt or not validate:
            logging.error("The 'encrypt' and 'validate' keys must be set in the TOML file when debug is False.")
            sys.exit(1)

    # initialise the configuration data class
    config = StudyConfiguration(debug, db, consent, tutorial, tutorial2, study, survey, complete, host, port, encrypt, validate, expiration)

    # run the main application
    main(config)


def main(config: StudyConfiguration):
    """
    Main entry point for the study application.
    :param config: The configuration settings to use.
    """

    # create the Beaker options
    session_options = dict()

    session_options["session.auto"] = True  # automatically save changes to the session
    session_options["session.httponly"] = True  # boost security: https://owasp.org/www-community/HttpOnly
    if config.expiration:
        session_options["session.cookie_expires"] = config.expiration

    if config.debug:
        session_options["session.type"] = "memory"
    else:
        session_options["session.type"] = "cookie"
        session_options["session.secure"] = True
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
    falcon_app.add_route('/record',RecordResource())


    current_directory = os.path.dirname(os.path.realpath(__file__))

    # 获取上级目录的路径
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

    # 构建 Figure 文件夹的路径
    figure_directory = os.path.join(parent_directory, 'Figure')


    print('current_directory:', current_directory)

    print('static_path:',parent_directory)
    print('figure_directory:', figure_directory)


    falcon_app.add_static_route("/figure", figure_directory)



    # wrap the app in the Beaker middleware
    app = SessionMiddleware(falcon_app, session_options)
    print(f"backend server running at {config.host}:{config.port}")

    try:
        run_server(app, config.host, config.port)
    except OSError as err:
        logging.error(f"unable to start the study server: {err}")


if __name__ == "__main__":
    cli()
    # cli(["--config", "template.toml", "--db", "study.db", "--consent", "consent.html", "--study", "study.html", "--survey", "survey.html", "--complete", "complete.html", "--debug"])
