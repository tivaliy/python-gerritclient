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


def get_fake_account(_account_id=1000226, name="John Doe",
                     email="john.doe@example.com", username="john"):
    """Creates a fake account

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    return {
        "_account_id": _account_id,
        "name": name,
        "email": email,
        "username": username,
        "secondary_emails": ['fake-email@example.com']
    }


def get_fake_accounts(account_count):
    """Create a random fake list of accounts."""

    return [get_fake_account(_account_id=i, username='john-{}'.format(i))
            for i in range(1, account_count+1)]
