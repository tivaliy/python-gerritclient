import abc
import argparse

from gerritclient import error
from gerritclient.commands import base
from gerritclient.common import utils


class AccountMixIn:
    entity_name = "account"


class AccountList(AccountMixIn, base.BaseListCommand):
    """Lists all accounts in Gerrit visible to the caller."""

    columns = ("_account_id",)

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument("query", help="Query string.")
        parser.add_argument(
            "--suggest", action="store_true", help="Get account suggestions."
        )
        parser.add_argument(
            "-l",
            "--limit",
            type=int,
            help="Limit the number of accounts to be included in the results.",
        )
        parser.add_argument(
            "-S",
            "--skip",
            type=int,
            help="Skip the given number of accounts from the beginning of the list.",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Includes full name, preferred email, "
            "username and avatars for each account.",
        )
        parser.add_argument(
            "--all-emails", action="store_true", help="Includes all registered emails."
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.all or parsed_args.suggest:
            self.columns += ("username", "name", "email")
        if parsed_args.all_emails and not parsed_args.all:
            self.columns += ("email", "secondary_emails")
        if (parsed_args.all_emails and parsed_args.all) or parsed_args.suggest:
            self.columns += ("secondary_emails",)

        response = self.client.get_all(
            parsed_args.query,
            suggested=parsed_args.suggest,
            limit=parsed_args.limit,
            skip=parsed_args.skip,
            detailed=parsed_args.all,
            all_emails=parsed_args.all_emails,
        )
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class AccountShow(AccountMixIn, base.BaseShowCommand):
    """Shows information about specific account in Gerrit."""

    columns = ("_account_id", "name", "email", "username", "status")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "-a", "--all", action="store_true", help="Show more details about account."
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.all:
            self.columns += ("secondary_emails", "registered_on")
        response = self.client.get_by_id(
            parsed_args.entity_id, detailed=parsed_args.all
        )
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class AccountCreate(AccountMixIn, base.BaseCreateCommand):
    """Creates a new account in Gerrit Code Review."""

    columns = ("_account_id", "username", "name", "email")


class BaseAccountSetCommand(AccountMixIn, base.BaseCommand, abc.ABC):
    @abc.abstractmethod
    def action(self, account_id, attribute):
        pass

    @property
    @abc.abstractmethod
    def attribute(self):
        pass

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        parser.add_argument(
            "attribute",
            metavar=f"{self.attribute}",
            help=f"Account {self.attribute}.",
        )
        return parser

    def take_action(self, parsed_args):
        self.action(parsed_args.account_id, parsed_args.attribute)
        msg = f"{self.attribute.capitalize()} for the account with identifier '{parsed_args.account_id}' was successfully set.\n"
        self.app.stdout.write(msg)


class AccountSetName(BaseAccountSetCommand):
    """Sets the full name of an account in Gerrit Code Review."""

    attribute = "name"

    def action(self, account_id, attribute):
        return self.client.set_name(account_id, name=attribute)


class AccountSetUsername(BaseAccountSetCommand):
    """Sets the username of an account in Gerrit Code Review."""

    attribute = "username"

    def action(self, account_id, attribute):
        return self.client.set_username(account_id, username=attribute)


class AccountEnable(AccountMixIn, base.BaseEntitySetState):
    """Sets the account state in Gerrit to active."""

    action_type = "enable"


class AccountDisable(AccountMixIn, base.BaseEntitySetState):
    """Sets the account state in Gerrit to inactive."""

    action_type = "disable"


class AccountStateShow(AccountMixIn, base.BaseShowCommand):
    """Fetches the state of an account in Gerrit."""

    columns = ("account_identifier", "is_active")

    def take_action(self, parsed_args):
        response = self.client.is_active(parsed_args.entity_id)
        data = {self.columns[0]: parsed_args.entity_id, self.columns[1]: response}
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data


class AccountStatusShow(AccountMixIn, base.BaseShowCommand):
    """Retrieves the status of an account."""

    columns = ("account_identifier", "status")

    def take_action(self, parsed_args):
        response = self.client.get_status(parsed_args.entity_id)
        data = {self.columns[0]: parsed_args.entity_id, self.columns[1]: response}
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data


class AccountStatusSet(BaseAccountSetCommand):
    """Sets the status of an account."""

    attribute = "status"

    def action(self, account_id, attribute):
        return self.client.set_status(account_id, status=attribute)


class AccountSetPassword(AccountMixIn, base.BaseShowCommand):
    """Sets/Generates the HTTP password of an account in Gerrit."""

    columns = ("account_identifier", "http_password")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--generate", action="store_true", help="Generate HTTP password."
        )
        group.add_argument("-p", "--password", help="HTTP password.")
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_password(
            parsed_args.entity_id, parsed_args.password, parsed_args.generate
        )
        data = {
            "account_identifier": parsed_args.entity_id,
            "http_password": response if response else None,
        }
        data = utils.get_display_data_single(self.columns, data)

        return self.columns, data


class AccountDeletePassword(AccountMixIn, base.BaseCommand):
    """Deletes the HTTP password of an account in Gerrit."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete_password(parsed_args.account_id)
        msg = (
            f"HTTP password for the account with identifier '{parsed_args.account_id}' "
            "was successfully removed.\n"
        )
        self.app.stdout.write(msg)


class AccountSSHKeyList(AccountMixIn, base.BaseListCommand):
    """Returns the SSH keys of an account in Gerrit."""

    columns = ("seq", "ssh_public_key", "encoded_key", "algorithm", "comment", "valid")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_ssh_keys(parsed_args.account_id)
        data = utils.get_display_data_multi(self.columns, response)

        return self.columns, data


class AccountSSHKeyShow(AccountMixIn, base.BaseShowCommand):
    """Retrieves an SSH key of a user in Gerrit."""

    columns = ("seq", "ssh_public_key", "encoded_key", "algorithm", "comment", "valid")

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-s",
            "--sequence-id",
            type=int,
            required=True,
            help="The sequence number of the SSH key.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_ssh_key(
            parsed_args.entity_id, parsed_args.sequence_id
        )
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class AccountSSHKeyAdd(AccountMixIn, base.BaseShowCommand):
    """Adds an SSH key for a user in Gerrit."""

    columns = ("seq", "ssh_public_key", "encoded_key", "algorithm", "comment", "valid")

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist")
        return file_path

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--ssh-key", help="The SSH public key.")
        group.add_argument(
            "--file",
            metavar="SSH_KEY_FILE",
            type=self.get_file_path,
            help="File with the SSH public key.",
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        ssh_key = parsed_args.ssh_key
        if file_path:
            try:
                with open(file_path, "r") as stream:
                    ssh_key = stream.read()
            except OSError:
                msg = f"Could not read file '{file_path}'"
                raise error.InvalidFileException(msg)
        response = self.client.add_ssh_key(parsed_args.entity_id, ssh_key)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class AccountSSHKeyDelete(AccountMixIn, base.BaseCommand):
    """Deletes an SSH key of a user in Gerrit."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        parser.add_argument(
            "--sequence-id",
            required=True,
            type=int,
            help="The sequence number of the SSH key.",
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete_ssh_key(parsed_args.account_id, parsed_args.sequence_id)
        msg = (
            f"SSH key with id '{parsed_args.sequence_id}' for the account with identifier '{parsed_args.account_id}' "
            "was successfully removed.\n"
        )
        self.app.stdout.write(msg)


class AccountMembershipList(AccountMixIn, base.BaseListCommand):
    """Lists all groups that contain the specified user as a member."""

    columns = (
        "group_id",
        "name",
        "id",
        "url",
        "options",
        "description",
        "owner",
        "owner_id",
    )

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_membership(parsed_args.account_id)
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class AccountEmailAdd(AccountMixIn, base.BaseShowCommand):
    """Registers a new email address for the user in Gerrit."""

    columns = ("email", "preferred", "pending_confirmation")

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument("-e", "--email", required=True, help="Account email.")
        parser.add_argument(
            "--preferred", action="store_true", help="Set email address as preferred."
        )
        parser.add_argument(
            "--no-confirmation",
            action="store_true",
            help="Email address confirmation. Only Gerrit administrators "
            "are allowed to add email addresses without confirmation.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.add_email(
            parsed_args.entity_id,
            parsed_args.email,
            preferred=parsed_args.preferred,
            no_confirmation=parsed_args.no_confirmation,
        )
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class AccountEmailDelete(AccountMixIn, base.BaseCommand):
    """Deletes an email address of an account in Gerrit."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        parser.add_argument("-e", "--email", required=True, help="Account email.")
        return parser

    def take_action(self, parsed_args):
        self.client.delete_email(parsed_args.account_id, parsed_args.email)
        msg = (
            f"Email address '{parsed_args.email}' of the account with identifier '{parsed_args.account_id}' "
            "was successfully removed.\n"
        )
        self.app.stdout.write(msg)


class AccountPreferredEmailSet(BaseAccountSetCommand):
    """Sets an email address as preferred email address for an account."""

    attribute = "email"

    def action(self, account_id, attribute):
        return self.client.set_preferred_email(account_id, email=attribute)


class AccountOAuthShow(AccountMixIn, base.BaseShowCommand):
    """Returns a previously obtained OAuth access token.

    If there is no token available, or the token has already expired,
    "404 Not Found" is returned as response. Requests to obtain an access
    token of another user are rejected with "403 Forbidden".
    """

    columns = (
        "username",
        "resource_host",
        "access_token",
        "provider_id",
        "expires_at",
        "type",
    )

    def take_action(self, parsed_args):
        response = self.client.get_oauth_token(parsed_args.entity_id)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


# Preferences commands


class AccountPreferencesShow(AccountMixIn, base.BaseShowCommand):
    """Gets the preferences of an account."""

    columns = (
        "changes_per_page",
        "theme",
        "date_format",
        "time_format",
        "diff_view",
        "expand_inline_diffs",
        "relative_date_in_change_table",
        "size_bar_in_change_table",
        "publish_comments_on_push",
        "work_in_progress_by_default",
    )

    def take_action(self, parsed_args):
        response = self.client.get_preferences(parsed_args.entity_id)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class AccountPreferencesSet(AccountMixIn, base.BaseShowCommand):
    """Sets the preferences of an account."""

    columns = (
        "changes_per_page",
        "theme",
        "diff_view",
    )

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist")
        return file_path

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "--file",
            type=self.get_file_path,
            required=True,
            help="File with preferences JSON/YAML.",
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        try:
            preferences = utils.read_from_file(file_path)
        except OSError:
            msg = f"Could not read preferences at {file_path}"
            raise error.InvalidFileException(msg)

        response = self.client.set_preferences(parsed_args.entity_id, preferences)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class AccountDiffPreferencesShow(AccountMixIn, base.BaseShowCommand):
    """Gets the diff preferences of an account."""

    columns = (
        "context",
        "tab_size",
        "line_length",
        "cursor_blink_rate",
        "expand_all_comments",
        "ignore_whitespace",
        "intraline_difference",
        "show_line_endings",
        "show_tabs",
        "show_whitespace_errors",
        "syntax_highlighting",
        "hide_top_menu",
        "auto_hide_diff_table_header",
        "hide_line_numbers",
        "render_entire_file",
        "hide_empty_pane",
        "match_brackets",
        "line_wrapping",
    )

    def take_action(self, parsed_args):
        response = self.client.get_diff_preferences(parsed_args.entity_id)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class AccountDiffPreferencesSet(AccountMixIn, base.BaseShowCommand):
    """Sets the diff preferences of an account."""

    columns = ("context", "tab_size", "line_length", "ignore_whitespace")

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist")
        return file_path

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "--file",
            type=self.get_file_path,
            required=True,
            help="File with diff preferences JSON/YAML.",
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        try:
            preferences = utils.read_from_file(file_path)
        except OSError:
            msg = f"Could not read preferences at {file_path}"
            raise error.InvalidFileException(msg)

        response = self.client.set_diff_preferences(parsed_args.entity_id, preferences)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


# Capabilities commands


class AccountCapabilitiesShow(AccountMixIn, base.BaseShowCommand):
    """Gets the capabilities of an account."""

    columns = (
        "accessDatabase",
        "administrateServer",
        "createAccount",
        "createGroup",
        "createProject",
        "emailReviewers",
        "flushCaches",
        "killTask",
        "maintainServer",
        "modifyAccount",
        "priority",
        "queryLimit",
        "runAs",
        "runGC",
        "streamEvents",
        "viewAllAccounts",
        "viewCaches",
        "viewConnections",
        "viewPlugins",
        "viewQueue",
    )

    def get_parser(self, app_name):
        parser = super().get_parser(app_name)
        parser.add_argument(
            "-q",
            "--query",
            nargs="+",
            help="Filter to specific capabilities.",
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_capabilities(
            parsed_args.entity_id, capabilities=parsed_args.query
        )
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


# Starred Changes commands


class AccountStarredChangeList(AccountMixIn, base.BaseListCommand):
    """Lists the starred changes of an account."""

    columns = (
        "id",
        "project",
        "branch",
        "change_id",
        "subject",
        "status",
        "_number",
    )

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_starred_changes(parsed_args.account_id)
        fetched_columns = [c for c in self.columns if response and c in response[0]]
        data = utils.get_display_data_multi(fetched_columns, response)
        return fetched_columns, data


class AccountStarredChangeAdd(AccountMixIn, base.BaseCommand):
    """Stars a change for an account."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        parser.add_argument(
            "-c", "--change-id", required=True, help="Change identifier to star."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.star_change(parsed_args.account_id, parsed_args.change_id)
        self.app.stdout.write(
            f"Change '{parsed_args.change_id}' was starred for account '{parsed_args.account_id}'.\n"
        )


class AccountStarredChangeDelete(AccountMixIn, base.BaseCommand):
    """Unstars a change for an account."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "account_id", metavar="account-identifier", help="Account identifier."
        )
        parser.add_argument(
            "-c", "--change-id", required=True, help="Change identifier to unstar."
        )
        return parser

    def take_action(self, parsed_args):
        self.client.unstar_change(parsed_args.account_id, parsed_args.change_id)
        self.app.stdout.write(
            f"Change '{parsed_args.change_id}' was unstarred for account '{parsed_args.account_id}'.\n"
        )


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug

    debug("list", AccountList, argv)


if __name__ == "__main__":
    debug()
