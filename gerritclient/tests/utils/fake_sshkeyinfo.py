def get_fake_ssh_key_info(seq, valid=True):
    """Creates a fake SSH key info

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    return {
        "seq": seq,
        "ssh_public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0T..."
        "YImydZAw\u003d\u003d john.doe@example.com",
        "encoded_key": "AAAAB3NzaC1yc2EAAAABIwAAAQEA0T...YImydZAw\u003d\u003d",
        "algorithm": "ssh-rsa",
        "comment": "john.doe@example.com",
        "valid": valid,
    }


def get_fake_ssh_keys_info(keys_count):
    """Create a random fake list of SSH keys info."""

    return [get_fake_ssh_key_info(seq=i, valid=True) for i in range(1, keys_count + 1)]
