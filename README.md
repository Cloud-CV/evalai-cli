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


## Challenge

 Display all of the challenges                                 
    ```$
       evalai challenges 
    ```

 Display the ongoing challenges                                
    ```$
        evalai challenges ongoing
    ```
    
 Display the future challenges                                 
    ```$
        evalai challenges future 
    ```    

 Display the past challenges                                
    ```$
        evalai challenges past
    ```

 Display details of a challenge with the given ID (1)                                 
    ```$
        evalai challenge 1  
    ```
    
 Display all challenges that you've participated in                                
    ```$
        evalai challenges --participant
    ```

 Display all challenges that you've hosted                                  
    ```$
        evalai challenges --host
    ```    


## Challenge Phase

 Display all challenge phases of the challenge with Challenge the given ID (1)                                
    ```$
        evalai challenge 1 phases 
    ```    

 Display the details of the phase with the given phase ID (4) of the challenge with the given challenge ID (1)                                
    ```$
        evalai challenge 1 phase 4
    ```


## Teams    

 Participate in a challenge with the given challenge ID (1) and given team ID (2)                                
    ```$
       evalai challenge 1 participate 2 
    ``` 
 

 View your participant teams                                                                
    ```$
        evalai teams --participant 
    ```   

 View your host teams                                
    ```$
       evalai teams --host
    ```
    
 Create a participant team                                   
    ```$
        evalai teams create participant 
    ```
    
 Create a host team                                   
    ```$
        evalai teams create host 
    ```


## Leaderboards and Submissions

### Make a submission to the given Phase (4) of a given challenge with ID (1)

 If given Challenge ID (1) is Docker based                                
    ```$
        evalai push <image:tag> -p 4 
    ```
    
 If given Challenge ID (1) is not Docker based                                  
    ```$
        evalai challenge 1 phase 4 submit --file submission.json 
    ```
    
 View status of a submission with given ID (78)                                  
    ```$
        evalai submission 78 
    ```
    
 Get all the phase splits of the given challenge ID (1) with given phase ID (4)                                
    ```$
        evalai challenge 1 phase 4 splits 
    ```
    
 View the leaderboard of given Challenge ID (1) with given Challenge Phase Split ID (4)                                
    ```$
        evalai challenge 1 leaderboard 4 
    ```
    
 View all the submissions to given Phase ID (4) of the given challenge ID (1)                                
    ```$
        evalai challenge 1 phase 4 submissions 
    ```
    
 View all the submissions to given Phase ID (4) of the given challenge ID (1) between given dates (06/15/18) and (06/25/18)                                
    ```$
        evalai challenge 1 phase 4 submissions -s 06/15/18 -e 06/25/18 
    ```
## Configure your custom backend
### Configure the Host URL (OPTIONAL) 

##### For forked version host url is http://localhost:8000

##### For online version host url is https://evalapi.cloudcv.org                                                             
 Only run the following command if you want to use CLI with your forked version of EvalAI.                                       
    ```$
        evalai host -sh <host url> 
    ```
