from requests import utils as requests_utils

from gerritclient.v1 import base


class ChangeClient(base.BaseV1Client):
    api_path = "/changes/"

    def get_all(self, query, options=None, limit=None, skip=None):
        """Query changes.

        :param query: Queries as a list of string
        :param options: List of options to fetch additional data about changes
        :param limit: Int value that allows to limit the number of changes
                      to be included in the output results
        :param skip: Int value that allows to skip the given number of
                     changes from the beginning of the list
        :return A list of ChangeInfo entries
        """

        params = {
            k: v
            for k, v in (("o", options), ("n", limit), ("S", skip))
            if v is not None
        }
        request_path = "{api_path}{query}".format(
            api_path=self.api_path, query="?q={query}".format(query="&q=".join(query))
        )
        return self.connection.get_request(request_path, params=params)

    def get_by_id(self, change_id, detailed=False, options=None):
        """Retrieve a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param detailed: boolean value, if True then retrieve a change with
                         labels, detailed labels, detailed accounts,
                         reviewer updates, and messages.
        :param options: List of options to fetch additional data about a change
        :return: ChangeInfo entity is returned that describes the change.
        """

        params = {"o": options}
        request_path = "{api_path}{change_id}/{detail}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            detail="detail" if detailed else "",
        )
        return self.connection.get_request(request_path, params=params)

    def create(self, data):
        """Create a new change."""

        return self.connection.post_request(self.api_path, json_data=data)

    def delete(self, change_id):
        """Delete a change."""

        request_path = "{api_path}{change_id}".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.delete_request(request_path, data={})

    def abandon(self, change_id):
        """Abandon a change."""

        request_path = "{api_path}{change_id}/abandon".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data={})

    def restore(self, change_id):
        """Restore a change."""

        request_path = "{api_path}{change_id}/restore".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data={})

    def revert(self, change_id, message=None):
        """Revert a change."""

        data = {k: v for k, v in (("message", message),) if v is not None}
        request_path = "{api_path}{change_id}/revert".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def rebase(self, change_id, parent=None):
        """Rebase a change."""

        data = {k: v for k, v in (("base", parent),) if v is not None}
        request_path = "{api_path}{change_id}/rebase".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def move(self, change_id, branch, message=None):
        """Move a change."""

        data = {
            k: v
            for k, v in (("destination_branch", branch), ("message", message))
            if v is not None
        }
        request_path = "{api_path}{change_id}/move".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def submit(self, change_id, on_behalf_of=None, notify=None):
        """Submit a change."""

        # TODO(vkulanov): add 'notify_details' field (parameter) support
        data = {
            k: v
            for k, v in (("on_behalf_of", on_behalf_of), ("notify", notify))
            if v is not None
        }
        request_path = "{api_path}{change_id}/submit".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def get_topic(self, change_id):
        """Retrieve the topic of a change."""

        request_path = "{api_path}{change_id}/topic".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def set_topic(self, change_id, topic):
        """Set the topic of a change."""

        data = {"topic": topic}
        request_path = "{api_path}{change_id}/topic".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.put_request(request_path, json_data=data)

    def delete_topic(self, change_id):
        """Delete the topic of a change."""

        request_path = "{api_path}{change_id}/topic".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.delete_request(request_path, data={})

    def get_assignee(self, change_id):
        """Retrieve the account of the user assigned to a change."""

        request_path = "{api_path}{change_id}/assignee".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def get_assignees(self, change_id):
        """Retrieve a list of every user ever assigned to a change."""

        request_path = "{api_path}{change_id}/past_assignees".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def set_assignee(self, change_id, account_id):
        """Set the assignee of a change."""

        data = {"assignee": account_id}
        request_path = "{api_path}{change_id}/assignee".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.put_request(request_path, json_data=data)

    def delete_assignee(self, change_id):
        """Delete the assignee of a change."""

        request_path = "{api_path}{change_id}/assignee".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.delete_request(request_path, data={})

    def publish_draft(self, change_id):
        """Publish a draft change."""

        request_path = "{api_path}{change_id}/publish".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data={})

    def get_included(self, change_id):
        """Retrieve the branches and tags in which a change is included."""

        request_path = "{api_path}{change_id}/in".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def index(self, change_id):
        """Add or update the change in the secondary index."""

        request_path = "{api_path}{change_id}/index".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data={})

    def get_comments(self, change_id, comment_type=None):
        """List the published comments of all revisions of the change.

        :param change_id: Identifier that uniquely identifies one change.
        :param comment_type: Type of comments (None|'drafts'|'robotcomments')
                             None - published comments,
                             'drafts' - draft comments,
                             'robotcomments' - robotcomments.
        :return A list of CommentInfo entries.
        """

        request_path = "{api_path}{change_id}/{comment_type}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            comment_type=comment_type if comment_type else "comments",
        )
        return self.connection.get_request(request_path)

    def check_consistency(self, change_id):
        """Perform consistency checks on the change."""

        request_path = "{api_path}{change_id}/check".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def fix_consistency(self, change_id, is_delete=False, expect_merged_as=False):
        """Perform consistency checks on the change and fixes any problems.

        :param change_id: Identifier that uniquely identifies one change.
        :param is_delete: If True, delete patch sets from the database
                          if they refer to missing commit options.
        :param expect_merged_as: If True, check that the change is merged into
                                 the destination branch as this exact SHA-1.
                                 If not, insert a new patch set referring to
                                 this commit.
        :return Returns a ChangeInfo entity with the problems field values
                that reflect any fixes.
        """

        data = {
            "delete_patch_set_if_commit_missing": is_delete,
            "expect_merged_as": expect_merged_as,
        }
        request_path = "{api_path}{change_id}/check".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    # Reviewer endpoints

    def get_reviewers(self, change_id):
        """List the reviewers of a change.

        :param change_id: Identifier that uniquely identifies one change.
        :return: A list of ReviewerInfo entries.
        """

        request_path = "{api_path}{change_id}/reviewers".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def get_reviewer(self, change_id, account_id):
        """Retrieve a reviewer of a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param account_id: Identifier that uniquely identifies one account.
        :return: A ReviewerInfo entity.
        """

        request_path = "{api_path}{change_id}/reviewers/{account_id}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            account_id=requests_utils.quote(str(account_id), safe=""),
        )
        return self.connection.get_request(request_path)

    def add_reviewer(self, change_id, reviewer, state=None, confirmed=None, notify=None):
        """Add a reviewer to the change.

        :param change_id: Identifier that uniquely identifies one change.
        :param reviewer: The ID of one account that should be added as reviewer
                         or the ID of one group for which all members should
                         be added as reviewers.
        :param state: Add reviewer in given state ('REVIEWER' or 'CC').
                      Defaults to 'REVIEWER'.
        :param confirmed: If True, reviewer addition is confirmed even if there
                          are warnings.
        :param notify: Notify handling ('NONE', 'OWNER', 'OWNER_REVIEWERS', 'ALL').
        :return: An AddReviewerResult entity.
        """

        data = {
            k: v
            for k, v in (
                ("reviewer", reviewer),
                ("state", state),
                ("confirmed", confirmed),
                ("notify", notify),
            )
            if v is not None
        }
        request_path = "{api_path}{change_id}/reviewers".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def delete_reviewer(self, change_id, account_id, notify=None):
        """Remove a reviewer from a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param account_id: Identifier that uniquely identifies one account.
        :param notify: Notify handling ('NONE', 'OWNER', 'OWNER_REVIEWERS', 'ALL').
        :return: Empty response.
        """

        data = {k: v for k, v in (("notify", notify),) if v is not None}
        request_path = "{api_path}{change_id}/reviewers/{account_id}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            account_id=requests_utils.quote(str(account_id), safe=""),
        )
        return self.connection.delete_request(request_path, data=data)

    def suggest_reviewers(self, change_id, query, limit=None, exclude_groups=None):
        """Suggest reviewers for a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param query: Query string to match potential reviewers.
        :param limit: Maximum number of suggested reviewers to return.
        :param exclude_groups: If True, exclude groups from suggestions.
        :return: A list of SuggestedReviewerInfo entries.
        """

        params = {
            k: v
            for k, v in (
                ("q", query),
                ("n", limit),
                ("exclude-groups", exclude_groups),
            )
            if v is not None
        }
        request_path = "{api_path}{change_id}/suggest_reviewers".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path, params=params)

    # Review (voting) endpoint

    def set_review(
        self,
        change_id,
        revision_id="current",
        message=None,
        labels=None,
        comments=None,
        tag=None,
        notify=None,
        on_behalf_of=None,
        ready=None,
        work_in_progress=None,
    ):
        """Set a review on a revision.

        :param change_id: Identifier that uniquely identifies one change.
        :param revision_id: Identifier that uniquely identifies one revision
                            (patchset). Defaults to 'current'.
        :param message: Review message to post.
        :param labels: Dict of label names to voting values
                       (e.g., {'Code-Review': 1, 'Verified': -1}).
        :param comments: Dict of file paths to lists of CommentInput entities.
        :param tag: Tag for the review (e.g., 'autogenerated:ci').
        :param notify: Notify handling ('NONE', 'OWNER', 'OWNER_REVIEWERS', 'ALL').
        :param on_behalf_of: Account ID to post review on behalf of.
        :param ready: If True, mark the change as ready for review.
        :param work_in_progress: If True, mark the change as work in progress.
        :return: A ReviewResult entity.
        """

        data = {
            k: v
            for k, v in (
                ("message", message),
                ("labels", labels),
                ("comments", comments),
                ("tag", tag),
                ("notify", notify),
                ("on_behalf_of", on_behalf_of),
                ("ready", ready),
                ("work_in_progress", work_in_progress),
            )
            if v is not None
        }
        request_path = "{api_path}{change_id}/revisions/{revision_id}/review".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            revision_id=requests_utils.quote(str(revision_id), safe=""),
        )
        return self.connection.post_request(request_path, json_data=data)

    # Attention Set endpoints

    def get_attention_set(self, change_id):
        """Get the attention set of a change.

        :param change_id: Identifier that uniquely identifies one change.
        :return: A list of AttentionSetInfo entries.
        """

        request_path = "{api_path}{change_id}/attention".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def add_to_attention_set(self, change_id, account_id, reason=None, notify=None):
        """Add a user to the attention set of a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param account_id: Identifier that uniquely identifies one account.
        :param reason: Reason for adding the user to the attention set.
        :param notify: Notify handling ('NONE', 'OWNER', 'OWNER_REVIEWERS', 'ALL').
        :return: An AttentionSetInfo entity.
        """

        data = {
            k: v
            for k, v in (
                ("user", account_id),
                ("reason", reason),
                ("notify", notify),
            )
            if v is not None
        }
        request_path = "{api_path}{change_id}/attention".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def remove_from_attention_set(self, change_id, account_id, reason=None, notify=None):
        """Remove a user from the attention set of a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param account_id: Identifier that uniquely identifies one account.
        :param reason: Reason for removing the user from the attention set.
        :param notify: Notify handling ('NONE', 'OWNER', 'OWNER_REVIEWERS', 'ALL').
        :return: Empty response.
        """

        data = {
            k: v
            for k, v in (("reason", reason), ("notify", notify))
            if v is not None
        }
        request_path = "{api_path}{change_id}/attention/{account_id}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            account_id=requests_utils.quote(str(account_id), safe=""),
        )
        return self.connection.delete_request(request_path, data=data)

    # Work-in-Progress / Ready-for-Review endpoints

    def set_work_in_progress(self, change_id, message=None):
        """Mark a change as work in progress.

        :param change_id: Identifier that uniquely identifies one change.
        :param message: Message to be added as review comment.
        :return: Empty response on success.
        """

        data = {k: v for k, v in (("message", message),) if v is not None}
        request_path = "{api_path}{change_id}/wip".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    def set_ready_for_review(self, change_id, message=None):
        """Mark a change as ready for review.

        :param change_id: Identifier that uniquely identifies one change.
        :param message: Message to be added as review comment.
        :return: Empty response on success.
        """

        data = {k: v for k, v in (("message", message),) if v is not None}
        request_path = "{api_path}{change_id}/ready".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    # Hashtags endpoints

    def get_hashtags(self, change_id):
        """Get the hashtags associated with a change.

        :param change_id: Identifier that uniquely identifies one change.
        :return: A list of hashtag strings.
        """

        request_path = "{api_path}{change_id}/hashtags".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def set_hashtags(self, change_id, add=None, remove=None):
        """Add and/or remove hashtags from a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param add: List of hashtags to add.
        :param remove: List of hashtags to remove.
        :return: A list of the hashtags after the operation.
        """

        data = {
            k: v for k, v in (("add", add), ("remove", remove)) if v is not None
        }
        request_path = "{api_path}{change_id}/hashtags".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.post_request(request_path, json_data=data)

    # Change Messages endpoints

    def get_messages(self, change_id):
        """List all the messages of a change.

        :param change_id: Identifier that uniquely identifies one change.
        :return: A list of ChangeMessageInfo entries.
        """

        request_path = "{api_path}{change_id}/messages".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path)

    def get_message(self, change_id, message_id):
        """Retrieve a change message.

        :param change_id: Identifier that uniquely identifies one change.
        :param message_id: The ID of a change message.
        :return: A ChangeMessageInfo entity.
        """

        request_path = "{api_path}{change_id}/messages/{message_id}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            message_id=requests_utils.quote(str(message_id), safe=""),
        )
        return self.connection.get_request(request_path)

    def delete_message(self, change_id, message_id, reason=None):
        """Delete a change message.

        :param change_id: Identifier that uniquely identifies one change.
        :param message_id: The ID of a change message.
        :param reason: Reason for deletion.
        :return: A ChangeMessageInfo entity (with message replaced).
        """

        data = {k: v for k, v in (("message", reason),) if v is not None}
        request_path = "{api_path}{change_id}/messages/{message_id}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=""),
            message_id=requests_utils.quote(str(message_id), safe=""),
        )
        return self.connection.delete_request(request_path, data=data)

    # Submitted Together endpoint

    def get_submitted_together(self, change_id, options=None):
        """Get the list of changes that would be submitted together.

        :param change_id: Identifier that uniquely identifies one change.
        :param options: List of additional options (e.g., 'NON_VISIBLE_CHANGES').
        :return: A SubmittedTogetherInfo entity.
        """

        params = {"o": options} if options else None
        request_path = "{api_path}{change_id}/submitted_together".format(
            api_path=self.api_path, change_id=requests_utils.quote(change_id, safe="")
        )
        return self.connection.get_request(request_path, params=params)


def get_client(connection):
    return ChangeClient(connection)
