from typing import Optional

import typer

from invisible_hand.ensures import ensure_client_secret_json_exists


def dev(
    org: Optional[str] = typer.Option(None, help="Last name of person to greet."),
    age: str = typer.Option("", help="Some help message"),
):
    ensure_client_secret_json_exists()
    print("nice")
