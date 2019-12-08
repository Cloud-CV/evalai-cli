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

5. Login to cli using the command ``` evalai login```
Two users will be created by default which are listed below -

    ```bash
    Host User - username: host, password: password
    Participant User - username: participant, password: password
    ```

______________________________________________________________________________________________________________________

# Some Important Commands and their Usage

### Note: Things to be edited at your side are given within brackets

## Challenge

Display all of the challenges                                 
    ```bash
       evalai challenges 
      ```

Display the ongoing challenges                                
    ```bash
        evalai challenges ongoing
    ```
    
Display the upcoming challenges                                 
    ```bash
        evalai challenges upcoming
    ```    

Display the past challenges                                
    ```bash
        evalai challenges past
    ```

Display details of a challenge with the given ID (1)                                 
    ```bash
        evalai challenge 1  
    ```
    
Display all challenges that you've participated in                                
    ```bash
        evalai challenges --participant
    ```

Display all challenges that you've hosted                                  
    ```bash
        evalai challenges --host
    ```    


## Challenge Phase

Display all challenge phases of the challenge with Challenge the given ID (1)                                
    ```bash
        evalai challenge 1 phases 
    ```    

Display the details of the phase with the given phase ID (4) of the challenge with the given challenge ID (1)                                
    ```bash
        evalai challenge 1 phase 4
    ```


## Teams    

 Participate in a challenge with the given challenge ID (1) and given team ID (2)                                
    ```bash
       evalai challenge 1 participant 2 
    ``` 
 

 View your participant teams                                                                
    ```bash
        evalai teams --participant 
    ```   

 View your host teams                                
    ```bash
       evalai teams --host
    ```
    
 Create a participant team                                   
    ```bash
        evalai teams create participant 
    ```
    
 Create a host team                                   
    ```bash
        evalai teams create host 
    ```


## Leaderboards and Submissions

### Make a submission to the given Phase (4) of a given challenge with ID (1)

 If given Challenge ID (1) is Docker based                                
    ```bash
        evalai push <image:tag> -p 4 
    ```
    
 If given Challenge ID (1) is not Docker based                                  
    ```bash
        evalai challenge 1 phase 4 submit --file submission.json 
    ```
    
 View status of a submission with given ID (78)                                  
    ```bash
        evalai submission 78 
    ```
    
 Get all the phase splits of the given challenge ID (1) with given phase ID (4)                                
    ```bash
        evalai challenge 1 phase 4 splits 
    ```
    
 View the leaderboard of given Challenge ID (1) with given Challenge Phase Split ID (4)                                
    ```bash
        evalai challenge 1 leaderboard 4 
    ```
    
 View all the submissions to given Phase ID (4) of the given challenge ID (1)                                
    ```bash
        evalai challenge 1 phase 4 submissions 
    ```
    
 View all the submissions to given Phase ID (4) of the given challenge ID (1) between given dates (06/15/18) and (06/25/18)                                
    ```bash
        evalai challenge 1 phase 4 submissions -s 06/15/18 -e 06/25/18 
    ```
## Configure your custom backend
### Configure the Host URL (OPTIONAL)    
Only run the following command if you want to use CLI with your forked version of EvalAI.                                 
    ```bash
        evalai host -sh https://evalapi.cloudcv.org 
    ```
