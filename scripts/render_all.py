"""Build every artifact required before publishing the Quarto book.

Use --no-compress to skip PDF compression, keeping the usual PDF filenames.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"
RENDER_ENV = os.environ.copy()
PYTHON_BIN_DIR = str(Path(sys.executable).resolve().parent)
RENDER_ENV["PATH"] = os.pathsep.join(
    [PYTHON_BIN_DIR, RENDER_ENV.get("PATH", "")]
)


def run_script(script_name: str, arguments: list[str] | None = None) -> None:
    """Run one build script with the current Python interpreter."""
    command = [sys.executable, str(SCRIPTS_DIR / script_name)]
    if arguments:
        command.extend(arguments)

    subprocess.run(
        command,
        cwd=PROJECT_DIR,
        check=True,
        env=RENDER_ENV,
    )


def render_book() -> None:
    """Render the complete book after all downloadable resources exist."""
    subprocess.run(
        ["quarto", "render"],
        cwd=PROJECT_DIR,
        check=True,
        env=RENDER_ENV,
    )


def confirm_publish() -> bool:
    """Ask whether the completed book should be published to GitHub Pages."""
    try:
        response = input(
            "\nPublish the website to GitHub Pages now? [y/N] "
        )
    except EOFError:
        return False

    return response.strip().lower() in {"y", "yes", "o", "oui"}


def publish_book() -> None:
    """Publish the already rendered book without rebuilding it."""
    subprocess.run(
        ["quarto", "publish", "gh-pages", "--no-render"],
        cwd=PROJECT_DIR,
        check=True,
        env=RENDER_ENV,
    )


def main(args: list[str] | None = None) -> None:
    """Render slides, notebooks and finally the complete book."""
    if args is None:
        args = sys.argv[1:]

    week_selectors = [argument for argument in args if not argument.startswith("--")]

    print("\n[1/3] Rendering presentations...")
    run_script("render_slides.py", args)

    print("\n[2/3] Rendering notebooks...")
    run_script("render_notebooks.py", week_selectors)

    print("\n[3/3] Rendering the book...")
    render_book()

    print("\nBuild complete.")

    if confirm_publish():
        print("\nPublishing to GitHub Pages...")
        publish_book()
        print("\nPublication complete.")
    else:
        print("Publication skipped.")
        print("Publish later with:")
        print("quarto publish gh-pages --no-render")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from error
