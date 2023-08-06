import typer
from typing import Optional, List
from pathlib import Path

from ddot import lib
from devinstaller_core import exception as e

app = typer.Typer()

DEFAULT_SPEC_FILE = "devfile.toml"
DEFAULT_PROG_FILE = "devfile.py"


def goodbye() -> None:
    """Final callback function. Runs after the end of everything."""
    typer.secho("\nBye. Have a good day.", fg="green")


# @app.command()
# def install(
#     spec_file: Optional[Path] = typer.Option(DEFAULT_SPEC_FILE),
#     platform: Optional[str] = None,
#     module: Optional[str] = None,
# ) -> None:
#     """Install the default group and the modules which it requires"""
#     try:
#         req_list = [module] if isinstance(module, str) else None
#         d = lib.Devinstaller()
#         d.install(
#             spec_file_path=f"file: {spec_file}",
#             platform_codename=platform,
#             requirements_list=req_list,
#         )
#     except e.DevinstallerBaseException as err:
#         typer.secho(str(err), fg="red")


@app.command()
def show(spec_file: Optional[Path] = typer.Option(DEFAULT_SPEC_FILE)) -> None:
    """Show all the groups and modules available for your OS"""

    d = lib.Devinstaller()
    d.show(spec_file_path=f"file: {spec_file}",)


@app.command()
def run(
    module: Optional[List[str]] = typer.Option(None, "--module", "-m"),
    spec_file: Optional[Path] = typer.Option(DEFAULT_SPEC_FILE),
):
    """Run commands"""

    req_list = list(module)
    d = lib.Devinstaller()
    d.install(
        spec_file_path=f"file: {spec_file}",
        platform_codename=None,
        requirements_list=req_list,
    )


def main():
    try:
        app()
    except e.DevinstallerBaseException as err:
        typer.secho(str(err), fg="red")
    finally:
        goodbye()


if __name__ == "__main__":
    main()
