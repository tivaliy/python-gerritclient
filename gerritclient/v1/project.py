from requests import utils as requests_utils

from gerritclient.v1 import base


class ProjectClient(base.BaseV1ClientCreateEntity):
    api_path = "/projects/"

    def get_all(
        self,
        is_all=False,
        limit=None,
        skip=None,
        pattern_dispatcher=None,
        project_type=None,
        description=False,
        branches=None,
    ):
        """Get list of all available projects accessible by the caller.

        :param is_all: boolean value, if True then all projects (including
                       hidden ones) will be added to the results
        :param limit: Int value that allows to limit the number of projects
                      to be included in the output results
        :param skip: Int value that allows to skip the given
                     number of projects from the beginning of the list
        :param pattern_dispatcher: Dict of pattern type with respective
                     pattern value: {('prefix'|'match'|'regex') : value}
        :param project_type: string value for type of projects to be fetched
                            ('code'|'permissions'|'all')
        :param description: boolean value, if True then description will be
                            added to the output result
        :param branches: List of names of branches as a string to limit the
                         results to the projects having the specified branches
                         and include the sha1 of the branches in the results
        :return: A map (dict) that maps entity names to respective entries
        """

        pattern_types = {"prefix": "p", "match": "m", "regex": "r"}

        p, v = None, None
        if pattern_dispatcher is not None and pattern_dispatcher:
            for item in pattern_types:
                if item in pattern_dispatcher:
                    p, v = pattern_types[item], pattern_dispatcher[item]
                    break
            else:
                raise ValueError(
                    "Pattern types can be either 'prefix', 'match' or 'regex'."
                )

        params = {
            k: v
            for k, v in (
                ("n", limit),
                ("S", skip),
                (p, v),
                ("type", project_type),
                ("b", branches),
            )
            if v is not None
        }
        params["all"] = int(is_all)
        params["d"] = int(description)
        return self.connection.get_request(self.api_path, params=params)

    def get_by_name(self, name):
        """Get detailed info about specified project."""

        request_path = "{api_path}{name}".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path)

    def delete(self, name, force=False, preserve=False):
        """Delete specified project."""

        data = {"force": force, "preserve": preserve}
        request_path = "{api_path}{name}".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.delete_request(request_path, data)

    def get_description(self, name):
        """Retrieves the description of a project."""

        request_path = "{api_path}{name}/description".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path)

    def set_description(self, name, description=None, commit_message=None):
        data = {"description": description, "commit_message": commit_message}
        request_path = "{api_path}{name}/description".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.put_request(request_path, json_data=data)

    def get_parent(self, name):
        request_path = "{api_path}{name}/parent".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path)

    def set_parent(self, name, parent, commit_message=None):
        data = {"parent": parent, "commit_message": commit_message}
        request_path = "{api_path}{name}/parent".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.put_request(request_path, json_data=data)

    def get_head(self, name):
        request_path = "{api_path}{name}/HEAD".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path)

    def set_head(self, name, branch):
        data = {"ref": branch}
        request_path = "{api_path}{name}/HEAD".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.put_request(request_path, json_data=data)

    def get_repo_statistics(self, name):
        request_path = "{api_path}{name}/statistics.git".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path)

    def get_branches(self, name):
        request_path = "{api_path}{name}/branches".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path)

    def get_branch(self, name, branch_name):
        request_path = "{api_path}{name}/branches/{branch_name}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            branch_name=requests_utils.quote(branch_name, safe=""),
        )
        return self.connection.get_request(request_path)

    def create_branch(self, name, branch_name, revision=None):
        """Create a new branch.

        :param name: Name of the project
        :param branch_name: Name of the branch
        :param revision: The base revision of the new branch. If not set,
                         HEAD will be used as base revision.
        :return: A BranchInfo entity that describes the created branch.
        """

        data = {"revision": revision}
        request_path = "{api_path}{name}/branches/{branch_name}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            branch_name=requests_utils.quote(branch_name, safe=""),
        )
        return self.connection.put_request(request_path, json_data=data)

    def delete_branch(self, name, branches):
        """Delete one or more branches.

        :param name: Name of the project
        :param branches: A list of branch names that identify the branches
                         that should be deleted.
        """

        data = {"branches": branches}
        request_path = "{api_path}{name}/branches:delete".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def get_children(self, name, recursively=False):
        """List the direct child projects of a project."""

        request_path = "{api_path}{name}/children/{recursively}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            recursively="?recursive" if recursively else "",
        )
        return self.connection.get_request(request_path)

    def get_reflog(self, name, branch):
        """Get the reflog of a certain branch."""

        request_path = "{api_path}{name}/branches/{branch}/reflog".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            branch=requests_utils.quote(branch, safe=""),
        )
        return self.connection.get_request(request_path)

    def run_gc(self, name, aggressive=False, show_progress=False):
        """Run the Git garbage collection for the repository of a project."""

        data = {"aggressive": aggressive, "show_progress": show_progress}
        request_path = "{api_path}{name}/gc".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def get_tags(self, name, limit=None, skip=None, pattern_dispatcher=None):
        """Get the tags for a project.

        :param name: Name of the project.
        :param limit: Int value that allows to limit the number of tags
                      to be included in the output results.
        :param skip: Int value that allows to skip the given number of tags
                     from the beginning of the list
        :param pattern_dispatcher: Pattern type (as a dict) with respective
                                   pattern value: {('match'|'regex') : value}
        """

        pattern_types = {"match": "m", "regex": "r"}

        p, v = None, None
        if pattern_dispatcher is not None and pattern_dispatcher:
            for item in pattern_types:
                if item in pattern_dispatcher:
                    p, v = pattern_types[item], pattern_dispatcher[item]
                    break
            else:
                raise ValueError("Pattern types can be either 'match' or 'regex'.")

        params = {k: v for k, v in (("n", limit), ("s", skip), (p, v)) if v is not None}

        request_path = "{api_path}{name}/tags".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path, params=params)

    def get_tag(self, name, tag_id):
        """Retrieve a tag of a project."""

        request_path = "{api_path}{name}/tags/{tag_id}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            tag_id=requests_utils.quote(tag_id, safe=""),
        )
        return self.connection.get_request(request_path)

    def create_tag(self, name, tag_id, revision=None, message=None):
        """Create a new tag on the project."""

        data = {"revision": revision, "message": message}
        request_path = "{api_path}{name}/tags/{tag_id}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            tag_id=tag_id,
        )
        return self.connection.put_request(request_path, json_data=data)

    def delete_tag(self, name, tags):
        """Delete one or more tags.

        :param name: Name of the project.
        :param tags: A list of tags to be deleted.
        """

        data = {"tags": tags}
        request_path = "{api_path}{name}/tags:delete".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def get_config(self, name):
        """Get some configuration information about a project."""

        request_path = "{api_path}{name}/config".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.get_request(request_path)

    def set_config(self, name, data):
        """Set the configuration of a project."""

        request_path = "{api_path}{name}/config".format(
            api_path=self.api_path, name=requests_utils.quote(name, safe="")
        )
        return self.connection.put_request(request_path, json_data=data)

    def get_commit(self, name, commit):
        """Retrieves a commit of a project."""

        request_path = "{api_path}{name}/commits/{commit}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            commit=commit,
        )
        return self.connection.get_request(request_path)

    def get_commit_affiliation(self, name, commit):
        """Retrieve the branches and tags in which a change is included."""

        request_path = "{api_path}{name}/commits/{commit}/in".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=""),
            commit=commit,
        )
        return self.connection.get_request(request_path)

    def get_file_content(self, name, commit, file_id):
        request_path = (
            "{api_path}{name}/commits/{commit}/files/{file_id}/content".format(
                api_path=self.api_path,
                name=requests_utils.quote(name, safe=""),
                commit=commit,
                file_id=requests_utils.quote(file_id, safe=""),
            )
        )
        return self.connection.get_request(request_path)


def get_client(connection):
    return ProjectClient(connection)
