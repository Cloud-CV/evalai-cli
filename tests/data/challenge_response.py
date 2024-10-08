import datetime

timestamp = datetime.datetime.now()
timestamp = (
    timestamp.replace(year=timestamp.year + 1).strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    )[:-3]
    + "Z"
)

challenges = """
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "allowed_email_domains": [],
            "anonymous_leaderboard": false,
            "approved_by_admin": true,
            "blocked_email_domains": [],
            "creator": {
                "created_by": "host",
                "id": 2,
                "team_name": "South Lisafurt Host Team"
            },
            "description": "Excepturi eligendi minus modi delectus doloreasperiores voluptatem. \
            Aspernatur itaque vitae repellendus. Natus ut tenetur labore dolores ex repudiandae.",
            "enable_forum": true,
            "end_date": "%s",
            "evaluation_details": "Amet officia saepe quis tempora magnam eum. Quidem ab \
            consectetur exercitationem omnis. Nostrumconsequuntur architecto eaque mollitia \
            ab minima expedita quam. Velit itaque voluptates suscipit aliquam perspiciatis \
            itaque cupiditate.",
            "id": 2,
            "image": null,
            "is_active": true,
            "published": true,
            "short_description": "Ratione laboriosam quae tempora. Temporibus porro repellat \
            rem facere. In impedit cupiditate voluptatum aut omnis animi illo. Perferendis \
            ratione dolores eaque nulla iustomollitia facere voluptatum. Earum dolor corporis \
            quo enim quia optio.",
            "start_date": "2018-02-02T18:56:42.747134Z",
            "submission_guidelines": "Perspiciatis id sunt ab magni rerum laboriosam. Alias \
            temporibus ratione est animi. Quisquam reiciendis impedit fugiat corporis nesciunt \
            totam. Odit molestiae praesentium et fuga architecto suscipit. At deleniti fugiat \
            necessitatibus vel provident qui perspiciatis.",
            "terms_and_conditions": "Est vero fugiattemporibus necessitatibus. Ea nihil \
            possimus consequuntur doloribus odio. Vero voluptates non et repellat \
            perferendis ipsam. Ex dicta nemo numquam cupiditate recusandae impedit.",
            "title": "Olivia Challenge"
        },
        {
            "allowed_email_domains": [],
            "anonymous_leaderboard": false,
            "approved_by_admin": true,
            "blocked_email_domains": [],
            "creator": {
                "created_by": "host",
                "id": 2,
                "team_name": "South Lisafurt Host Team"
            },
            "description": "Voluptates consequatur commodi odit repellendus quam. Id nemo \
            provident ipsa cupiditate enim blanditiis autem. Recusandae veronecessitatibus \
            debitis esse eveniet consequatur. Provident saepe officiis incidunt cum.",
            "enable_forum": true,
            "end_date": "%s",
            "evaluation_details": "Adipisci possimus tenetur illum maiores. Laboriosam error \
            nostrum illum nesciunt cumque officiis suscipit. Occaecati velit fugiat alias \
            magnamvoluptas voluptatem ad. Repudiandae velit impedit veniam numquam.",
            "id": 3,
            "image": null,
            "is_active": false,
            "published": true,
            "short_description": "Dicta tempore quia itaque ex quam. Quas sequi in voluptates \
            esse aspernatur deleniti. In magnam ipsam totam ratione quidempraesentium eius \
            distinctio.",
            "start_date": "2016-12-29T18:56:42.752783Z",
            "submission_guidelines": "Ullam vitae explicabo consequuntur odit fugiat pariatur \
            doloribus ab. Qui ullam adipisci est corporis facilis. Quas excepturi \
            delenitidolorum tempora necessitatibus.",
            "terms_and_conditions": "Recusandae saepe ipsum saepe ullam aut. Cum eiusnihil \
            blanditiis itaque. Fugiat sed quod nostrum.",
            "title": "Jason Challenge"
        }
    ]
}
""" % (timestamp, timestamp)


challenge_details = """
{
    "allowed_email_domains": [],
    "anonymous_leaderboard": false,
    "approved_by_admin": true,
    "blocked_email_domains": [],
    "creator": {
        "created_by": "host",
        "id": 1,
        "team_name": "Lake Cynthiabury Host Team",
        "team_url": ""
    },
    "description": "Ex voluptatum accusantium dignissimos voluptatem eveniet enim non \
    aspernatur. Expedita consequatur velit vitae enim. Vel asperiores deserunt suscipit \
    non eaque veritatis labore. A atque illo fuga suscipit mollitia dignissimos assumenda.",
    "enable_forum": true,
    "end_date": "2019-11-11T06:31:31.594239Z",
    "evaluation_details": "Perspiciatis harum molestias iste corporis \
    aspernatur sit doloribus. Occaecati aliquid ullam odit aperiam in. Cupiditate consectetur \
    ab doloremque dolore.",
    "id": 1,
    "image": null,
    "is_active": true,
    "published": true,
    "short_description": "Nisi vero sint ipsam recusandae. Eveniet provident expedita iusto \
    atque delectus et recusandae. Odio blanditiis qui alias autem minima blanditiis. Iste et \
    ipsa minima placeat cupiditate fuga.",
    "start_date": "2018-03-21T06:31:31.594224Z",
    "submission_guidelines": "Ratione vitae dolor eos officia rem exercitationem. \
    Ipsam pariatur a alias mollitia perspiciatis. Ipsa sit esse officiis quam eaque.",
    "terms_and_conditions": "Officia dolores non labore nihil exercitationem minima. \
    Esse repellendus accusamus minus nisi. Commodi cum adipisci molestias ipsum beatae qui \
    enim porro. Cumque saepe distinctio repellendus et sed labore ratione aspernatur.",
    "title": "Sarah Challenge",
    "max_docker_image_size": 42949672960
}
"""


challenge_participant_teams = """
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "created_by": "host",
            "id": 3,
            "members": [
                {
                    "member_id": 5,
                    "member_name": "host",
                    "status": "Self"
                }
            ],
            "team_name": "Test1"
        }
    ]
}
"""


challenge_host_teams = """
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "created_by": "host",
            "id": 2,
            "members": [
                {
                    "id": 2,
                    "permissions": "Admin",
                    "status": "Self",
                    "team_name": 2,
                    "user": "host"
                }
            ],
            "team_name": "South Lisafurt Host Team"
        }
    ]
}
"""


challenge_phase_list = """
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "challenge": 10,
            "codename": "phase1",
            "description": "Ipsa id minima commodi quo itaque. Reprehenderit eos iusto\
             maiores iusto impedit dolores. Nihil possimus repudiandae animi quasi nulla\
              molestias reiciendis necessitatibus. Minus eos similique facilis accusamus\
               reprehenderit in officiis.",
            "end_date": "2019-09-25T18:56:42.789372Z",
            "id": 19,
            "is_active": false,
            "is_public": true,
            "leaderboard_public": true,
            "max_submissions": 100000,
            "max_submissions_per_day": 100000,
            "name": "Kimberly Phase",
            "start_date": "2018-08-21T18:56:42.789363Z"
        },
        {
            "challenge": 10,
            "codename": "phase2",
            "description": "Est nobis consequatur quam sint in nemo distinctio magni.\
             Eaque a natus laboriosam ipsa molestiae corrupti.",
            "end_date": "2019-09-25T18:56:42.789372Z",
            "id": 20,
            "is_active": false,
            "is_public": true,
            "leaderboard_public": true,
            "max_submissions": 100000,
            "max_submissions_per_day": 100000,
            "name": "Philip Phase",
            "start_date": "2018-08-21T18:56:42.789363Z"
        }
    ]
}
"""


challenge_phase_details = """
{
  "id": 42,
  "name": "Test Phase",
  "description": "Test Description",
  "leaderboard_public": "True",
  "start_date": "2019-01-01T00:00:00Z",
  "end_date": "2099-05-24T23:59:59Z",
  "challenge": 21,
  "max_submissions_per_day": 5,
  "max_submissions_per_month": 50,
  "max_submissions": 50,
  "is_public": "True",
  "is_active": "True",
  "is_submission_public": "True",
  "codename": "test",
  "test_annotation": "http://localhost:8000/media/test_annotations/6b95e923-76f7-490e-a2f7-551b354a07b8.pdf",
  "slug": "random-test-21",
  "max_concurrent_submissions_allowed": 3,
  "environment_image": "None",
  "is_restricted_to_select_one_submission": "False",
  "submission_meta_attributes": [
    {
      "name": "TextAttribute",
      "type": "text",
      "required": "True",
      "description": "Sample"
    },
    {
      "name": "SingleOptionAttribute",
      "type": "radio",
      "options": [
        "A",
        "B",
        "C"
      ],
      "required": "True",
      "description": "Sample"
    },
    {
      "name": "MultipleChoiceAttribute",
      "type": "checkbox",
      "options": [
        "alpha",
        "beta",
        "gamma"
      ],
      "required": "True",
      "description": "Sample"
    },
    {
      "name": "TrueFalseField",
      "type": "boolean",
      "required": "True",
      "description": "Sample"
    }
  ],
  "is_partial_submission_evaluation_enabled": "False",
  "config_id": 2,
  "allowed_submission_file_types": ".json, .zip, .txt, .tsv, .gz, .csv, .h5, .npy",
  "default_submission_meta_attributes": [
    {
      "name": "method_name",
      "is_visible": "True"
    },
    {
      "name": "method_description",
      "is_visible": "True"
    },
    {
      "name": "project_url",
      "is_visible": "True"
    },
    {
      "name": "publication_url",
      "is_visible": "True"
    }
  ]
}
"""

challenge_phase_details_slug = """
{
    "id": 2,
    "name": "test2019",
    "description": "This phase evaluates models on the test split of the GQA dataset",
    "leaderboard_public": true,
    "start_date": "2019-02-08T19:59:59Z",
    "end_date": "2099-05-15T23:59:59Z",
    "challenge": 10,
    "max_submissions_per_day": 2,
    "max_submissions_per_month": 10,
    "max_submissions": 10,
    "is_public": true,
    "is_active": true,
    "codename": "test2019",
    "slug": "philip-phase-2019",
    "submission_meta_attributes": [
    {
      "name": "TextAttribute",
      "type": "text",
      "required": "True",
      "description": "Sample"
    },
    {
      "name": "SingleOptionAttribute",
      "type": "radio",
      "options": [
        "A",
        "B",
        "C"
      ],
      "required": "True",
      "description": "Sample"
    },
    {
      "name": "MultipleChoiceAttribute",
      "type": "checkbox",
      "options": [
        "alpha",
        "beta",
        "gamma"
      ],
      "required": "True",
      "description": "Sample"
    },
    {
      "name": "TrueFalseField",
      "type": "boolean",
      "required": "True",
      "description": "Sample"
    }
  ]
}
"""


object_error = """
{
    "error": "Sorry, the object does not exist."
}
"""


invalid_token = '{"detail": "Invalid token"}'


token_expired = '{"detail": "Token has expired"}'


challenge_phase_splits = """
[
    {
        "challenge_phase": 4,
        "challenge_phase_name": "William Phase",
        "dataset_split": 3,
        "dataset_split_name": "Split 3",
        "id": 7,
        "visibility": 3
    },
    {
        "challenge_phase": 4,
        "challenge_phase_name": "William Phase",
        "dataset_split": 4,
        "dataset_split_name": "Split 4",
        "id": 8,
        "visibility": 3
    },
    {
        "challenge_phase": 3,
        "challenge_phase_name": "Scott Phase",
        "dataset_split": 3,
        "dataset_split_name": "Split 3",
        "id": 5,
        "visibility": 3
    },
    {
        "challenge_phase": 3,
        "challenge_phase_name": "Scott Phase",
        "dataset_split": 4,
        "dataset_split_name": "Split 4",
        "id": 6,
        "visibility": 3
    }
]
"""


leaderboard = """
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "challenge_phase_split": 189,
            "filtering_score": 0.8202264740335806,
            "id": 26652,
            "leaderboard__schema": {
                "default_order_by": "score",
                "labels": [
                    "score"
                ]
            },
            "result": [
                0.8202264740335806
            ],
            "submission__participant_team__team_name": "cyberagent",
            "submission__submitted_at": "2018-05-25T05:45:26.215498Z"
        },
        {
            "challenge_phase_split": 189,
            "filtering_score": 0.686372510737993,
            "id": 17372,
            "leaderboard__schema": {
                "default_order_by": "score",
                "labels": [
                    "score"
                ]
            },
            "result": [
                0.686372510737993
            ],
            "submission__participant_team__team_name": "ADVISE (PITT)",
            "submission__submitted_at": "2018-05-14T02:24:22.639441Z"
        },
        {
            "challenge_phase_split": 189,
            "filtering_score": 0.6226474033580632,
            "id": 16133,
            "leaderboard__schema": {
                "default_order_by": "score",
                "labels": [
                    "score"
                ]
            },
            "result": [
                0.6226474033580632
            ],
            "submission__participant_team__team_name": "VSE (PITT)",
            "submission__submitted_at": "2018-05-11T21:37:15.490292Z"
        },
        {
            "challenge_phase_split": 189,
            "filtering_score": 0.5284654431862553,
            "id": 27346,
            "leaderboard__schema": {
                "default_order_by": "score",
                "labels": [
                    "score"
                ]
            },
            "result": [
                0.5284654431862553
            ],
            "submission__participant_team__team_name": "planb",
            "submission__submitted_at": "2018-05-29T16:04:37.491494Z"
        },
        {
            "challenge_phase_split": 189,
            "filtering_score": 0.24709098008590394,
            "id": 27407,
            "leaderboard__schema": {
                "default_order_by": "score",
                "labels": [
                    "score"
                ]
            },
            "result": [
                0.24709098008590394
            ],
            "submission__participant_team__team_name": "titan",
            "submission__submitted_at": "2018-05-30T09:45:49.672613Z"
        },
        {
            "challenge_phase_split": 189,
            "filtering_score": 0.20484185864896526,
            "id": 15304,
            "leaderboard__schema": {
                "default_order_by": "score",
                "labels": [
                    "score"
                ]
            },
            "result": [
                0.20484185864896526
            ],
            "submission__participant_team__team_name": "idxm",
            "submission__submitted_at": "2018-05-09T08:51:10.900548Z"
        }
    ]
}
"""

empty_leaderboard = """
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": []
}
"""

get_submission_file_presigned_url = """
{
    "presigned_urls": [
        {
            "partNumber": 1,
            "url": "https://staging-evalai.s3.amazonaws.com/media/submission_files/submission_403/5fb32be8-1fcf-42d3-9b9c-230e4027d656.json?uploadId=R8AlOJggehmUU87Ar2cDp2tF9p6Rez8iKmmWpwUD0Wi.VumJ6faNO_RFvkD3bJ4NzmokztAncqsd0JsUeslHGtK9m1B533gIQHbuxkwNgx_7F6_YTxtoUpqMHxFtY4Si&partNumber=1&Signature=Bga2IIsvDfJFOAMnZ5G64y0%3D&Expires=1603971221"
        }
    ],
    "upload_id": "R8AlOJggehmUU87Ar2cDp2tF9p6Rez8iKmmWpwUD0Wi.VumJ6faNO_RFvkD3bJ4NzmokztAncqsd0JsUeslHGtK9m1B533gIQHbuxkwNgx_7F6_YTxtoUpqMHxFtY4Si",
    "submission_pk": 9
}
"""  # noqa: E501

upload_file_to_s3 = """
{
    "parts": "[
        {
            "ETag": "\\"8e31830e7ed2b537d7fff83ef2525384\\"",
            "PartNumber": 1
        }
    ]",
    "upload_id": "R8AlOJggehmUU87Ar2cDp2tF9p6Rez8iKmmWpwUD0Wi.VumJ6faNO_RFvkD3bJ4NzmokztAncqsd0JsUeslHGtK9m1B533gIQHbuxkwNgx_7F6_YTxtoUpqMHxFtY4Si"
}
"""  # noqa: E501

finish_submission_file_upload = """
{
    "upload_id": "R8AlOJggehmUU87Ar2cDp2tF9p6Rez8iKmmWpwUD0Wi.VumJ6faNO_RFvkD3bJ4NzmokztAncqsd0JsUeslHGtK9m1B533gIQHbuxkwNgx_7F6_YTxtoUpqMHxFtY4Si",
    "submission_pk": 9
}
"""  # noqa: E501

part_file_upload_to_s3 = """
{
    "ETag": "\\"8e31830e7ed2b537d7fff83ef2525384\\""
}
"""

send_submission_message = """
{
    "submission_pk": 9,
    "phase_pk": 2,
    "challenge_pk": 1,
}
"""

get_annotation_file_presigned_url = """
{
    "presigned_urls": [
        {
            "partNumber": 1,
            "url": "https://staging-evalai.s3.amazonaws.com/media/test_annotations/8af3d688-f559-49be-ab20-16e02805d228.txt?uploadId=40_2O5xMNg6dBZonEAIXNJdEmcwbAHDQpXzdM9ITvEawkBW96BCSZTcZf4qxNMfzK2ZhkJfjonuG6a4aP40UCY6EK8y66trEMf1AzlOs1VjNrg.T9nAaMPOIavDQLKJw&partNumber=1&Signature=lkHj9JhsvodXNnbKE%2F7y9t3E%3D&Expires=1603971332"
        }
    ],
    "upload_id": "40_2O5xMNg6dBZonEAIXNJdEmcwbAHDQpXzdM9ITvEawkBW96BCSZTcZf4qxNMfzK2ZhkJfjonuG6a4aP40UCY6EK8y66trEMf1AzlOs1VjNrg.T9nAaMPOIavDQLKJw"
}
"""  # noqa: E501

finish_annotation_file_upload = """
{
    "upload_id": "40_2O5xMNg6dBZonEAIXNJdEmcwbAHDQpXzdM9ITvEawkBW96BCSZTcZf4qxNMfzK2ZhkJfjonuG6a4aP40UCY6EK8y66trEMf1AzlOs1VjNrg.T9nAaMPOIavDQLKJw",
    "challenge_phase_pk": 2
}
"""  # noqa: E501

annotation_part_file_upload_to_s3 = """
{
    "ETag": "\\"30bb2b9819ff69e7891523af9ad66b49\\""
}
"""
