# Basics
Run `evalai --help` to list all the commands the that EvalAI-CLI can execute.
It gives the following output.

```` 
Welcome to the EvalAI CLI.

Options:
  --help  Show this message and exit.

Commands:
  challenge   Display challenge specific details.
  challenges  Lists challenges
  host        View and configure the Host URL.
  submission  View submission specific details.
  teams       List all the participant/host teams of a challenge
````

# Usage

|                                                 Command                                                 	|                                  Use                                  	|                                                 Return                                                	|                                       Example                                       	|
|:-------------------------------------------------------------------------------------------------------:	|:---------------------------------------------------------------------:	|:-----------------------------------------------------------------------------------------------------:	|:-----------------------------------------------------------------------------------:	|
|                                            evalai challenges                                            	|             It displays the details of all the challenges.            	|                    Challenge ID, Title, Description, Creator, Start Date, End Date                    	|                                `$ evalai challenges`                                	|
|                                     evalai challenge [CHALLENGE-ID]                                     	|      It is used for viewing the details of a specific challenge.      	| Start Date, End Date, Description, Submission Guidelines, Evaluation Guidelines, Terms and Conditions 	|                                `$ evalai challenge 1`                               	|
|                                     evalai challenges --participant                                     	| It is used for viewing the challenges in which the user participated. 	|                    Challenge ID, Title, Description, Creator, Start Date, End Date                    	|                         `$ evalai challenges --participant`                         	|
|                                         evalai challenges --host                                        	|    It is used for viewing the challenges that the user has hosted.    	|                    Challenge ID, Title, Description, Creator, Start Date, End Date                    	|                             `$ evalai challenges --host`                            	|
|                                         evalai challenge ongoing                                        	|               It is used for viewing ongoing challenges.              	|                    Challenge ID, Title, Description, Creator, Start Date, End Date                    	|                             `$ evalai challenge ongoing`                            	|
|                                          evalai challenge past                                          	|        It is used for viewing challenges happened in the past.        	|                    Challenge ID, Title, Description, Creator, Start Date, End Date                    	|                              `$ evalai challenge past`                              	|
|                                         evalai challenge future                                         	|              It is used for viewing upcoming challenges.              	|                    Challenge ID, Title, Description, Creator, Start Date, End Date                    	|                             `$ evalai challenge future`                             	|
|                           evalai challenge [CHALLENGE-ID] phase [PHASE] splits                          	|                It is used for viewing the phase splits.               	|                        Challenge Phase ID, Dataset Split, Challenge Phase Name                        	|                        `$ evalai challenge 2 phase 1 splits`                        	|
|                            evalai challenge [CHALLENGE-ID] leaderboard [CPS]                            	|                It is used for viewing the leaderboard.                	|                                                                                                       	|                         `$ evalai challenge 2 leaderboard 1`                        	|
|                        evalai challenge [CHALLENGE-ID] phase [PHASE] submissions                        	|               It is used for viewing user's submissions.              	|                                                                                                       	|                      `$ evalai challenge 2 phase 1 submissions`                     	|
|                                               evalai host                                               	|                It is used to view the current host URL.               	|                                                                                                       	|                                   `$ evalai host`                                   	|
|                                       evalai host --set-host [URL]                                      	|                 It is used to configure the host URL.                 	|                                                                                                       	|                       `$ evalai host -sh http://0.0.0.0:8888`                       	|
|                                        evalai teams --participate                                       	|        It is used for viewing the teams, the user is a part of.       	|                                                                                                       	|                            `$ evalai teams --participate`                           	|
|                            evalai challenge [CHALLENGE-ID] participate [TEAM]                           	|           It is used for registering a team in a challenge.           	|                                                                                                       	|                         `$ evalai challenge 2 participate 1`                        	|
|                                  evalai challenge [CHALLENGE-ID] phases                                 	|           It is used for viewing the phases of a challenge.           	|                                                                                                       	|                            `$ evalai challenge 2 phases`                            	|
|                              evalai challenge [CHALLENGE-ID] phase [PHASE]                              	|        It is used for viewing a specific phrase of a challenge.       	|                                                                                                       	|                            `$ evalai challenge 2 phase 1`                           	|
|                    evalai challenge [CHALLENGE-ID] phase [PHASE] submit --file [FILE]                   	|            It is used for submitting a file in a challenge.           	|                                                                                                       	|                `$ evalai challenge 2 phase 1 submit --file ./main.py`               	|
|                                      evalai submission [SUBMISSION]                                     	|             It is used for viewing the user's submission.             	|                                                                                                       	|                               `$ evalai submission 5`                               	|
| evalai challenge [CHALLENGE-ID] phase [PHASE] submissions --start-date [M/D/YY] --end-date [M/D/YY] 	|   It is used for viewing submissions between a particular duration.   	|                                                                                                       	| `$ evalai challenge 2 phase 1 submissions --start-date 8/23/18 --end-date 11/27/18` 	|

# Remarks

* **CHALLENGE-ID**: It is an integer value.
* **PHASE**: It is an integer value.
* **CPS**: It is an integer value.
* **TEAM**: It is an integer value.
* **SUBMISSION**: It is an integer value.
