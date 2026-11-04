import os
import re
import subprocess
import shutil
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
SLIDES_DIR = PROJECT_DIR / "slides"
RENDER_ENV = os.environ.copy()
PYTHON_BIN_DIR = str(Path(sys.executable).resolve().parent)
RENDER_ENV["PATH"] = os.pathsep.join(
    [PYTHON_BIN_DIR, RENDER_ENV.get("PATH", "")]
)


def compress_pdf(pdf_file, dpi=150):
    temp_file = f"{pdf_file}.tmp"
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dPDFSETTINGS=/ebook",
        f"-r{dpi}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dDetectDuplicateImages",
        "-o",
        temp_file,
        pdf_file,
    ]
    try:
        subprocess.run(cmd, check=True, env=RENDER_ENV)
        os.rename(temp_file, pdf_file)
        print(f"PDF compressed to {dpi} dpi.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Compression error: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False


def run_decktape(slide_stem, compress=True):
    html_file = SLIDES_DIR / f"{slide_stem}.html"
    pdf_file = SLIDES_DIR / f"{slide_stem}.pdf"
    cmd = [
        "decktape",
        "reveal",
        "--fragments",
        str(html_file),
        str(pdf_file),
    ]
    try:
        subprocess.run(cmd, check=True, cwd=PROJECT_DIR, env=RENDER_ENV)
        print(f"PDF generated: {pdf_file.relative_to(PROJECT_DIR)}")
        return compress_pdf(pdf_file, dpi=150) if compress else True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def prepare_slide_bibliographies():
    """Refresh local bibliography copies so slides can be extracted alone."""
    target = SLIDES_DIR / "assets"
    target.mkdir(parents=True, exist_ok=True)
    for source in (PROJECT_DIR / "assets").glob("*.bib"):
        shutil.copy2(source, target / source.name)


def process_slide(slide_file):
    relative_file = slide_file.relative_to(PROJECT_DIR)
    print(f"Rendering {relative_file}...")
    result = subprocess.run(
        ["quarto", "render", str(relative_file)],
        cwd=PROJECT_DIR,
        env=RENDER_ENV,
    )

    if result.returncode != 0:
        print(f"Render failed: {relative_file}")
        return False

    return True


def find_slides(selectors):
    slide_files = sorted(SLIDES_DIR.glob("*.qmd"))
    if not selectors:
        return slide_files

    requested = {normalize_selector(selector) for selector in selectors}
    selected = [slide for slide in slide_files if normalize_selector(slide.stem) in requested]
    found = {normalize_selector(slide.stem) for slide in selected}
    missing = sorted(requested - found)

    if missing:
        print(
            f"Skipping missing presentation(s): {', '.join(missing)}."
        )

    return selected


def normalize_selector(selector):
    """Accept a class number or either the current or historical filename."""
    stem = Path(selector).stem
    match = re.fullmatch(r"(?:slides_)?(?:class|semaine)_(\d{1,2})", stem)
    if stem.isdigit():
        return f"{int(stem):02d}"
    if match:
        return f"{int(match.group(1)):02d}"
    return stem


def parse_args(args):
    """Read PDF and optional slide-selection arguments."""
    generate_pdf = True
    compress = True
    selectors = []

    for argument in args:
        if argument == "--no-pdf":
            generate_pdf = False
        elif argument == "--no-compress":
            compress = False
        else:
            selectors.append(argument)

    return generate_pdf, compress, selectors


def main(args=None):
    """Render the presentations and optionally export their PDFs."""
    if args is None:
        args = sys.argv[1:]

    generate_pdf, compress, selectors = parse_args(args)
    prepare_slide_bibliographies()

    slide_files = find_slides(selectors)
    rendered_slides = [slide for slide in slide_files if process_slide(slide)]

    if len(rendered_slides) != len(slide_files):
        raise SystemExit("At least one presentation failed to render.")

    if generate_pdf:
        pdf_results = [run_decktape(slide.stem, compress=compress) for slide in rendered_slides]
        if not all(pdf_results):
            raise SystemExit("At least one presentation PDF failed to render.")


if __name__ == "__main__":
    main()
