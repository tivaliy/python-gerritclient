def get_fake_comment(
    patch_set=None, comment_id=None, line=None, message=None, author=None
):
    """Creates a fake comment."""

    return {
        "patch_set": patch_set or 1,
        "id": comment_id or "TvcXrmjM",
        "line": line or 23,
        "message": message or "[nit] trailing whitespace",
        "updated": "2013-02-26 15:40:43.986000000",
        "author": author
        or {
            "_account_id": 1000096,
            "name": "John Doe",
            "email": "john.doe@example.com",
        },
    }


def get_fake_comments(comment_count, **kwargs):
    """Creates a random fake list of comments."""

    return [get_fake_comment(**kwargs) for _ in range(comment_count)]


def get_fake_comments_in_change(comment_count, path=None, **kwargs):
    """Creates a random fake list of comments in change."""

    return {
        path or "gerrit-server/fake/path/to/file": get_fake_comments(
            comment_count, **kwargs
        )
    }
