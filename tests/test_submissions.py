import docker
import json
import os
import pytest
import responses
import socket

from click.testing import CliRunner
from datetime import datetime
from dateutil import tz

from evalai.challenges import challenge
from evalai.submissions import submission, push
from tests.data import submission_response, challenge_response

from evalai.utils.config import API_HOST_URL
from evalai.utils.urls import URLS
from .base import BaseTestClass


class TestGetSubmissionDetails(BaseTestClass):
    def setup(self):

        self.submission = json.loads(submission_response.submission_result)

        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.get_submission.value).format("9"),
            json=self.submission,
            status=200,
        )

        responses.add(
            responses.GET,
            self.submission["submission_result_file"],
            json=json.loads(submission_response.submission_result_file),
            status=200,
        )

    @responses.activate
    def test_display_submission_details(self):
        team_title = "\n{}".format(self.submission["participant_team_name"])
        sid = "Submission ID: {}\n".format(str(self.submission["id"]))

        team = "{} {}".format(team_title, sid)

        status = "\nSubmission Status : {}\n".format(self.submission["status"])
        execution_time = "\nExecution Time (sec) : {}\n".format(
            self.submission["execution_time"]
        )

        date = datetime.strptime(
            self.submission["submitted_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        date = date.replace(tzinfo=from_zone)
        converted_date = date.astimezone(to_zone)

        date = converted_date.strftime("%D %r")
        submitted_at = "\nSubmitted At : {}\n".format(date)
        submission_data = "{}{}{}{}\n".format(
            team, status, execution_time, submitted_at
        )

        runner = CliRunner()
        result = runner.invoke(submission, ["9"])
        response = result.output
        assert response == submission_data

    @responses.activate
    def test_display_submission_details_with_a_string_argument(self):
        expected = (
            "Usage: submission [OPTIONS] SUBMISSION_ID COMMAND [ARGS]...\n"
            '\nError: Invalid value for "SUBMISSION_ID": two is not a valid integer\n'
        )
        runner = CliRunner()
        result = runner.invoke(submission, ["two"])
        response = result.output
        assert response == expected

    @responses.activate
    def test_display_submission_details_with_no_argument(self):
        expected = (
            "Usage: submission [OPTIONS] SUBMISSION_ID COMMAND [ARGS]...\n"
            '\nError: Missing argument "SUBMISSION_ID".\n'
        )
        runner = CliRunner()
        result = runner.invoke(submission)
        response = result.output
        assert response == expected

    @responses.activate
    def test_display_submission_result(self):
        expected = "{}\n".format(
            submission_response.submission_result_file
        ).strip()
        runner = CliRunner()
        result = runner.invoke(submission, ["9", "result"])
        response = result.output.strip()
        assert response == expected


class TestMakeSubmission(BaseTestClass):
    def setup(self):
        self.submission = json.loads(submission_response.submission_result)

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format(
                "1", "2"
            ),
            json=self.submission,
            status=200,
        )

        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.make_submission.value).format(
                "10", "2"
            ),
            json=self.submission,
            status=200,
        )

        # To get AWS Credentials
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.get_aws_credentials.value).format(
                "2"
            ),
            json=json.loads(submission_response.aws_credentials),
            status=200,
        )

        # To get Challenge Phase Details
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(
                API_HOST_URL, URLS.challenge_phase_details.value
            ).format("2"),
            json=json.loads(challenge_response.challenge_phase_details),
            status=200,
        )

        # To get Challenge Phase Details
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_phase_detail.value).format(
                "1", "2"
            ),
            json=json.loads(challenge_response.challenge_phase_details),
            status=200,
        )

        # To get Challenge Phase Details using slug
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(
                API_HOST_URL, URLS.phase_details_using_slug.value
            ).format("philip-phase-2019"),
            json=json.loads(challenge_response.challenge_phase_details_slug),
            status=200,
        )

        # To get Challenge Details
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_details.value).format(
                "10"
            ),
            json=json.loads(challenge_response.challenge_details),
            status=200,
        )

        # To get presigned URLs for submission upload parts
        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.get_presigned_url_for_submission_file.value).format(
                "2",
            ),
            json=json.loads(challenge_response.get_submission_file_presigned_url),
            status=200,
        )

        # To finish mulitpart file upload
        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.finish_upload_for_submission_file.value).format(
                "2", "9"
            ),
            json=json.loads(challenge_response.finish_submission_file_upload),
            status=200,
        )

        # To get presigned URL for part
        presigned_url_response = json.loads(challenge_response.get_submission_file_presigned_url)
        part_file_upload_url = presigned_url_response["presigned_urls"][0]["url"]
        responses.add(
            responses.PUT,
            part_file_upload_url,
            headers=json.loads(challenge_response.part_file_upload_to_s3),
            status=200,
        )

        # To publish submission message
        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.send_submission_message.value).format(
                "2", "9"
            )
        )

        # To get presigned URLs for submission upload parts
        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.get_presigned_url_for_annotation_file.value).format(
                "2",
            ),
            json=json.loads(challenge_response.get_annotation_file_presigned_url),
            status=200,
        )

        # To finish mulitpart file upload
        url = "{}{}"
        responses.add(
            responses.POST,
            url.format(API_HOST_URL, URLS.finish_upload_for_annotation_file.value).format(
                "2"
            ),
            json=json.loads(challenge_response.finish_annotation_file_upload),
            status=200,
        )

        # To get presigned URL for part
        presigned_url_response = json.loads(challenge_response.get_annotation_file_presigned_url)
        part_file_upload_url = presigned_url_response["presigned_urls"][0]["url"]
        responses.add(
            responses.PUT,
            part_file_upload_url,
            headers=json.loads(challenge_response.annotation_part_file_upload_to_s3),
            status=200,
        )

        responses.add_passthru("http+docker://localhost/")

    @responses.activate
    def test_make_submission_when_file_is_not_valid(self):
        expected = (
            "Usage: challenge phase submit [OPTIONS]\n"
            '\nError: Invalid value for "--file": Could not open file: file: No such file or directory\n'
        )
        runner = CliRunner()
        result = runner.invoke(
            challenge, ["1", "phase", "2", "submit", "--file", "file"]
        )
        response = result.output
        assert response == expected

    @responses.activate
    def test_make_submission_when_file_is_valid_without_metadata(self):
        expected = (
            "Your file {} with the ID {} is successfully submitted.\n\n"
            "You can use `evalai submission {}` to view this submission's status."
        ).format("test_file.txt", "9", "9")
        expected = (
            "Do you want to include the Submission Details? [y/N]: N\n"
            "Do you want to include the Submission Metadata? [y/N]: N\n\n{}".format(
                expected
            )
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt"],
                input="N\nN",
            )
            assert result.exit_code == 0
            assert result.output.strip() == expected

    @responses.activate
    def test_make_submission_when_file_is_valid_with_metadata(self):
        expected = "Do you want to include the Submission Details? [y/N]: Y"
        expected = "{}\n{}".format(
            expected,
            (
                "Method Name []: Test\nMethod Description []: "
                "Test\nProject URL []: Test\nPublication URL []: Test\n"
            ),
        )
        expected = "{}{}".format(
            expected,
            "Do you want to include the Submission Metadata? [y/N]: Y\n",
        )
        expected = "{}{}".format(
            expected,
            (
                "TextAttribute* (Sample) []: Test\nSingleOptionAttribute* (Sample):\n"
                "Choices:['A', 'B', 'C'] []: A\nMultipleChoiceAttribute* (Sample):\n"
                "Choices(separated by comma):['alpha', 'beta', 'gamma']: alpha\nTrueFalseField* (Sample) []: True\n"
            ),
        )
        expected = "{}\n{}".format(
            expected,
            (
                "Your file {} with the ID {} is successfully submitted.\n\n"
                "You can use `evalai submission {}` to view this "
                "submission's status."
            ).format("test_file.txt", "9", "9"),
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt"],
                input="Y\nTest\nTest\nTest\nTest\nY\nTest\nA\nalpha\nTrue\n",
            )
            assert result.exit_code == 0
            assert result.output.strip() == expected

    @pytest.fixture()
    def test_make_submission_for_docker_based_challenge_setup(self, request):
        def get_open_port():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 0))
            s.listen(1)
            port = s.getsockname()[1]
            s.close()
            return port

        registry_port = get_open_port()
        client = docker.from_env()
        image_tag = "evalai-push-test:v1"
        client.images.build(
            path=os.path.join(os.path.dirname(__file__), "data"), tag=image_tag
        )
        container = client.containers.run(
            "registry:2",
            name="registry-test",
            detach=True,
            ports={"5000/tcp": registry_port},
            auto_remove=True,
        )

        def test_make_submission_for_docker_based_challenge_teardown():
            container.stop(timeout=1)

        request.addfinalizer(
            test_make_submission_for_docker_based_challenge_teardown
        )
        return (registry_port, image_tag)

    @responses.activate
    def test_make_submission_for_docker_based_challenge_without_submission_metadata(
        self, test_make_submission_for_docker_based_challenge_setup
    ):
        registry_port, image_tag = (
            test_make_submission_for_docker_based_challenge_setup
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                push,
                [
                    image_tag,
                    "-p",
                    "philip-phase-2019",
                    "-u",
                    "localhost:{0}".format(registry_port),
                ],
                input="N\nN",
            )
            assert result.exit_code == 0

    @responses.activate
    def test_make_submission_for_docker_based_challenge_with_submission_metadata(
        self, test_make_submission_for_docker_based_challenge_setup
    ):
        registry_port, image_tag = (
            test_make_submission_for_docker_based_challenge_setup
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                push,
                [
                    image_tag,
                    "-p",
                    "philip-phase-2019",
                    "-u",
                    "localhost:{0}".format(registry_port),
                    "--public"
                ],
                input="Y\nTest\nTest\nTest\nTest\nY\nTest\nA\nalpha\nTrue\n",
            )
            assert result.exit_code == 0

    @responses.activate
    def test_make_submission_using_presigned_url(self, request):
        expected = (
            "Do you want to include the Submission Details? [y/N]: N\n"
            "Do you want to include the Submission Metadata? [y/N]: N\n"
            "Uploading the file...\n\n"
            "Your submission test_file.txt with the id 9 is successfully submitted for evaluation.\n\n"
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt", "--large"],
                input="N\nN"
            )
            response = result.output

            # Remove progress bar from response
            splitted_response = response.split("\n")
            splitted_response.pop(3)
            response = "\n".join(splitted_response)
            assert response == expected

    @responses.activate
    def test_upload_annotation_using_presigned_url(self, request):
        expected = (
            "Uploading the file...\n\n"
            "The annotation file test_file.txt for challenge phase 2 is successfully uploaded.\n\n"
        )
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("1 2 3 4 5 6")

            result = runner.invoke(
                challenge,
                ["1", "phase", "2", "submit", "--file", "test_file.txt", "--large", "--annotation"],
                input="N"
            )
            response = result.output

            # Remove progress bar from response
            splitted_response = response.split("\n")
            splitted_response.pop(1)

            response = "\n".join(splitted_response)
            assert response == expected


class TestPush(BaseTestClass):
    def setup(self):
        url = "{}{}"
        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.phase_details_using_slug.value).format("20"),
            json=json.loads(challenge_response.challenge_phase_details_slug),
            status=200,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.challenge_details.value).format("10"),
            json=json.loads(challenge_response.challenge_details),
            status=200,
        )

        responses.add(
            responses.GET,
            url.format(API_HOST_URL, URLS.get_aws_credentials.value).format("2"),
            json=json.loads(submission_response.aws_credentials),
            status=200,
        )

    def test_push_when_image_is_not_valid(self):
        expected = (
            "Error: Please enter the tag name with image.\n\n"
            "For eg: `evalai push ubuntu:latest --phase 123`"
        )
        runner = CliRunner()
        result = runner.invoke(push, ["invalid-image", "--phase", "20"])
        response = result.output.strip()
        assert response == expected
        assert result.exit_code == 1

    def test_push_when_image_not_found(self):
        expected = "Error: Image not found. Please enter the correct image name and tag."
        runner = CliRunner()
        result = runner.invoke(push, ["foo:bar", "--phase", "20"])
        response = result.output.strip()
        assert response == expected
