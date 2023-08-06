"""exceptions module"""

from dataclasses import dataclass


class MatatikaException(Exception):
    """Class to handle custom Matatika exceptions"""

    def __init__(self, message=None):

        super().__init__(message)
        self.message = message

    def __str__(self):

        return self.message


class NoDefaultContextSetError(MatatikaException):
    """Error to raise when no default context is set"""

    def __str__(self):

        msg = \
            "No default context is set\n" \
            "Set one using 'matatika context use' "\
            "(see 'matatika context use --help')"
        return msg


@dataclass
class ContextExistsError(MatatikaException):
    """Error to raise when a context exists"""

    name: str

    def __str__(self):

        msg = f"Context '{self.name}' already exists"
        return msg


@dataclass
class ContextDoesNotExistError(MatatikaException):
    """Error to raise when a context does not exists"""

    name: str

    def __str__(self):

        msg = f"Context '{self.name}' does not exist"
        return msg


@dataclass
class DefaultContextVariableNotSetError(MatatikaException):
    """Error to raise when a variable is not set in the default context"""

    variable: str

    def __post_init__(self):

        if self.variable == 'auth_token':
            self.command_override = "-a / --auth-token"
            self.set_variable_command = "matatika context update -a $AUTH_TOKEN"
        elif self.variable == 'endpoint_url':
            self.command_override = "-e / --endpoint-url"
            self.set_variable_command = "matatika context update -a $ENDPOINT_URL"
        elif self.variable == 'workspace_id':
            self.command_override = "-w / --workspace-id"
            self.set_variable_command = "matatika context update -w $WORKSPACE_ID"

    def __str__(self):

        msg = \
            f"Variable '{self.variable}' not set in the default context\n" \
            f"Use '{self.command_override}' to provide a one-time command override\n" \
            f"Use '{self.set_variable_command}' to set the variable in the default context"
        return msg


class WorkspaceNotFoundError(MatatikaException):
    """Class to raise an exception when a workspace is not found"""

    def __init__(self, endpoint_url, workspace_id):

        super().__init__()
        self.endpoint_url = endpoint_url
        self.workspace_id = workspace_id

    def __str__(self):

        msg = \
            f"Workspace {self.workspace_id} does not exist within the current authorisation " \
            f"context: {self.endpoint_url}"
        return msg


class DatasetNotFoundError(MatatikaException):
    """Class to raise an exception when a dataset is not found"""

    def __init__(self, dataset_id, endpoint_url):

        super().__init__()
        self.dataset_id = dataset_id
        self.endpoint_url = endpoint_url

    def __str__(self):

        msg = \
            f"Dataset {self.dataset_id} does not exist within the current authorisation " \
            f"context: {self.endpoint_url}"
        return msg
