import abc
import argparse

from gerritclient import error
from gerritclient.commands import base
from gerritclient.common import utils


class ChangeMixIn:
    entity_name = "change"

    columns = (
        "id",
        "project",
        "branch",
        "topic",
        "hashtags",
        "change_id",
        "subject",
        "status",
        "created",
        "updated",
        "submitted",
        "starred",
        "stars",
        "reviewed",
        "submit_type",
        "mergeable",
        "submittable",
        "insertions",
        "deletions",
        "unresolved_comment_count",
        "_number",
        "owner",
        "actions",
        "labels",
        "permitted_labels",
        "removable_reviewers",
        "reviewers",
        "reviewer_updates",
        "messages",
        "current_revision",
        "revisions",
        "_more_changes",
        "problems",
    )


class ChangeCommentMixIn:
    entity_name = "change"

    columns = (
        "patch_set",
        "id",
        "path",
        "side",
        "parent",
        "line",
        "range",
        "in_reply_to",
        "message",
        "updated",
        "author",
        "tag",
        "unresolved",
        "robot_id",
        "robot_run_id",
        "url",
        "properties",
        "fix_suggestions",
    )

    @staticmethod
    def format_data(data):
        fetched_data = []
        for file_path, comment_info in data.items():
            for item in comment_info:
                item["path"] = file_path
                fetched_data.append(item)
        return fetched_data


class ChangeList(ChangeMixIn, base.BaseListCommand):
    """Queries changes visible to the caller."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument("query", nargs="+", help="Query string.")
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            help="Limit the number of changes to be included in the results.",
        )
        parser.add_argument(
            "-S",
            "--skip",
            type=int,
            help="Skip the given number of changes from the beginning of the list.",
        )
        parser.add_argument(
            "-o", "--option", nargs="+", help="Fetch additional data about changes."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_all(
            query=parsed_args.query,
            options=parsed_args.option,
            limit=parsed_args.limit,
            skip=parsed_args.skip,
        )
        # Clients are allowed to specify more than one query. In this case
        # the result is an array of arrays, one per query in the same order
        # the queries were given in. If the number of queries more then one,
        # then merge arrays in a single one to display data correctly.
        if len(parsed_args.query) > 1:
            response = [item for sublist in response for item in sublist]
        fetched_columns = [c for c in self.columns if response and c in response[0]]
        data = utils.get_display_data_multi(fetched_columns, response)
        return fetched_columns, data


class ChangeShow(ChangeMixIn, base.BaseShowCommand):
    """Retrieves a change."""

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Retrieves a change with labels, detailed labels, "
            "detailed accounts, reviewer updates, and messages.",
        )
        parser.add_argument(
            "-o", "--option", nargs="+", help="Fetch additional data about a change."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_by_id(
            change_id=parsed_args.entity_id,
            detailed=parsed_args.all,
            options=parsed_args.option,
        )
        # As the number of columns can greatly very depending on request
        # let's fetch only those that are in response and print them in
        # respective (declarative) order
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeCreate(ChangeMixIn, base.BaseCommand, base.show.ShowOne):
    """Creates a new change."""

    columns = (
        "id",
        "project",
        "branch",
        "topic",
        "change_id",
        "subject",
        "status",
        "created",
        "updated",
        "mergeable",
        "insertions",
        "deletions",
        "_number",
        "owner",
    )

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist")
        return file_path

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "file", type=self.get_file_path, help="File with metadata of a new change."
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        try:
            data = utils.read_from_file(file_path)
        except OSError:
            msg = f"Could not read metadata at {file_path}"
            raise error.InvalidFileException(msg)

        response = self.client.create(data)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class BaseChangeAction(ChangeMixIn, base.BaseShowCommand, abc.ABC):
    """Base class to perform actions on changes."""

    @property
    def parameters(self):
        """Additional parameters to be passed to 'action' method as a tuple."""

        return ()

    @abc.abstractmethod
    def action(self, change_id, **kwargs):
        pass

    def take_action(self, parsed_args):
        # Retrieve necessary parameters from argparse.Namespace object
        params = {k: v for k, v in vars(parsed_args).items() if k in self.parameters}
        response = self.action(parsed_args.entity_id, **params)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeAbandon(BaseChangeAction):
    """Abandons a change."""

    def action(self, change_id, **kwargs):
        return self.client.abandon(change_id)


class ChangeRestore(BaseChangeAction):
    """Restores a change."""

    def action(self, change_id, **kwargs):
        return self.client.restore(change_id)


class ChangeRevert(BaseChangeAction):
    """Reverts a change."""

    parameters = ("message",)

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-m",
            "--message",
            help="Message to be added as review comment when reverting the change.",
        )
        return parser

    def action(self, change_id, message=None):
        return self.client.revert(change_id, message=message)


class ChangeMove(BaseChangeAction):
    """Moves a change."""

    parameters = ("branch", "message")

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument("-b", "--branch", required=True, help="Destination branch.")
        parser.add_argument(
            "-m", "--message", help="A message to be posted in this change's comments."
        )
        return parser

    def action(self, change_id, branch=None, message=None):
        return self.client.move(change_id, branch, message=message)


class ChangeSubmit(BaseChangeAction):
    """Submits a change."""

    parameters = ("on_behalf_of", "notify")

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "--on-behalf-of", help="Submit the change on behalf of the given user."
        )
        parser.add_argument(
            "--notify",
            choices=["NONE", "OWNER", "OWNER_REVIEWERS", "ALL"],
            default="ALL",
            help="Notify handling that defines to whom email notifications "
            "should be sent after the change is submitted.",
        )
        return parser

    def action(self, change_id, on_behalf_of=None, notify=None):
        return self.client.submit(change_id, on_behalf_of=on_behalf_of, notify=notify)


class ChangeRebase(BaseChangeAction):
    """Rebases a change."""

    parameters = ("parent",)

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument("-p", "--parent", help="The new parent revision.")
        return parser

    def action(self, change_id, parent=None):
        return self.client.rebase(change_id, parent=parent)


class ChangeDelete(ChangeMixIn, base.BaseCommand):
    """Deletes a change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete(parsed_args.change_id)
        self.app.stdout.write(
            f"Change with ID {parsed_args.change_id} was successfully deleted.\n"
        )


class ChangeTopicShow(ChangeMixIn, base.BaseShowCommand):
    """Retrieves the topic of a change."""

    columns = ("topic",)

    def take_action(self, parsed_args):
        response = self.client.get_topic(parsed_args.entity_id) or None
        data = utils.get_display_data_single(self.columns, {"topic": response})
        return self.columns, data


class ChangeTopicSet(ChangeMixIn, base.BaseShowCommand):
    """Sets the topic of a change."""

    columns = ("topic",)

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument("-t", "--topic", required=True, help="Topic of a change.")
        return parser

    def take_action(self, parsed_args):
        response = (
            self.client.set_topic(parsed_args.entity_id, parsed_args.topic) or None
        )
        data = utils.get_display_data_single(self.columns, {"topic": response})
        return self.columns, data


class ChangeTopicDelete(ChangeMixIn, base.BaseShowCommand):
    """Deletes the topic of a change."""

    columns = ("topic",)

    def take_action(self, parsed_args):
        response = self.client.delete_topic(parsed_args.entity_id) or None
        data = utils.get_display_data_single(self.columns, {"topic": response})
        return self.columns, data


class ChangeAssigneeShow(BaseChangeAction):
    """Retrieves the account of the user assigned to a change."""

    columns = ("_account_id", "name", "email", "username")

    def action(self, change_id, **kwargs):
        return self.client.get_assignee(change_id)


class ChangeAssigneeHistoryShow(ChangeMixIn, base.BaseListCommand):
    """Retrieve a list of every user ever assigned to a change."""

    columns = ("_account_id", "name", "email", "username")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_assignees(parsed_args.change_id)
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class ChangeAssigneeSet(ChangeMixIn, base.BaseShowCommand):
    """Sets the assignee of a change."""

    columns = ("_account_id", "name", "email", "username")

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-a",
            "--account",
            required=True,
            help="The ID of one account that should be added as assignee.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_assignee(parsed_args.entity_id, parsed_args.account)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ChangeAssigneeDelete(BaseChangeAction):
    """Deletes the assignee of a change."""

    columns = ("_account_id", "name", "email", "username")

    def action(self, change_id, **kwargs):
        return self.client.delete_assignee(change_id)


class ChangeDraftPublish(ChangeMixIn, base.BaseCommand):
    """Publishes a draft change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.publish_draft(parsed_args.change_id)
        self.app.stdout.write(
            f"Draft change with ID {parsed_args.change_id} was successfully published.\n"
        )


class ChangeIncludedInSHow(BaseChangeAction):
    """Retrieves the branches and tags in which a change is included."""

    columns = ("branches", "tags", "external")

    def action(self, change_id, **kwargs):
        return self.client.get_included(change_id)


class ChangeIndex(ChangeMixIn, base.BaseCommand):
    """Adds or updates the change in the secondary index."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.index(parsed_args.change_id)
        msg = (
            f"Change with ID {parsed_args.change_id} was successfully added/updated in the "
            "secondary index.\n"
        )
        self.app.stdout.write(msg)


class ChangeCommentList(ChangeCommentMixIn, base.BaseListCommand):
    """Lists the published comments of all revisions of the change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-t",
            "--type",
            choices=["drafts", "robotcomments"],
            default=None,
            help="The type of comments. Defaults to published.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_comments(
            parsed_args.change_id, comment_type=parsed_args.type
        )
        data = self.format_data(response)
        fetched_columns = [c for c in self.columns if data and c in data[0]]
        data = utils.get_display_data_multi(fetched_columns, data)
        return fetched_columns, data


class ChangeCheck(ChangeMixIn, base.BaseShowCommand):
    """Performs consistency checks on the change.

    Returns a ChangeInfo entity with the problems field.
    """

    def take_action(self, parsed_args):
        response = self.client.check_consistency(parsed_args.entity_id)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeFix(ChangeMixIn, base.BaseShowCommand):
    """Performs consistency checks on the change.

    Additionally fixes any problems that can be fixed automatically. The
    returned field values reflect any fixes. Only the change owner,
    a project owner, or an administrator may fix changes.
    """

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "--delete-patchset",
            action="store_true",
            help="Delete patch sets from the database "
            "if they refer to missing commit options.",
        )
        parser.add_argument(
            "--expect-merged-as",
            action="store_true",
            help="Check that the change is merged into the destination branch "
            "as this exact SHA-1. If not, insert a new patch set "
            "referring to this commit.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.fix_consistency(
            parsed_args.entity_id,
            is_delete=parsed_args.delete_patchset,
            expect_merged_as=parsed_args.expect_merged_as,
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


# Reviewer commands


class ChangeReviewerMixIn:
    entity_name = "change"

    columns = (
        "_account_id",
        "name",
        "email",
        "username",
        "approvals",
    )


class ChangeReviewerList(ChangeReviewerMixIn, base.BaseListCommand):
    """Lists the reviewers of a change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_reviewers(parsed_args.change_id)
        fetched_columns = [c for c in self.columns if response and c in response[0]]
        data = utils.get_display_data_multi(fetched_columns, response)
        return fetched_columns, data


class ChangeReviewerShow(ChangeReviewerMixIn, base.BaseShowCommand):
    """Retrieves a reviewer of a change."""

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-a",
            "--account",
            required=True,
            help="The account identifier of the reviewer.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_reviewer(
            parsed_args.entity_id, parsed_args.account
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeReviewerAdd(ChangeReviewerMixIn, base.BaseCommand, base.show.ShowOne):
    """Adds a reviewer to a change."""

    columns = (
        "input",
        "reviewers",
        "ccs",
        "error",
        "confirm",
    )

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-r",
            "--reviewer",
            required=True,
            help="The ID of one account or group to add as reviewer.",
        )
        parser.add_argument(
            "-s",
            "--state",
            choices=["REVIEWER", "CC"],
            default="REVIEWER",
            help="The state in which to add the reviewer (default: REVIEWER).",
        )
        parser.add_argument(
            "--confirmed",
            action="store_true",
            help="Confirm adding the reviewer even if there are warnings.",
        )
        parser.add_argument(
            "--notify",
            choices=["NONE", "OWNER", "OWNER_REVIEWERS", "ALL"],
            help="Notify handling for adding the reviewer.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.add_reviewer(
            parsed_args.change_id,
            reviewer=parsed_args.reviewer,
            state=parsed_args.state,
            confirmed=parsed_args.confirmed if parsed_args.confirmed else None,
            notify=parsed_args.notify,
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeReviewerDelete(ChangeMixIn, base.BaseCommand):
    """Removes a reviewer from a change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-a",
            "--account",
            required=True,
            help="The account identifier of the reviewer to remove.",
        )
        parser.add_argument(
            "--notify",
            choices=["NONE", "OWNER", "OWNER_REVIEWERS", "ALL"],
            help="Notify handling for removing the reviewer.",
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete_reviewer(
            parsed_args.change_id,
            account_id=parsed_args.account,
            notify=parsed_args.notify,
        )
        self.app.stdout.write(
            f"Reviewer '{parsed_args.account}' was removed from change "
            f"'{parsed_args.change_id}'.\n"
        )


class ChangeReviewerSuggest(ChangeReviewerMixIn, base.BaseListCommand):
    """Suggests reviewers for a change."""

    columns = ("account", "group", "count")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-q", "--query", required=True, help="Query string to match reviewers."
        )
        parser.add_argument(
            "-l", "--limit", type=int, help="Maximum number of suggestions to return."
        )
        parser.add_argument(
            "--exclude-groups",
            action="store_true",
            help="Exclude groups from suggestions.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.suggest_reviewers(
            parsed_args.change_id,
            query=parsed_args.query,
            limit=parsed_args.limit,
            exclude_groups=parsed_args.exclude_groups if parsed_args.exclude_groups else None,
        )
        fetched_columns = [c for c in self.columns if response and c in response[0]]
        data = utils.get_display_data_multi(fetched_columns, response)
        return fetched_columns, data


# Review (voting) command


class ChangeReview(ChangeMixIn, base.BaseCommand, base.show.ShowOne):
    """Sets a review on a change (post votes and comments)."""

    columns = ("labels", "reviewers", "ready")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-r",
            "--revision",
            default="current",
            help="Revision (patchset) identifier. Defaults to 'current'.",
        )
        parser.add_argument(
            "-m", "--message", help="Review message to post."
        )
        parser.add_argument(
            "-l",
            "--label",
            action="append",
            metavar="LABEL=VALUE",
            help="Label vote in format 'Label-Name=value' (e.g., 'Code-Review=+1'). "
            "Can be specified multiple times.",
        )
        parser.add_argument(
            "--tag", help="Tag for the review (e.g., 'autogenerated:ci')."
        )
        parser.add_argument(
            "--notify",
            choices=["NONE", "OWNER", "OWNER_REVIEWERS", "ALL"],
            help="Notify handling for the review.",
        )
        parser.add_argument(
            "--on-behalf-of", help="Account ID to post review on behalf of."
        )
        parser.add_argument(
            "--ready",
            action="store_true",
            help="Mark the change as ready for review.",
        )
        parser.add_argument(
            "--wip",
            action="store_true",
            help="Mark the change as work in progress.",
        )
        return parser

    def take_action(self, parsed_args):
        # Parse label arguments into a dict
        labels = None
        if parsed_args.label:
            labels = {}
            for label_arg in parsed_args.label:
                if "=" not in label_arg:
                    raise error.BadDataException(
                        f"Invalid label format: '{label_arg}'. Expected 'Label-Name=value'."
                    )
                name, value = label_arg.split("=", 1)
                try:
                    labels[name] = int(value)
                except ValueError:
                    raise error.BadDataException(
                        f"Invalid label value: '{value}'. Must be an integer."
                    )

        response = self.client.set_review(
            parsed_args.change_id,
            revision_id=parsed_args.revision,
            message=parsed_args.message,
            labels=labels,
            tag=parsed_args.tag,
            notify=parsed_args.notify,
            on_behalf_of=parsed_args.on_behalf_of,
            ready=parsed_args.ready if parsed_args.ready else None,
            work_in_progress=parsed_args.wip if parsed_args.wip else None,
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


# Attention Set commands


class AttentionSetMixIn:
    entity_name = "change"

    columns = (
        "account",
        "last_update",
        "reason",
    )


class ChangeAttentionSetShow(AttentionSetMixIn, base.BaseListCommand):
    """Gets the attention set of a change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_attention_set(parsed_args.change_id)
        # Response is a dict keyed by account ID, convert to list
        data = []
        if isinstance(response, dict):
            for account_id, info in response.items():
                info["account"] = account_id
                data.append(info)
        else:
            data = response
        fetched_columns = [c for c in self.columns if data and c in data[0]]
        data = utils.get_display_data_multi(fetched_columns, data)
        return fetched_columns, data


class ChangeAttentionSetAdd(AttentionSetMixIn, base.BaseCommand, base.show.ShowOne):
    """Adds a user to the attention set of a change."""

    columns = ("_account_id", "name", "email", "username", "reason", "last_update")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-a",
            "--account",
            required=True,
            help="The account identifier to add to the attention set.",
        )
        parser.add_argument(
            "-r",
            "--reason",
            help="Reason for adding the user to the attention set.",
        )
        parser.add_argument(
            "--notify",
            choices=["NONE", "OWNER", "OWNER_REVIEWERS", "ALL"],
            help="Notify handling.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.add_to_attention_set(
            parsed_args.change_id,
            account_id=parsed_args.account,
            reason=parsed_args.reason,
            notify=parsed_args.notify,
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeAttentionSetRemove(ChangeMixIn, base.BaseCommand):
    """Removes a user from the attention set of a change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-a",
            "--account",
            required=True,
            help="The account identifier to remove from the attention set.",
        )
        parser.add_argument(
            "-r",
            "--reason",
            help="Reason for removing the user from the attention set.",
        )
        parser.add_argument(
            "--notify",
            choices=["NONE", "OWNER", "OWNER_REVIEWERS", "ALL"],
            help="Notify handling.",
        )
        return parser

    def take_action(self, parsed_args):
        self.client.remove_from_attention_set(
            parsed_args.change_id,
            account_id=parsed_args.account,
            reason=parsed_args.reason,
            notify=parsed_args.notify,
        )
        self.app.stdout.write(
            f"User '{parsed_args.account}' was removed from the attention set "
            f"of change '{parsed_args.change_id}'.\n"
        )


# Work-in-Progress / Ready-for-Review commands


class ChangeWip(ChangeMixIn, base.BaseCommand):
    """Marks a change as work in progress."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-m", "--message", help="Message to be added as review comment."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.set_work_in_progress(
            parsed_args.change_id, message=parsed_args.message
        )
        self.app.stdout.write(
            f"Change '{parsed_args.change_id}' was marked as work in progress.\n"
        )


class ChangeReady(ChangeMixIn, base.BaseCommand):
    """Marks a change as ready for review."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-m", "--message", help="Message to be added as review comment."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.set_ready_for_review(
            parsed_args.change_id, message=parsed_args.message
        )
        self.app.stdout.write(
            f"Change '{parsed_args.change_id}' was marked as ready for review.\n"
        )


# Hashtags commands


class ChangeHashtagsShow(ChangeMixIn, base.BaseCommand, base.lister.Lister):
    """Gets the hashtags associated with a change."""

    columns = ("hashtag",)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_hashtags(parsed_args.change_id)
        data = [[tag] for tag in response]
        return self.columns, data


class ChangeHashtagsSet(ChangeMixIn, base.BaseCommand, base.lister.Lister):
    """Adds and/or removes hashtags from a change."""

    columns = ("hashtag",)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "--add",
            action="append",
            metavar="HASHTAG",
            help="Hashtag to add. Can be specified multiple times.",
        )
        parser.add_argument(
            "--remove",
            action="append",
            metavar="HASHTAG",
            help="Hashtag to remove. Can be specified multiple times.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_hashtags(
            parsed_args.change_id,
            add=parsed_args.add,
            remove=parsed_args.remove,
        )
        data = [[tag] for tag in response]
        return self.columns, data


# Change Messages commands


class ChangeMessageMixIn:
    entity_name = "change"

    columns = (
        "id",
        "author",
        "real_author",
        "date",
        "message",
        "tag",
        "_revision_number",
    )


class ChangeMessageList(ChangeMessageMixIn, base.BaseListCommand):
    """Lists all the messages of a change."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_messages(parsed_args.change_id)
        fetched_columns = [c for c in self.columns if response and c in response[0]]
        data = utils.get_display_data_multi(fetched_columns, response)
        return fetched_columns, data


class ChangeMessageShow(ChangeMessageMixIn, base.BaseShowCommand):
    """Retrieves a change message."""

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-m",
            "--message-id",
            required=True,
            help="The ID of the change message.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_message(
            parsed_args.entity_id, parsed_args.message_id
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeMessageDelete(ChangeMessageMixIn, base.BaseShowCommand):
    """Deletes a change message (replaces content with deletion notice)."""

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-m",
            "--message-id",
            required=True,
            help="The ID of the change message.",
        )
        parser.add_argument(
            "-r",
            "--reason",
            help="Reason for deletion.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.delete_message(
            parsed_args.entity_id,
            parsed_args.message_id,
            reason=parsed_args.reason,
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


# Revision endpoints


class RevisionFileMixIn:
    entity_name = "change"

    columns = (
        "path",
        "status",
        "lines_inserted",
        "lines_deleted",
        "size_delta",
        "size",
    )


class ChangeRevisionFileList(RevisionFileMixIn, base.BaseListCommand):
    """Lists files modified in a revision."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-r",
            "--revision",
            default="current",
            help="Revision (patchset) identifier. Defaults to 'current'.",
        )
        parser.add_argument(
            "--base", type=int, help="Patchset number to compare against."
        )
        parser.add_argument(
            "--parent",
            type=int,
            help="For merge commits, the parent number to compare against.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_revision_files(
            parsed_args.change_id,
            revision_id=parsed_args.revision,
            base=parsed_args.base,
            parent=parsed_args.parent,
        )
        # Response is a dict of file paths to FileInfo, convert to list
        data = []
        if isinstance(response, dict):
            for file_path, info in response.items():
                info["path"] = file_path
                data.append(info)
        fetched_columns = [c for c in self.columns if data and c in data[0]]
        data = utils.get_display_data_multi(fetched_columns, data)
        return fetched_columns, data


class ChangeFileDiff(ChangeMixIn, base.BaseShowCommand):
    """Gets the diff of a file from a revision."""

    columns = (
        "meta_a",
        "meta_b",
        "change_type",
        "intraline_status",
        "diff_header",
        "content",
        "binary",
    )

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "--file", required=True, help="Path of the file."
        )
        parser.add_argument(
            "-r",
            "--revision",
            default="current",
            help="Revision (patchset) identifier. Defaults to 'current'.",
        )
        parser.add_argument(
            "--base", type=int, help="Patchset number to compare against."
        )
        parser.add_argument(
            "--parent",
            type=int,
            help="For merge commits, the parent number to compare against.",
        )
        parser.add_argument(
            "--context", type=int, help="Number of context lines to include."
        )
        parser.add_argument(
            "--intraline",
            action="store_true",
            help="Include intraline differences.",
        )
        parser.add_argument(
            "--whitespace",
            choices=["IGNORE_NONE", "IGNORE_TRAILING", "IGNORE_LEADING_AND_TRAILING", "IGNORE_ALL"],
            help="Whitespace handling.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_file_diff(
            parsed_args.entity_id,
            parsed_args.file,
            revision_id=parsed_args.revision,
            base=parsed_args.base,
            parent=parsed_args.parent,
            context=parsed_args.context,
            intraline=parsed_args.intraline if parsed_args.intraline else None,
            whitespace=parsed_args.whitespace,
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeFileContent(ChangeMixIn, base.BaseCommand):
    """Gets the content of a file from a revision."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "--file", required=True, help="Path of the file."
        )
        parser.add_argument(
            "-r",
            "--revision",
            default="current",
            help="Revision (patchset) identifier. Defaults to 'current'.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_file_content(
            parsed_args.change_id,
            parsed_args.file,
            revision_id=parsed_args.revision,
        )
        self.app.stdout.write(str(response))


class ChangeRelated(ChangeMixIn, base.BaseShowCommand):
    """Gets related changes of a revision."""

    columns = ("changes",)

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-r",
            "--revision",
            default="current",
            help="Revision (patchset) identifier. Defaults to 'current'.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_related_changes(
            parsed_args.entity_id, revision_id=parsed_args.revision
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeCherryPick(ChangeMixIn, base.BaseShowCommand):
    """Cherry picks a revision to a destination branch."""

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-r",
            "--revision",
            default="current",
            help="Revision (patchset) identifier. Defaults to 'current'.",
        )
        parser.add_argument(
            "-d",
            "--destination",
            required=True,
            help="The destination branch.",
        )
        parser.add_argument(
            "-m", "--message", help="The commit message for the cherry-pick."
        )
        parser.add_argument(
            "--notify",
            choices=["NONE", "OWNER", "OWNER_REVIEWERS", "ALL"],
            help="Notify handling.",
        )
        parser.add_argument(
            "--keep-reviewers",
            action="store_true",
            help="Keep the original reviewers.",
        )
        parser.add_argument(
            "--allow-conflicts",
            action="store_true",
            help="Allow cherry-picking with conflicts.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.cherry_pick(
            parsed_args.entity_id,
            revision_id=parsed_args.revision,
            destination=parsed_args.destination,
            message=parsed_args.message,
            notify=parsed_args.notify,
            keep_reviewers=parsed_args.keep_reviewers if parsed_args.keep_reviewers else None,
            allow_conflicts=parsed_args.allow_conflicts if parsed_args.allow_conflicts else None,
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangePatch(ChangeMixIn, base.BaseCommand):
    """Gets the formatted patch for a revision."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "change_id", metavar="change-identifier", help="Change identifier."
        )
        parser.add_argument(
            "-r",
            "--revision",
            default="current",
            help="Revision (patchset) identifier. Defaults to 'current'.",
        )
        parser.add_argument(
            "-p", "--path", help="Only return the patch for the specified file."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_patch(
            parsed_args.change_id,
            revision_id=parsed_args.revision,
            path=parsed_args.path,
        )
        self.app.stdout.write(str(response))


# Submitted Together command


class ChangeSubmittedTogether(ChangeMixIn, base.BaseShowCommand):
    """Gets the list of changes that would be submitted together."""

    columns = ("changes", "non_visible_changes")

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-o",
            "--option",
            nargs="+",
            help="Additional options (e.g., 'NON_VISIBLE_CHANGES').",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_submitted_together(
            parsed_args.entity_id, options=parsed_args.option
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug

    debug("show", ChangeShow, argv)


if __name__ == "__main__":
    debug()
