<h4>Integration Tests for testing interaction between CLI and EvalAI server</h4>

Testing is a crucial part of the CI/CD process. Currently for the evalai-cli
project, we have unit tests to cover individual units in the code.
However, this uses the stubbing approach i.e. pre-defined responses that will be
used for a specific request. This approach makes the test far from how the
application is actually supposed to work in practice.

In the actual application, the CLI works with the EvalAI server. To test the
complete setup, integration tests are required.
