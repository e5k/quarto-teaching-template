"""Render the weekly Quarto chapters as clean, unexecuted notebooks."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = PROJECT_DIR / "course"
WEEK_PATTERN = re.compile(r"(?:class|semaine)_\d{2}\.qmd$")


def weekly_chapters() -> list[Path]:
    """Return numbered weekly chapters, excluding block introductions."""
    return sorted(
        path
        for path in COURSE_DIR.glob("*.qmd")
        if WEEK_PATTERN.fullmatch(path.name) and normalize_selector(path.stem) != "01"
    )


def normalize_selector(selector):
    """Accept a class number or either the current or historical filename."""
    stem = Path(selector).stem
    match = re.fullmatch(r"(?:slides_)?(?:class|semaine)_(\d{1,2})", stem)
    if stem.isdigit():
        return f"{int(stem):02d}"
    if match:
        return f"{int(match.group(1)):02d}"
    return stem


def select_chapters(selectors: list[str]) -> list[Path]:
    """Select weekly chapters from optional week numbers or filenames."""
    chapters = weekly_chapters()
    if not selectors:
        return chapters

    requested = {normalize_selector(selector) for selector in selectors}
    selected = [chapter for chapter in chapters if normalize_selector(chapter.stem) in requested]
    found = {normalize_selector(chapter.stem) for chapter in selected}
    missing = sorted(requested - found)

    if missing:
        available = ", ".join(chapter.stem for chapter in chapters)
        raise SystemExit(
            f"Unknown notebook chapter(s): {', '.join(missing)}. "
            f"Available chapters: {available}"
        )

    return selected


def clean_markdown(source: str) -> str:
    """Remove Quarto-only wrappers that are not useful inside Jupyter."""
    source = re.sub(r"\A---\n.*?\n---\n*", "", source, flags=re.DOTALL)
    source = re.sub(r"\{\{<\s*fa\s+[^>]+>\}\}\s*", "", source)
    source = re.sub(r"\{\{<\s*pagebreak\s*>\}\}", "", source)

    lines: list[str] = []
    for line in source.splitlines():
        if re.match(r"^\s*:::\s*(?:\{.*\})?\s*$", line):
            continue
        if line.startswith("#"):
            line = re.sub(r"\s+\{[^{}]*\}\s*$", "", line)
        line = re.sub(r"\)\{[^{}\n]*\}", ")", line)
        lines.append(line)

    return "\n".join(lines).strip() + "\n"


def clean_notebook(path: Path) -> None:
    """Remove outputs, execution state, cell options and UI-only markup."""
    notebook = json.loads(path.read_text(encoding="utf-8"))

    for cell in notebook.get("cells", []):
        source = "".join(cell.get("source", []))

        if cell.get("cell_type") == "markdown":
            source = clean_markdown(source)
        elif cell.get("cell_type") == "code":
            source = "\n".join(
                line
                for line in source.splitlines()
                if not line.lstrip().startswith("#|")
            ).rstrip() + "\n"
            cell["execution_count"] = None
            cell["outputs"] = []

        cell["source"] = source.splitlines(keepends=True)
        cell["metadata"] = {}

    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    }

    path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def render_notebook(source: Path) -> None:
    """Convert one QMD chapter next to its HTML output."""
    output = source.with_suffix(".ipynb")
    print(f"Rendering {source.relative_to(PROJECT_DIR)} as a notebook...")
    subprocess.run(
        [
            "quarto",
            "convert",
            str(source.relative_to(PROJECT_DIR)),
            "--output",
            str(output),
        ],
        cwd=PROJECT_DIR,
        check=True,
    )
    clean_notebook(output)


def main(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    chapters = select_chapters(args)
    if not chapters:
        raise SystemExit("No weekly chapters were found.")

    for chapter in chapters:
        render_notebook(chapter)

    print(f"Generated {len(chapters)} clean notebook(s).")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from error
