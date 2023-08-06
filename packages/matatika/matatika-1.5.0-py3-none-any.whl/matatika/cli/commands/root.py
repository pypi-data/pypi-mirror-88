"""CLI entrypoint 'matatika' command"""

import click
import jwt
import pkg_resources
import requests
from matatika.exceptions import MatatikaException

version = pkg_resources.require("matatika")[0].version


class ExceptionHandler(click.Group):
    """CLI entrypoint and error handling"""

    def invoke(self, ctx):
        """Invoke method override"""

        try:
            return super().invoke(ctx)

        except MatatikaException as err:
            click.secho(str(err), fg='red')

        except jwt.exceptions.DecodeError as err:
            msg = repr(err) + \
                "\nPlease check your authentication token is correct and valid"
            click.secho(msg, fg='red')

        except requests.exceptions.HTTPError as err:
            msg = repr(err) + \
                "\nPlease check your authentication token has not expired and the correct " \
                "endpoint is specified"
            click.secho(msg, fg='red')


@click.group(cls=ExceptionHandler)
@click.pass_context
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--endpoint-url", "-e", help="Endpoint URL")
@click.option("--trace", "-t", is_flag=True, help="Trace variable sources")
@click.version_option(version=version)
def matatika(ctx, auth_token, endpoint_url, trace):
    """CLI entrypoint and base command"""

    ctx.ensure_object(dict)

    ctx.obj['auth_token'] = auth_token
    ctx.obj['endpoint_url'] = endpoint_url
    ctx.obj['trace'] = trace
