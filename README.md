# EvalAI-CLI

<b>Official Command Line utility to use EvalAI in your terminal.</b>

EvalAI-CLI is designed to extend the functionality of the EvalAI web application to command line to make the platform more accessible and terminal-friendly to its users.

------------------------------------------------------------------------------------------

[![Join the chat at https://gitter.im/Cloud-CV/EvalAI](https://badges.gitter.im/Cloud-CV/EvalAI.svg)](https://gitter.im/Cloud-CV/EvalAI?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/Cloud-CV/evalai-cli.svg?branch=master)](https://travis-ci.org/Cloud-CV/evalai-cli)
[![Coverage Status](https://coveralls.io/repos/github/Cloud-CV/evalai-cli/badge.svg?branch=master)](https://coveralls.io/github/Cloud-CV/evalai-cli?branch=master)
[![Documentation Status](https://readthedocs.org/projects/markdown-guide/badge/?version=latest)](https://evalai-cli.cloudcv.org)


## Contributing Guidelines

If you are interested in contributing to EvalAI-CLI, follow our [contribution guidelines](https://github.com/Cloud-CV/evalai-cli/blob/master/.github/CONTRIBUTING.md).

## Development Setup

1. Setup the development environment for EvalAI and make sure that it is running perfectly.

2. Clone the evalai-cli repository to your machine via git

    ```bash
    git clone https://github.com/Cloud-CV/evalai-cli.git evalai-cli
    ```

3. Create a virtual environment

    ```bash
    cd EvalAI-CLI
    virtualenv -p python3 venv
    source venv/bin/activate
    ```

4. Install the package locally

    ```bash
    pip install -e .
    ```

5. Get auth token for EvalAI-CLI
- Open web browser and hit the url http://127.0.0.1:8888.
- Login with your credentials and move to the profile section.
- Click on `Get your Auth Token` to get the authentication token & download it as a JSON file.
- Create a folder with name `.evalai` in your home directory by using the command `mkdir ~/.evalai`.
- Place the downloaded authentication token in this folder by using the command `mv ~/Downloads/token.json ~/.evalai/`.


6. Login to cli using the command ``` evalai login```
Two users will be created by default which are listed below -

    ```bash
    Host User - username: host, password: password
    Participant User - username: participant, password: password
    ```

## Contributing Guidelines

If you are interested in contributing to EvalAI-CLI, follow our [contribution guidelines](https://github.com/Cloud-CV/evalai-cli/blob/master/.github/CONTRIBUTING.md).

