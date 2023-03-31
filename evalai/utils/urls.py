from enum import Enum


class URLS(Enum):
    login = "/api/auth/login"
    get_access_token = "/api/accounts/user/get_auth_token"
    challenge_list = "/api/challenges/challenge/all/all/all"
    past_challenge_list = "/api/challenges/challenge/past/approved/public"
    future_challenge_list = "/api/challenges/challenge/future/approved/public"
    challenge_details = "/api/challenges/challenge/{}"
    challenge_phase_details = "/api/challenges/challenge/phase/{}/"
    participant_teams = "/api/participants/participant_team"
    host_teams = "/api/hosts/challenge_host_team/"
    host_challenges = "/api/challenges/challenge_host_team/{}/challenge"
    challenge_phase_split_detail = "/api/challenges/{}/challenge_phase_split"
    create_host_team = "/api/hosts/create_challenge_host_team"
    host_team_list = "/api/hosts/challenge_host_team/"
    participant_challenges = "/api/participants/participant_team/{}/challenge"
    participant_team_list = "/api/participants/participant_team"
    participate_in_a_challenge = (
        "/api/challenges/challenge/{}/participant_team/{}"
    )
    challenge_phase_list = "/api/challenges/challenge/{}/challenge_phase"
    challenge_phase_detail = "/api/challenges/challenge/{}/challenge_phase/{}"
    my_submissions = "/api/jobs/challenge/{}/challenge_phase/{}/submission/"
    make_submission = "/api/jobs/challenge/{}/challenge_phase/{}/submission/"
    get_submission = "/api/jobs/submission/{}"
    leaderboard = "/api/jobs/challenge_phase_split/{}/leaderboard/"
    get_aws_credentials = (
        "/api/challenges/phases/{}/participant_team/aws/credentials/"
    )
    download_file = "/api/jobs/submission_files/?bucket={}&key={}"
    phase_details_using_slug = "/api/challenges/phase/{}/"
    get_presigned_url_for_annotation_file = "/api/challenges/phases/{}/get_annotation_file_presigned_url/"
    get_presigned_url_for_submission_file = "/api/jobs/phases/{}/get_submission_file_presigned_url/"
    finish_upload_for_submission_file = "/api/jobs/phases/{}/finish_submission_file_upload/{}/"
    finish_upload_for_annotation_file = "/api/challenges/phases/{}/finish_annotation_file_upload/"
    send_submission_message = "/api/jobs/phases/{}/send_submission_message/{}/"
    terms_and_conditions_page = "/web/challenges/challenge-page/{}/evaluation"
