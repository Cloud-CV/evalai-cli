<p align="center"><img width="65%" src="docs/static/images/evalai_logo.png" /></p>

------------------------------------------------------------------------------------------

[![Join the chat at https://gitter.im/Cloud-CV/EvalAI](https://badges.gitter.im/Cloud-CV/EvalAI.svg)](https://gitter.im/Cloud-CV/EvalAI?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/Cloud-CV/evalai-cli.svg?branch=master)](https://travis-ci.org/Cloud-CV/evalai-cli)
[![Coverage Status](https://coveralls.io/repos/github/Cloud-CV/evalai-cli/badge.svg?branch=master)](https://coveralls.io/github/Cloud-CV/evalai-cli?branch=master)

EvalAI is an open source web application that helps researchers, students and data-scientists to create, collaborate and participate in various AI challenges organized round the globe.

In recent years, it has become increasingly difficult to compare an algorithm solving a given task with other existing approaches. These comparisons suffer from minor differences in algorithm implementation, use of non-standard dataset splits and different evaluation metrics. By providing a central leaderboard and submission interface, we make it easier for researchers to reproduce the results mentioned in the paper and perform reliable & accurate quantitative analysis. By providing swift and robust backends based on map-reduce frameworks that speed up evaluation on the fly, EvalAI aims to make it easier for researchers to reproduce results from technical papers and perform reliable and accurate analyses.

<p align="center"><img width="65%" src="docs/static/images/kaggle_comparison.png" /></p>

A question we’re often asked is: Doesn’t Kaggle already do this? The central differences are:

- **Custom Evaluation Protocols and Phases**: We have designed versatile backend framework that can support user-defined evaluation metrics, various evaluation phases, private and public leaderboard.

- **Faster Evaluation**: The backend evaluation pipeline is engineered so that submissions can be evaluated parallelly using multiple cores on multiple machines via mapreduce frameworks offering a significant performance boost over similar web AI-challenge platforms.

- **Portability**: Since the platform is open-source, users have the freedom to host challenges on their own private servers rather than having to explicitly depend on Cloud Services such as AWS, Azure, etc.

- **Easy Hosting**: Hosting a challenge is streamlined. One can create the challenge on EvalAI using the intuitive UI (work-in-progress) or using zip configuration file.

- **Centralized Leaderboard**: Challenge Organizers whether host their challenge on EvalAI or forked version of EvalAI, they can send the results to main EvalAI server. This helps to build a centralized platform to keep track of different challenges. 

## Goal

The goal of this package is to offer almost all the features available on the website within your terminal.

## Development Setup

### Step 1:

Setup the development environment for EvalAI and make sure that django server & submission worker is running perfectly

### Step 2:

1. Clone the evalai-cli repository to your machine via git

```bash
git clone https://github.com/Cloud-CV/evalai-cli.git EvalAI-CLI
```

2. Create a virtual environment

```bash
$ cd EvalAI-CLI
$ virtualenv -v python3 venv
$ source venv/bin/activate
```
3. Install the package dependencies

```bash
$ pip install -r requirements.txt
```

4. Install the package locally to try it out

```bash
$ pip install -e .
```

## Contributing Guidelines

If you are interested in contributing to EvalAI-CLI, follow our [contribution guidelines](https://github.com/Cloud-CV/evalai-cli/blob/master/.github/CONTRIBUTING.md).
