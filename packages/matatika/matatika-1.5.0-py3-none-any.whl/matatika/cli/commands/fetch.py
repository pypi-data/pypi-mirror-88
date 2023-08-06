"""CLI 'fetch' command"""


import click
from matatika.cli.utility import Resolver
from matatika.types import DataFormat
from .root import matatika


@matatika.command("fetch", short_help="Fetch the data from a dataset")
@click.pass_context
@click.argument("dataset-id", type=click.UUID)
@click.option("--output-file", "-f", type=click.Path(writable=True), help="Output file path")
def fetch(ctx, dataset_id, output_file):
    """Fetch the data from a dataset"""

    client = Resolver(ctx).client(workspace_id=None)
    data = client.fetch(dataset_id, data_format=DataFormat.RAW)

    if output_file:
        with open(output_file, "w") as file_:
            file_.write(data)
        click.secho(f"Dataset {dataset_id} data successfully written to {output_file}",
                    fg='green')

    else:
        click.secho(f"*** START DATASET {dataset_id} DATA CHUNK STDOUT DUMP ***",
                    err=True,  fg='yellow')
        click.echo(data)
        click.secho(f"*** END DATASET {dataset_id} DATA CHUNK STDOUT DUMP ***",
                    err=True,  fg='yellow')
