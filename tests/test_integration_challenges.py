from click.testing import CliRunner

from evalai.add_token import set_token
from evalai.challenges import challenges, challenge


class TestIntegrationChallenges:
    def setup(self):
        self.url = "{}{}"
        self.undefined_token = "0" * 40
        self.valid_testuser_token = "3c6dcbdb50b6edc2942f4629c0c1ca51fa80d88c"

        # Temporary Solution, a long term solution will have to be more dynamic
        # and adaptables
        self.challenge_data_string = """
        +------------+----------+--------------------------------------------------------------------------------------------------------------------------------------------+--------------+-----------+------+\n
        | Start Date | End Date |                                                                Description                                                                 | Submission G | Evaluatio | Term |\n
        |            |          |                                                                                                                                            |  uidelines   | n Details | s an |\n
        |            |          |                                                                                                                                            |              |           | d Co |\n
        |            |          |                                                                                                                                            |              |           | ndit |\n
        |            |          |                                                                                                                                            |              |           | ions |\n
        +------------+----------+--------------------------------------------------------------------------------------------------------------------------------------------+--------------+-----------+------+\n
        |  01/29/19  | 01/01/00 | b'Recent progress in computer vision and natural language processing has demonstrated that lower-level tasks are much closer to being solv | b'Please ent | b'The cha | b'Pl |\n
        |            |          | ed. We believe that the time is ripe to pursue higher-level tasks, one of which is Visual Question Answering (VQA), where the goal is to b | er "None" if | llenge ev | ease |\n
        |            |          | e able to understand the semantics of scenes well enough to be able to answer open-ended, free-form natural language questions (asked by h |  some field  | aluation  |  ref |\n
        |            |          | 017. The 2nd and 3rd editions of the VQA Challenge were organized in CVPR 2017 and CVPR 2018 on the VQA v2.0 dataset. The 1st edition of t | /Publication |  and code | o th |\n
        |            |          | umans) about images. VQA Challenge 2019 is the 4th edition of the VQA Challenge on the VQA v2.0 dataset introduced in Goyal et al., CVPR 2 | like Project | procedure | er t |\n
        |            |          | he VQA Challenge was organized in CVPR 2016 on the 1st edition (v1.0) of the VQA dataset introduced in Antol et al., ICCV 2015. VQA v2.0 d |  URL is not  |  is descr | e VQ |\n
        |            |          | ataset is more balanced and reduces language biases over VQA v1.0, and is about twice the size of VQA v1.0. For almost every question in t | there for a  | ibed on t | A Te |\n
        |            |          | nd instructions on the VQA website. In particular, please see the overview, download, evaluation and challenge pages for more details. We  | ubmission.'  | aluation  | of U |\n
        |            |          | he VQA v2.0 dataset, there are two similar images that have different answers to the question. To participate in the challenge, you can fi | particular s | he VQA Ev | rms  |\n
        |            |          | also provide dataset visualization and browser pages to give everyone a sense of the dataset contents. Note: All the timings mentioned are |              |  page.'   | se.' |\n
        |            |          |                                                          local to your timezone.'                                                          |              |           |      |\n
        +------------+----------+--------------------------------------------------------------------------------------------------------------------------------------------+--------------+-----------+------+\n
        """
        self.set_token_to(self.valid_testuser_token)

    def set_token_to(self, token):
        runner = CliRunner()
        runner.invoke(set_token, token)

    def set_token_to_undefined(self):
        self.set_token_to(self.undefined_token)

    def test_challenges_when_token_is_invalid(self):
        self.set_token_to_undefined()
        runner = CliRunner()
        expected = "\nThe authentication token you are using isn't valid. Please generate it again.\n\n"
        result = runner.invoke(challenges)
        assert expected == result.output

    def test_challenge_details_when_challenge_id_is_not_int(self):
        runner = CliRunner()
        expected = "{}{}".format(
            "Usage: challenge [OPTIONS] CHALLENGE COMMAND [ARGS]...\n\n",
            "Error: Invalid value for \"CHALLENGE\": x is not a valid integer\n"
        )
        result = runner.invoke(challenge, "x")
        assert expected == result.output

    def test_display_challenge_details(self):

        runner = CliRunner()
        expected = self.challenge_data_string
        result = runner.invoke(challenge, ["163"])
        assert expected == result.output
