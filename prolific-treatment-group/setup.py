from setuptools import setup


setup(
    name="study-server",
    packages=["study_server"],
    version="0.1.0",
    description="A server for the study application.",
    author="Kim Bauters",
    author_email="kim.bauters@bristol.ac.uk",
    license="Protected",
    install_requires=[
        "pendulum",  # handle datetime instances with ease
        "dacite",  # convert dictionaries to dataclass instances
        "tomli",  # TOML configuration file parser
        "click",  # easy decorator style command line interface
        "requests",  # handle API requests
        "falcon",  # fast web framework
        "beaker",  # session management
        "cryptography",  # secure encryption
        "sqlalchemy",  # ORM for database access
        "falcon-sqla",  # SQL session middleware for falcon
    ],
    extras_require={
        "devel": ["cheroot", "pylint", "perflint"],  # pure Python WSGI server
        "production": ["bjoern"],  # fast WSGI server, requires apt install build-essential python3-dev libev-dev
    },
    classifiers=[],
    include_package_data=True,
    platforms="any",
)
