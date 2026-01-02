import json
from unittest import mock

import pytest

from gerritclient.tests.unit.cli import clibase
from gerritclient.tests.utils import fake_account, fake_change, fake_comment


class TestChangeCommand(clibase.BaseCLITest):
    """Tests for gerrit change * commands."""

    def test_change_list_w_single_query(self):
        query = ["status:open+is:watched"]
        args = "change list {query} --max-width 110".format(query="".join(query))
        self.m_client.get_all.return_value = fake_change.get_fake_changes(5)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            query=query, options=None, limit=None, skip=None
        )

    def test_change_list_w_multiple_queries(self):
        query = ["status:open+is:watched", "is:closed+owner:self+limit:5"]
        args = "change list {query} --max-width 110".format(query=" ".join(query))
        self.m_client.get_all.return_value = [
            fake_change.get_fake_changes(3),
            fake_change.get_fake_changes(2),
        ]
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            query=query, options=None, limit=None, skip=None
        )

    def test_change_list_w_skip(self):
        skip = 2
        query = ["status:open+is:watched"]
        args = "change list {query} --skip {skip} --max-width 110".format(
            query="".join(query), skip=skip
        )
        self.m_client.get_all.return_value = fake_change.get_fake_changes(5)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            query=query, options=None, limit=None, skip=skip
        )

    def test_change_list_w_limit(self):
        limit = 2
        query = ["status:open+is:watched"]
        args = "change list {query} --limit {limit} --max-width 110".format(
            query="".join(query), limit=limit
        )
        self.m_client.get_all.return_value = fake_change.get_fake_changes(2)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            query=query, options=None, limit=limit, skip=None
        )

    def test_change_list_w_options(self):
        options = ["LABELS", "MESSAGES", "REVIEWED"]
        query = ["status:open+is:watched"]
        args = "change list {query} --option {option} --max-width 110".format(
            query="".join(query), option=" ".join(options)
        )
        self.m_client.get_all.return_value = fake_change.get_fake_changes(2)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            query=query, options=options, limit=None, skip=None
        )

    def test_change_show_wo_details(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change show {change_id} --max-width 110"
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            identifier=change_id
        )
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(
            change_id=change_id, detailed=False, options=None
        )

    def test_change_show_w_details(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change show {change_id} --all --max-width 110"
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            identifier=change_id
        )
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(
            change_id=change_id, detailed=True, options=None
        )

    def test_change_show_w_options(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        options = ["LABELS", "MESSAGES", "REVIEWED"]
        args = "change show {change_id} --option {options} --max-width 110".format(
            change_id=change_id, options=" ".join(options)
        )
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            identifier=change_id
        )
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(
            change_id=change_id, detailed=False, options=options
        )

    @mock.patch("gerritclient.common.utils.file_exists", mock.Mock(return_value=True))
    def test_change_create(self):
        test_data = {
            "project": "myProject",
            "subject": "Fake subject",
            "branch": "master",
            "topic": "create-change-in-browser",
        }
        expected_path = "/tmp/fakes/fake-change.json"
        args = f"change create {expected_path}"
        self.m_client.create.return_value = fake_change.get_fake_change(**test_data)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch("gerritclient.common.utils.open", m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, "r")
        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.create.assert_called_once_with(test_data)

    @mock.patch("gerritclient.common.utils.file_exists", mock.Mock(return_value=True))
    @mock.patch("sys.stderr")
    def test_change_create_bad_file_format_fail(self, mocked_stderr):
        test_data = {}
        expected_path = "/tmp/fakes/bad_file.format"
        args = f"change create {expected_path}"

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch("gerritclient.common.utils.open", m_open, create=True):
            result = self.exec_command(args)
            assert result == 1
            stderr_output = "".join(
                call[0][0] for call in mocked_stderr.write.call_args_list
            )
            assert "Unsupported data format" in stderr_output

    def test_change_delete(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change delete {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.delete.assert_called_once_with(change_id)

    def test_change_abandon(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change abandon {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.abandon.assert_called_once_with(change_id)

    def test_change_restore(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change restore {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.restore.assert_called_once_with(change_id)

    def test_change_revert(self):
        message = "Fake message"
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f'change revert {change_id} --message "{message}"'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.revert.assert_called_once_with(change_id, message=message)

    def test_change_rebase(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change rebase {change_id} "
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.rebase.assert_called_once_with(change_id, parent=None)

    def test_change_rebase_w_parent(self):
        base = "6f0aea35251c48692e7e88ee3bc2bfa53684cd39"
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change rebase {change_id} --parent {base} "
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.rebase.assert_called_once_with(change_id, parent=base)

    def test_change_move(self):
        message = "Fake message"
        branch = "fake-branch"
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f'change move {change_id} -b {branch} -m "{message}"'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.move.assert_called_once_with(change_id, branch, message=message)

    def test_change_submit_wo_parameters(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change submit {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.submit.assert_called_once_with(
            change_id, on_behalf_of=None, notify="ALL"
        )

    def test_change_submit_w_parameters(self):
        notify = "NONE"
        username = "jdoe"
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change submit {change_id} --on-behalf-of {username} --notify {notify}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.submit.assert_called_once_with(
            change_id, on_behalf_of=username, notify=notify
        )

    def test_change_topic_show(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change topic show {change_id}"
        self.m_client.get_topic.return_value = "Fake topic"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_topic.assert_called_once_with(change_id)

    def test_change_topic_set(self):
        topic = "New fake topic"
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f'change topic set {change_id} --topic "{topic}"'
        self.m_client.set_topic.return_value = topic
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_topic.assert_called_once_with(change_id, topic)

    def test_change_topic_delete(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change topic delete {change_id}"
        self.m_client.delete_topic.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.delete_topic.assert_called_once_with(change_id)

    def test_change_assignee_show(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change assignee show {change_id}"
        account = fake_account.get_fake_account()
        self.m_client.get_assignee.return_value = account
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_assignee.assert_called_once_with(change_id)

    def test_change_assignee_history_show(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change assignee history show {change_id}"
        fake_accounts = fake_account.get_fake_accounts(3)
        self.m_client.get_assignee.return_value = fake_accounts
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_assignees.assert_called_once_with(change_id)

    def test_change_assignee_set(self):
        account = {
            "_account_id": 26071983,
            "name": "John Doe",
            "username": "jdoe",
            "email": "jdoe@example.com",
        }
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = "change assignee set {change_id} --account {account}".format(
            change_id=change_id, account=account["username"]
        )
        account = fake_account.get_fake_account(**account)
        self.m_client.set_assignee.return_value = account
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_assignee.assert_called_once_with(
            change_id, account["username"]
        )

    def test_change_assignee_delete(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change assignee delete {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.delete_assignee.assert_called_once_with(change_id)

    def test_change_draft_publish(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change draft publish {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.publish_draft.assert_called_once_with(change_id)

    def test_change_included_get(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change included-in show {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_included.assert_called_once_with(change_id)

    def test_change_index(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change index {change_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.index.assert_called_once_with(change_id)

    def test_change_comments_list(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change comment list {change_id} --max-width 110"
        fake_comments = fake_comment.get_fake_comments_in_change(3)
        self.m_client.get_comments.return_value = fake_comments
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_comments.assert_called_once_with(change_id, comment_type=None)

    def test_change_draft_comments_list(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change comment list {change_id} --type drafts --max-width 110"
        fake_comments = fake_comment.get_fake_comments_in_change(3)
        self.m_client.get_comments.return_value = fake_comments
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_comments.assert_called_once_with(
            change_id, comment_type="drafts"
        )

    def test_change_robotcomments_list(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change comment list {change_id} --type robotcomments --max-width 110"
        fake_comments = fake_comment.get_fake_comments_in_change(3)
        self.m_client.get_comments.return_value = fake_comments
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_comments.assert_called_once_with(
            change_id, comment_type="robotcomments"
        )

    @mock.patch("sys.stderr")
    def test_change_comments_list_w_wrong_type_fail(self, mocked_stderr):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change comment list {change_id} --type bad_comment"
        with pytest.raises(SystemExit):
            self.exec_command(args)
        assert "invalid choice: 'bad_comment'" in mocked_stderr.write.call_args_list[-1][0][0]

    def test_change_consistency_check(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change check {change_id} --max-width 110"
        change = fake_change.get_fake_change(identifier=change_id)
        self.m_client.check_consistency.return_value = change
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.check_consistency.assert_called_once_with(change_id)

    def test_change_consistency_check_and_fix(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change fix {change_id} --max-width 110"
        change = fake_change.get_fake_change(identifier=change_id)
        self.m_client.fix_consistency.return_value = change
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.fix_consistency.assert_called_once_with(
            change_id, is_delete=False, expect_merged_as=False
        )

    def test_change_consistency_check_and_fix_w_parameters(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = (
            f"change fix {change_id} --delete-patchset --expect-merged-as "
            "--max-width 110"
        )
        change = fake_change.get_fake_change(identifier=change_id)
        self.m_client.fix_consistency.return_value = change
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.fix_consistency.assert_called_once_with(
            change_id, is_delete=True, expect_merged_as=True
        )

    # Reviewer tests

    def test_change_reviewer_list(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change reviewer list {change_id} --max-width 110"
        fake_reviewers = fake_account.get_fake_accounts(3)
        self.m_client.get_reviewers.return_value = fake_reviewers
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_reviewers.assert_called_once_with(change_id)

    def test_change_reviewer_show(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        account_id = "jdoe"
        args = f"change reviewer show {change_id} --account {account_id}"
        self.m_client.get_reviewer.return_value = fake_account.get_fake_account()
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_reviewer.assert_called_once_with(change_id, account_id)

    def test_change_reviewer_add(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        reviewer = "jdoe"
        args = f"change reviewer add {change_id} --reviewer {reviewer}"
        self.m_client.add_reviewer.return_value = {"input": reviewer, "reviewers": []}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.add_reviewer.assert_called_once_with(
            change_id, reviewer=reviewer, state="REVIEWER", confirmed=None, notify=None
        )

    def test_change_reviewer_add_as_cc(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        reviewer = "jdoe"
        args = f"change reviewer add {change_id} --reviewer {reviewer} --state CC"
        self.m_client.add_reviewer.return_value = {"input": reviewer, "ccs": []}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.add_reviewer.assert_called_once_with(
            change_id, reviewer=reviewer, state="CC", confirmed=None, notify=None
        )

    def test_change_reviewer_add_w_confirmed(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        reviewer = "big-group"
        args = f"change reviewer add {change_id} --reviewer {reviewer} --confirmed"
        self.m_client.add_reviewer.return_value = {"input": reviewer, "reviewers": []}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.add_reviewer.assert_called_once_with(
            change_id, reviewer=reviewer, state="REVIEWER", confirmed=True, notify=None
        )

    def test_change_reviewer_delete(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        account_id = "jdoe"
        args = f"change reviewer delete {change_id} --account {account_id}"
        self.m_client.delete_reviewer.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.delete_reviewer.assert_called_once_with(
            change_id, account_id=account_id, notify=None
        )

    def test_change_reviewer_suggest(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        query = "john"
        args = f"change reviewer suggest {change_id} --query {query}"
        self.m_client.suggest_reviewers.return_value = [
            {"account": fake_account.get_fake_account(), "count": 5}
        ]
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.suggest_reviewers.assert_called_once_with(
            change_id, query=query, limit=None, exclude_groups=None
        )

    # Review (voting) tests

    def test_change_review_w_message(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        message = "Looks good to me"
        args = f'change review {change_id} --message "{message}"'
        self.m_client.set_review.return_value = {"labels": {}}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_review.assert_called_once_with(
            change_id,
            revision_id="current",
            message=message,
            labels=None,
            tag=None,
            notify=None,
            on_behalf_of=None,
            ready=None,
            work_in_progress=None,
        )

    def test_change_review_w_labels(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change review {change_id} --label Code-Review=+1 --label Verified=+1"
        self.m_client.set_review.return_value = {"labels": {"Code-Review": 1, "Verified": 1}}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_review.assert_called_once_with(
            change_id,
            revision_id="current",
            message=None,
            labels={"Code-Review": 1, "Verified": 1},
            tag=None,
            notify=None,
            on_behalf_of=None,
            ready=None,
            work_in_progress=None,
        )

    def test_change_review_w_revision(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        revision = "2"
        args = f"change review {change_id} --revision {revision} --label Code-Review=-1"
        self.m_client.set_review.return_value = {"labels": {"Code-Review": -1}}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_review.assert_called_once_with(
            change_id,
            revision_id=revision,
            message=None,
            labels={"Code-Review": -1},
            tag=None,
            notify=None,
            on_behalf_of=None,
            ready=None,
            work_in_progress=None,
        )

    def test_change_review_w_ready(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change review {change_id} --ready"
        self.m_client.set_review.return_value = {"ready": True}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_review.assert_called_once_with(
            change_id,
            revision_id="current",
            message=None,
            labels=None,
            tag=None,
            notify=None,
            on_behalf_of=None,
            ready=True,
            work_in_progress=None,
        )

    # Attention Set tests

    def test_change_attention_set_show(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change attention-set show {change_id}"
        self.m_client.get_attention_set.return_value = {
            "1000096": {"account": {"_account_id": 1000096}, "reason": "Reviewer"}
        }
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_attention_set.assert_called_once_with(change_id)

    def test_change_attention_set_add(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        account_id = "jdoe"
        reason = "Please review"
        args = f'change attention-set add {change_id} --account {account_id} --reason "{reason}"'
        self.m_client.add_to_attention_set.return_value = fake_account.get_fake_account()
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.add_to_attention_set.assert_called_once_with(
            change_id, account_id=account_id, reason=reason, notify=None
        )

    def test_change_attention_set_remove(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        account_id = "jdoe"
        args = f"change attention-set remove {change_id} --account {account_id}"
        self.m_client.remove_from_attention_set.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.remove_from_attention_set.assert_called_once_with(
            change_id, account_id=account_id, reason=None, notify=None
        )

    # WIP / Ready tests

    def test_change_wip(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change wip {change_id}"
        self.m_client.set_work_in_progress.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_work_in_progress.assert_called_once_with(
            change_id, message=None
        )

    def test_change_wip_w_message(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        message = "Still working on this"
        args = f'change wip {change_id} --message "{message}"'
        self.m_client.set_work_in_progress.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_work_in_progress.assert_called_once_with(
            change_id, message=message
        )

    def test_change_ready(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change ready {change_id}"
        self.m_client.set_ready_for_review.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_ready_for_review.assert_called_once_with(
            change_id, message=None
        )

    def test_change_ready_w_message(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        message = "Ready for review now"
        args = f'change ready {change_id} --message "{message}"'
        self.m_client.set_ready_for_review.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_ready_for_review.assert_called_once_with(
            change_id, message=message
        )

    # Hashtags tests

    def test_change_hashtags_show(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change hashtags show {change_id}"
        self.m_client.get_hashtags.return_value = ["bug", "urgent"]
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_hashtags.assert_called_once_with(change_id)

    def test_change_hashtags_set_add(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change hashtags set {change_id} --add feature --add urgent"
        self.m_client.set_hashtags.return_value = ["feature", "urgent"]
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_hashtags.assert_called_once_with(
            change_id, add=["feature", "urgent"], remove=None
        )

    def test_change_hashtags_set_remove(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change hashtags set {change_id} --remove wip"
        self.m_client.set_hashtags.return_value = []
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.set_hashtags.assert_called_once_with(
            change_id, add=None, remove=["wip"]
        )

    # Change Messages tests

    def test_change_message_list(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change message list {change_id} --max-width 110"
        self.m_client.get_messages.return_value = [
            {"id": "msg1", "message": "Uploaded patch set 1.", "date": "2024-01-01"}
        ]
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_messages.assert_called_once_with(change_id)

    def test_change_message_show(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        message_id = "abc123"
        args = f"change message show {change_id} --message-id {message_id}"
        self.m_client.get_message.return_value = {
            "id": message_id, "message": "Test message", "date": "2024-01-01"
        }
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_message.assert_called_once_with(change_id, message_id)

    def test_change_message_delete(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        message_id = "abc123"
        reason = "Spam"
        args = f'change message delete {change_id} --message-id {message_id} --reason "{reason}"'
        self.m_client.delete_message.return_value = {
            "id": message_id, "message": "Message deleted", "date": "2024-01-01"
        }
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.delete_message.assert_called_once_with(
            change_id, message_id, reason=reason
        )

    # Submitted Together tests

    def test_change_submitted_together(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change submitted-together {change_id}"
        self.m_client.get_submitted_together.return_value = {"changes": [], "non_visible_changes": 0}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_submitted_together.assert_called_once_with(
            change_id, options=None
        )

    def test_change_submitted_together_w_options(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change submitted-together {change_id} --option NON_VISIBLE_CHANGES"
        self.m_client.get_submitted_together.return_value = {"changes": [], "non_visible_changes": 2}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_submitted_together.assert_called_once_with(
            change_id, options=["NON_VISIBLE_CHANGES"]
        )

    # Revision file tests

    def test_change_revision_file_list(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change revision file-list {change_id} --max-width 110"
        self.m_client.get_revision_files.return_value = {
            "/COMMIT_MSG": {"lines_inserted": 10},
            "src/main.py": {"status": "M", "lines_inserted": 5, "lines_deleted": 2},
        }
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_revision_files.assert_called_once_with(
            change_id, revision_id="current", base=None, parent=None
        )

    def test_change_revision_file_list_w_revision(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        revision = "2"
        args = f"change revision file-list {change_id} --revision {revision}"
        self.m_client.get_revision_files.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_revision_files.assert_called_once_with(
            change_id, revision_id=revision, base=None, parent=None
        )

    def test_change_file_diff(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        file_path = "src/main.py"
        args = f"change file diff {change_id} --file {file_path}"
        self.m_client.get_file_diff.return_value = {
            "meta_a": {"name": file_path},
            "meta_b": {"name": file_path},
            "change_type": "MODIFIED",
            "content": [],
        }
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_file_diff.assert_called_once_with(
            change_id,
            file_path,
            revision_id="current",
            base=None,
            parent=None,
            context=None,
            intraline=None,
            whitespace=None,
        )

    def test_change_file_diff_w_options(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        file_path = "src/main.py"
        args = f"change file diff {change_id} --file {file_path} --context 5 --intraline --whitespace IGNORE_ALL"
        self.m_client.get_file_diff.return_value = {"content": []}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_file_diff.assert_called_once_with(
            change_id,
            file_path,
            revision_id="current",
            base=None,
            parent=None,
            context=5,
            intraline=True,
            whitespace="IGNORE_ALL",
        )

    def test_change_file_content(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        file_path = "src/main.py"
        args = f"change file content {change_id} --file {file_path}"
        self.m_client.get_file_content.return_value = "cHJpbnQoJ2hlbGxvJyk="
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_file_content.assert_called_once_with(
            change_id, file_path, revision_id="current"
        )

    def test_change_related(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change related {change_id}"
        self.m_client.get_related_changes.return_value = {"changes": []}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_related_changes.assert_called_once_with(
            change_id, revision_id="current"
        )

    def test_change_cherry_pick(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        destination = "stable-1.0"
        args = f"change cherry-pick {change_id} --destination {destination}"
        self.m_client.cherry_pick.return_value = fake_change.get_fake_change()
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.cherry_pick.assert_called_once_with(
            change_id,
            revision_id="current",
            destination=destination,
            message=None,
            notify=None,
            keep_reviewers=None,
            allow_conflicts=None,
        )

    def test_change_cherry_pick_w_options(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        destination = "stable-1.0"
        message = "Cherry-pick to stable"
        args = f'change cherry-pick {change_id} --destination {destination} --message "{message}" --keep-reviewers'
        self.m_client.cherry_pick.return_value = fake_change.get_fake_change()
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.cherry_pick.assert_called_once_with(
            change_id,
            revision_id="current",
            destination=destination,
            message=message,
            notify=None,
            keep_reviewers=True,
            allow_conflicts=None,
        )

    def test_change_patch(self):
        change_id = "I8473b95934b5732ac55d26311a706c9c2bde9940"
        args = f"change patch {change_id}"
        self.m_client.get_patch.return_value = "ZGlmZiAtLWdpdCBhL2Zvby5weSBiL2Zvby5weQ=="
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("change", mock.ANY)
        self.m_client.get_patch.assert_called_once_with(
            change_id, revision_id="current", path=None
        )
