from click.testing import CliRunner

from evalai.add_token import set_token
from evalai.login import login
from evalai.challenges import challenges, challenge


class TestIntegrationChallenges:
    def setUp(self):
        self.url = "{}{}"
        self.undefined_token = "0" * 40

        # Temporary Solution, a long term solution will have to be more dynamic
        # and adaptables
        # self.challenge_data_string = """
        # +-----+--------------------+------------------------------------------------------------------------------------------------------------------+----------+----------------------+----------------------+\n
        # | ID  |       Title        |                                                Short Description                                                 | Creator  |      Start Date      |       End Date       |\n
        # +-----+--------------------+------------------------------------------------------------------------------------------------------------------+----------+----------------------+----------------------+\n
        # | 163 | VQA Challenge 2019 | Recent progress in computer vision and natural language processing has demonstrated that lower-level tasks are m | VQA Team | 01/29/19 05:29:59 AM | 01/01/00 05:29:59 AM |\n
        # |     |                    | uch closer to being solved. We believe that the time is ripe to pursue higher-level tasks, one of which is Visua |          |                      |                      |\n
        # |     |                    | l Question Answering (VQA), where the goal is to be able to understand the semantics of scenes well enough to be |          |                      |                      |\n
        # |     |                    |          able to answer open-ended, free-form natural language questions (asked by humans) about images.         |          |                      |                      |\n
        # +-----+--------------------+------------------------------------------------------------------------------------------------------------------+----------+----------------------+----------------------+\n
        # """

    def set_token_to(self, token):
        runner = CliRunner()
        runner.invoke(set_token, token)

    def set_token_to_undefined(self):
        self.set_token_to(self.undefined_token)

    # def login_as_participant(self):
    #    runner = CliRunner()
    #    runner.invoke(login, ["participant", "password"])

    def test_challenges_when_token_is_invalid(self):
        self.set_token_to_undefined()
        runner = CliRunner()
        expected = "\nThe authentication token you are using isn't valid. Please generate it again.\n\n"
        result = runner.invoke(challenges)
        assert expected == result.output

    def test_challenge_details_when_challenge_id_is_not_int(self):
        self.login_as_participant()
        runner = CliRunner()
        expected = "{}{}".format(
            "Usage: evalai challenge [OPTIONS] CHALLENGE COMMAND [ARGS]...\n",
            "Error: Invalid value for \"CHALLENGE\": not_integer is not a valid integer\n"
        )
        result = runner.invoke(challenge, "not_integer")
        assert expected == result.output

    # def test_display_challenges_participated(self):
    #     self.set_token_to(self.valid_testuser_token)
    #
    #     runner = CliRunner()
    #     expected = "\n{}\n{}\n".format("Participated Challenges", self.challenge_data_string)
    #     result = runner.invoke(challenges, ["--participant"])
    #     assert expected == result.output
