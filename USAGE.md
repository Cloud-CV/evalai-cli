## Usage Instructions

The EvalAI CLI commands are designed with efficiency and convenience in mind. The design is easy to remember and remains the same throughout package.

EvalAI is invoked by typing `evalai` on the terminal. You can view the different sub-commands by using `evalai --help` 
The CLI is split into multiple sections according to functionality.
 
- **Challenges**: View the different challenges sorted by time and participated.
 
- **Challenge**: View challenge specific details such as phases, splits, and even allows you to interact and make submissions.
 
 - **Teams**: View and create you own teams.
 
 - **Submissions**: View with submissions.

### Arguments
 Some commands are used for viewing details about a specific object such as:

 - **Challenge**: View phases, splits, details, leaderboard.
 
 - **Phase**: View details, make submissions.
 
 - **Teams**: Create teams, participate in challenges.
 
 - **Submissions**: Viewing submission.
 
You need these type of object specific commands to pass the object ID related to them to do operations on them. These are passed as arguments which have to be an INTEGER and should be of belong to the object you're trying to operate on, otherwise it can't recognise the object or it would make a wrong operation.

##### 1. For viewing all the current challenges

``evalai challenges``
The above step returns the following details.
- ID
- Title
- Short Description
- Creator
- Start Date
- End date  

**Example Usage**

``$ evalai challenges # Fetchs all the details of the challenges``
  
##### 2. For viewing specific challenge

``evalai challenge [CHALLENGE_ID]``
 The above step returns the following details.
- Start date
- End date
- Description
- Submission Guidelines
- Evaluation Guidelines
- Terms and Conditions

**Note** - The **CHALLENGE_ID** is an integer. If it is not known, you can try the 1st command and view the id of the challenge you wish to see.

**Example Usage**

``$ evalai challenge 3 # Fetch details of challenge with ID 3``

##### 3. For viewing the challenges that you've participated in.

``evalai challenges --participant``

##### 4. For viewing the challenges that you've hosted/participated.

Use participant/host as flag

**Example Usage**

``$ evalai challenge --participate``

##### 5. For viewing the ongoing/past/future challenges.

Use ongoing/past/future as an argument.

**Example Usage**

``$ evalai challenge ongoing``

##### 6. For viewing the phase splits.

``evalai challenge CHALLENGE phase PHASE splits``

**Example Usage**

``$ evalai challenge 1 phase 1 splits``

**Note** : [CHALLENGE] & [PHASE] are integer value. 

##### 7. For viewing leaderboard.

``evalai challenge CHALLENGE leaderboard CPS``

**Example Usage**

``$ evalai challenge 1 leaderboard 1``

**Note** : **CHALLENGE** & **CPS** are integer values.

##### 8. For viewing user's submission.

``evalai challenge CHALLENGE phase PHASE submissions``

**Note** : **CHALLENGE** & **PHASE** are integer values.

**Example Usage**

``$ evalai challenge 1 phase 1 submissions``

##### 9. To view the current host url.

``$ evalai host ``

##### 10. To configure URL

``evalai host --set-host <URL>``

**Example Usage**

``$ evalai host -sh http://localhost:8888``

##### 11. For viewing the teams, the user is part of.

``evalai teams [FLAG]``

Use participant/host as flag

**Example Usage**

``$ evalai teams --participate``

##### 12. For creating a team.

``evalai teams create [ARGUEMENT]``

Use participant/host as Argument

**Example Usage**

``$ evalai teams create --participate``

##### 13. For registering a team in a challenge.

``evalai challenge CHALLENEGE participate TEAM``

**Note** : **CHALLENGE** & **TEAM** are integer values.

**Example Usage**

``$ evalai challenge 1 participate 1``

##### 14. For viewing phases of a challenge.

``evalai challenge CHALLENGE phases``

**Note** : **CHALLENGE** is an integer value.

**Example Usage**

``$ evalai challenge 1 phases``

##### 15. For viewing a particular phase of a challenge

``evalai challenge CHALLENGE phase PHASE``

**Note** : **CHALLENGE** & **PHASE** are integer values.

**Example Usage**

``$ evalai challenge 1 phase 1``

##### 16. For submitting a file in a challenge.

``evalai challenge CHALLENGE phase PHASE submit --file FILE``

**Note** : **CHALLENGE** & **PHASE** are integer values.

**Example Usage**

``$ evalai challenge 1 phase 1 submit --file ../hello.txt``

##### 17. For viewing your submission.

``evalai submission SUBMISSION``

**Note** : **SUBMISSION** is an integer value.

**Example Usage**

``$ evalai submission 1``

##### 18. For filtering submission by date.

``evalai challenge CHALLENGE phase PHASE submissions --start-date MM/DD/YY --end-date MM/DD/YY``

**Note** : **CHALLENGE** & **PHASE** are integer values. Use `8` in month/date instead of `08`

**Example Usage**

``$ evalai challenge 1 phase 1 submissions --start-date 1/1/18 --end-date 12/30/18``
