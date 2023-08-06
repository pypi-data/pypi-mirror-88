import json
import requests


class PostMattermost:

    def __init__(self, _attachments):
        self.attachments = _attachments

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Attachment:

    def __init__(self, _fallback, _color, _text, _title, _title_link, _fields):
        self.fallback = _fallback
        self.color = _color
        self.text = _text
        self.title = _title
        self.title_link = _title_link
        self.fields = _fields


def send_file_to_mattermost(url_webhook, ci_project_url, ci_job_id, title):

    attachment = Attachment("Gitlab Artifact download",
                            "#FF8000",
                            "Gitlab Artifact download link CI-JOB : " + ci_job_id,
                            title,
                            ci_project_url + "/-/jobs/" + str(ci_job_id) + "/artifacts/download?file_type=archive",
                            [])

    post_mattermost = PostMattermost([attachment])

    payload = post_mattermost.to_json()
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.request("POST", url_webhook, headers=headers, data=payload)
    except requests.exceptions.HTTPError as exception:
        print(exception)
        exit(0)
    except requests.exceptions.ConnectionError as exception:
        print(exception)
        exit(0)
