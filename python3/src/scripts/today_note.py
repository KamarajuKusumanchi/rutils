#! /usr/bin/env python3
"""Create a note for today."""

# Script to create a file with today's date yyyy-mm-dd.txt and fill it with
# some content if such a file does not already exist and then open it in vim.
# If the file already exists, just open it in vim.
from pathlib import Path
import subprocess
from datetime import date

import typer

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
)

def create_or_open_note(directory: Path, editor: str):
    """Create today's note file if it doesn't exist, then open it in the editor."""
    # Get today's date in yyyy-mm-dd format
    date_str = date.today().isoformat()
    filepath = directory / f"{date_str}.txt"

    # If the file does not exist, create it with some content.
    if not filepath.exists():
        with open(filepath, "w") as f:
            f.write("-" * 80 + "\n")
            f.write(f"today | {date_str}\n")
            f.write("-" * 80 + "\n")
        typer.echo(f"Created {filepath}")
    else:
        typer.echo(f"Opening existing note: {filepath}")

    # Open in vim
    subprocess.run([editor, str(filepath)])

@app.command()
def main(
    directory: Path = typer.Option(
        Path("."),
        "--dir", "-d",
        help="Directory where the note file will be created.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
    editor: str = typer.Option(
        "vim",
        "--editor", "-e",
        help="Editor to open the note with.",
    ),
):
    """Create a note for today."""
    create_or_open_note(directory, editor)


if __name__ == "__main__":
    app()
