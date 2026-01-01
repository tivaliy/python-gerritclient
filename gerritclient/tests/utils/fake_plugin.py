def get_fake_plugin(plugin_id="fake-plugin"):
    """Creates a fake plugin

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    return {
        "id": plugin_id,
        "version": "1.0",
        "index_url": f"plugins/{plugin_id}/",
        "disabled": None,
    }


def get_fake_plugins(plugins_count):
    """Creates a random fake plugins map."""

    fake_plugins = {}
    for i in range(1, plugins_count + 1):
        fake_plugins[f"fake-plugin-{i}"] = get_fake_plugin(f"fake-plugin-{i}")
    return fake_plugins
