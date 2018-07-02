# Commands Overview

The EvalAI CLI commands are designed with efficiency and convenience in mind. The design is easy to remember and remains the same throughout package.

EvalAI is invoked by typing `evalai` on the terminal. You can view the different sub-commands by using `evalai --help` 

The CLI is split into multiple sections according to functionality.

- Challenges: View the different challenges sorted by time and participated.

- Challenge: View challenge specific details such as phases, splits, and even allows you to interact and make submissions.

- Teams: View and create you own teams.

- Submissions: View with submissions.


## Flags

Flags are optional additions passed to a command to specify a specific condition and to return the results based on that.

#### Example

For viewing all the challenges, you use the command:

    evalai challenges

Which is going to return all the challenges.

But suppose you want to view only the challenges that you've participated in, you pass in the flag `--participant` to the command.

    evalai challenges --participant

Which will return only the challenges you've participated in.


## Arguments

Some commands used for viewing details about a specific object such as:

- Challenge: View phases, splits, details, leaderboard.

- Phase: View details, make submissions.

- Teams: Create teams, participate in challenges.

- Submissions: Viewing submission.

These type of object specific commands needs you to pass the object ID related to them to do operations on them.
These are passed as arguments which have to be an INTEGER and should be of belong to the object
you're trying to operate on, otherwise it'd can't recognise the object or would make a wrong operation.


#### Example

If you want to view the phases of a particular challenge, you need to mention the ID of the particular challenge that the phases belong to.

You do that by executing the command

    evalai challenges

which will return the details of the challenges along with the ID's. You take that ID and pass it on to the view the phases.

    evalai challenge CHALLENGE_ID phases

which will return the phases of that particular challenge.

This is all the object specific commands are designed.
