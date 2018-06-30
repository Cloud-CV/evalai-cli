# Commands Overview

The EvalAI CLI commands are designed with efficiency and convenience in mind. The design is easy to remember and remains the same throughout all the commands.

EvalAI is invoked by typing `evalai` on the terminal. You can view the different sub-commands by using `evalai --help` 

The CLI is split into different sections or different subcommands.

- Challenges: View the different challenges sorted by time and participated.

- Challenge: View challenge specific details such as phases, splits, and even allows you to interact and make submissions.

- Teams: View and create you own teams.

- Submissions: View with submissions.

## Passing arguments and flags.

### Flags

Flags are optional additions used to specify a condition to return the results based on that condition. Flags are used in the CLI by passing it after the command is passed.

For example, for viewing all the challenges, you may use the command,

    `evalai challenges`

Which is going to return all the challenges.

But suppose you want to view only the challenges that you've participated in, you pass the flag `--participant` to the command.

    `evalai challenges --participant`

Which will return only the challenges you've participated in.


### Arguments

Some commands used for viewing details about a specific object such as:

- Details about a challenge.

- Details of a phase.

- Use a particular team.

- View submissions for a challenge.

These type of object specific commands needs to be passed mandatory object ID's. These are passed as arguments which have to be an Integer and should belong to the object 
you're trying to operate on.

For example,

If you want to view the phases of a particular challenge, you need to fetch the ID of the particular challenge you want to view.

You do that by taking the ID returned by the command

    `evalai challenges`

returns the details of the challenges along with the ID's. You take that ID and pass it on to the phase command.

    `evalai challenge CHALLENGE_ID phases`

returns you the phases of that particular challenge.

This is all the object specific commands are designed.
