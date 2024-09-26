import typer
from typing_extensions import Annotated
from enum import Enum

from airdrop import airdrop_monthly_alloc


class OutputType(str, Enum):
    table = "table"
    csv = "csv"
    json = "json"


app = typer.Typer()


@app.command()
def monthly_alloc(
    config: Annotated[typer.FileText, typer.Argument(help="Input config file.")],
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="Output file path. If skipped, output is printed on screen.",
        ),
    ] = None,
    type: Annotated[
        OutputType, typer.Option("--type", "-t", help="Output type.")
    ] = OutputType.table,
):
    """
    Compute the DHK dao monthly airdrop allocation based on staked value on various blockchains.
    """
    airdrop_monthly_alloc(config, output, type)


if __name__ == "__main__":
    app()
