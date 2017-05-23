#
#    Copyright 2017 Vitalii Kulanov
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


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
        "valid": valid
    }


def get_fake_ssh_keys_info(keys_count):
    """Create a random fake list of SSH keys info."""

    return [get_fake_ssh_key_info(seq=i, valid=True)
            for i in range(1, keys_count + 1)]
