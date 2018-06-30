# Configuring the CLI.

## Configure the Host URL

Before you can start using the EvalAI-CLI to do operations, you have to configure the host URL of the EvalAI instance that you want to connect to.

In the rest of this docs, we would be using `http://evalapi.cloudcv.org/` URL which is where the backend for the EvalAI server is hosted.

We need to configure our CLI to work with this backend.

For this we can use the command.

    `evalai configure -sh http://evalapi.cloudcv.org/`

Now, the CLI is ready to communicate with the backend. If you want to reconfigure the CLI with a different instance of EvalAI, you can use the same command.

## Token Authentication

Now, you have to get your own unique token to connect to your own account for performing the different operations.

Step 1: Log in to your EvalAI account and go to you profile section.

Step 2: Click the `Get Authentication Token` button in your profile.

Step 3: Click `Download as JSON` to download the token in a file.

Step 4: In the terminal, switch to your home directory.

    `cd ~`

Step 5: Create a dedicated folder for EvalAI's configurations.

    `mkdir .evalai`

Step 5: Copy the `token.json` into the newly created `.evalai` folder.

    `mv Downloads/token.json ~/.evalai`

Now you're all set and ready to go!
