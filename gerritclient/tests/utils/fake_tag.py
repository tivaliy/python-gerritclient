def get_fake_tag():
    """Creates a fake TagInfo."""

    return {
        "ref": "refs/tags/v1.0",
        "revision": "49ce77fdcfd3398dc0dedbe016d1a425fd52d666",
        "object": "1624f5af8ae89148d1a3730df8c290413e3dcf30",
        "message": "Annotated tag",
        "tagger": {
            "name": "John Doe",
            "email": "j.doe@example.com",
            "date": "2014-10-06 07:35:03.000000000",
            "tz": 540,
        },
    }


def get_fake_tags(tags_count):
    """Creates a random fake tag list of a project."""

    return [get_fake_tag() for _ in range(tags_count)]
