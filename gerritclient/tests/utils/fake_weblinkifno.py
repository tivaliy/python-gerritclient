def get_fake_weblinkinfo(name="gitweb", project_id="fake-project"):
    """Creates a fake WebLinkInfo entity

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review WebLinkInfo entity.
    """
    return [
        {
            "name": name,
            "url": f"gitweb?p\u003d{project_id}.git;a\u003dsummary",
            "image_url": None,
        }
    ]
