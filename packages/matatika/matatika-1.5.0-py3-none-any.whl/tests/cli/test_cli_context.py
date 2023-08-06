"""CLI 'context' command test module"""

from matatika.cli.commands.root import matatika
from matatika.context import DEFAULT, TEMPLATE, CONTEXTS
from tests.cli.test_cli import (
    MOCK_CONTEXTS_JSON,
    TestCLI
)


class TestCLIContext(TestCLI):
    """Test class for CLI context command"""

    #
    # list
    #

    def test_list(self):
        """Test list with existing contexts in the contexts file"""

        result = self.runner.invoke(matatika, ["context",
                                               "list"])

        for context_name in MOCK_CONTEXTS_JSON[CONTEXTS]:
            self.assertIn(context_name, result.output)

        self.assertIs(result.exit_code, 0)

    def test_list_no_contexts(self):
        """Test list with no existing contexts in the contexts file"""

        result = self.runner.invoke(matatika, ["context",
                                               "list"])
        self.assertIs(result.exit_code, 0)

    #
    # create
    #

    def test_create_no_context_name_arg(self):
        """Test create without context name argument"""

        result = self.runner.invoke(matatika, ["context",
                                               "create"])

        self.assertIn("Error: Missing argument 'CONTEXT_NAME'.", result.output)
        self.assertIs(result.exit_code, 2)

    def test_create_no_auth_token_opt(self):
        """Test create without required auth token option"""

        context_name = "unittest-context1"

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name])

        self.assertIn("Error: Missing option '--auth-token' / '-a'.",
                      result.output)
        self.assertIs(result.exit_code, 2)

    def test_create_no_non_required_opts(self):
        """Test create without all non-required options specified"""

        context_name = "unittest-context1"
        variables = {
            'auth_token': "unittest_auth_token",
            'endpoint_url': "unittest_endpoint_url",
            'workspace_id': "unittest_workspace_id"
        }

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name,
                                               "-a", variables['auth_token']])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_create_all_opts(self):
        """Test create with all non-required options specified"""

        context_name = "unittest-context1"
        variables = {
            'auth_token': "unittest_auth_token",
            'endpoint_url': "unittest_endpoint_url",
            'workspace_id': "4862da59-8061-47e4-a55c-c5c83f64fcb6"
        }

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name,
                                               "-a", variables['auth_token'],
                                               "-e", variables['endpoint_url'],
                                               "-w", variables['workspace_id']])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    #
    # info
    #
    def test_info(self):
        """Test info with a default context set in the contexts file"""

        result = self.runner.invoke(matatika, ["context",
                                               "info"])

        default_context_name = MOCK_CONTEXTS_JSON[DEFAULT]

        for value in MOCK_CONTEXTS_JSON[CONTEXTS][default_context_name].values():
            self.assertIn(value, result.output)

        self.assertIs(result.exit_code, 0)

    def test_default_no_default_context(self):
        """Test info with no default context set in the contexts file"""

        # override patch return value
        self.mock__read_json.return_value = TEMPLATE

        result = self.runner.invoke(matatika, ["context",
                                               "info"])

        msg = "No default context is set\n" \
            "Set one using 'matatika context use' (see 'matatika context use --help')"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 0)

    #
    # use
    #
    def test_use(self):
        """Test use with a context name that exists in the contexts file"""

        context_name = 'context1'
        result = self.runner.invoke(matatika, ["context",
                                               "use",
                                               context_name])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_use_invalid_context_name(self):
        """Test use with a context name that does exist in the contexts file"""

        invalid_context_name = "invalid-context-name"
        result = self.runner.invoke(matatika, ["context",
                                               "use",
                                               invalid_context_name])

        self.assertIn(
            f"Context '{invalid_context_name}' does not exist", result.output)
        self.assertIs(result.exit_code, 0)

    #
    # update
    #
    def test_update_no_default_context(self):
        """Test update with no default context set in the contexts file"""

        # override patch return value
        self.mock__read_json.return_value = TEMPLATE

        result = self.runner.invoke(matatika, ["context",
                                               "update"])

        msg = "No default context is set\n" \
            "Set one using 'matatika context use' (see 'matatika context use --help')"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 0)

    def test_update_no_opts(self):
        """Test update with no options"""

        result = self.runner.invoke(matatika, ["context",
                                               "update"])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    #
    # delete
    #
    def test_delete(self):
        """Test delete with a context name that does exist in the contexts file"""

        context_name = 'context1'
        result = self.runner.invoke(matatika, ["context",
                                               "delete",
                                               context_name])

        self.assertNotIn(context_name, self.mock__read_json)
        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_delete_invalid_context_name(self):
        """Test delete with a context name that does not exist in the contexts file"""

        invalid_context_name = "invalid-context-name"
        result = self.runner.invoke(matatika, ["context",
                                               "delete",
                                               invalid_context_name])

        self.assertIn(
            f"Context '{invalid_context_name}' does not exist", result.output)
        self.assertIs(result.exit_code, 0)
