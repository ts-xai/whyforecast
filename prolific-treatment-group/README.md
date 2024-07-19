# Prolific Study Template
This is the template for conducting studies using the Prolific academic research platform. It helps handle complex tasks including session management, participant verification from Prolific, and persistent data storage for the study.

## Getting Started
To get started, install the dependencies listed in the `setup.py` file. If you're using a Mac with an M-series processor, you might encounter some difficulties while installing the `cryptography` package.

## Running the Study
To configure your study, you'll need to modify a TOML configuration file. A template for this file, named `template.toml`, is provided. The most significant option you'll need to configure is the `debug` option. During development, it's recommended to set `debug` to `false` to avoid complications arising from server configurations. Once the configuration file is ready, you can initiate the study using the following command:

    python3 study_server/main.py --debug --config <path to config file> ...
    
The study allows templates for all components such as the consent, study, survey, and completion HTML. All of these need to be provided, for example:

	... --db study.db --consent consent.html --study study.html --survey survey.html --complete complete.html

To view all available command line options at any point, you can use:

    python3 study_server/main.py --help

The core part of the study occurs at the `/study` endpoint. The way the system interacts with this endpoint is defined in the `resources.py` file in the `StudyResource` class. If necessary, you can extend this class with additional code or files to support your specific study requirements.