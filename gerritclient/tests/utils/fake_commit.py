def get_fake_commit(commit_id=None):
    return {
        "commit": commit_id or "184ebe53805e102605d11f6b143486d15c23a09c",
        "parents": [
            {
                "commit": "1eee2c9d8f352483781e772f35dc586a69ff5646",
                "subject": "Migrate contributor agreements to All-Projects.",
            }
        ],
        "author": {
            "name": "Shawn O. Pearce",
            "email": "sop@google.com",
            "date": "2012-04-24 18:08:08.000000000",
            "tz": -420,
        },
        "committer": {
            "name": "Shawn O. Pearce",
            "email": "sop@google.com",
            "date": "2012-04-24 18:08:08.000000000",
            "tz": -420,
        },
        "subject": "Use an EventBus to manage star icons",
        "message": "Use an EventBus to manage star icons\n\n"
        "Image widgets that need to ...",
    }


def get_fake_commit_affiliation():
    return {"branches": ["master", "fake/branch"], "tags": ["fake_tag"]}
