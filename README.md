# Quarto teaching template for books and presentations

## Overview

Each course and the template can be independent Git repositories. Template files are **copied into each course**, so rendering does not depend on files outside the repository.

The YAML files separate course-specific information in `_quarto.yml` from reusable appearance and functionality in `_template.yml`. Quarto combines them using its native `metadata-files` mechanism.

There is no Python synchronisation manager, manifest, lock file, `_teaching/` directory, submodule or subtree. For the current two-way Git workflow using remotes and selected feature commits, see [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

## Standard structure

```text
my-course/
├── _quarto.yml                 ← course-specific settings
├── _template.yml               ← shared book settings
├── _quarto-answer.yml
├── _quarto-question.yml
├── index.qmd
├── assets/                     ← styles, web scripts, CSL and bibliography
├── _extensions/                ← book extensions
├── scripts/                    ← teaching-material build scripts
├── course/
│   ├── class_01.qmd
│   └── class_02.qmd
└── slides/
    ├── _quarto.yml             ← course-specific presentation settings
    ├── _template.yml           ← reusable slide theme and plugins
    ├── _extensions/            ← clean, animate, verticator, etc.
    ├── assets/
    ├── mathjax-config.js
    └── slides_class_01.qmd
```

`course/` and `slides/` are the two main content folders, following the structure of *Outils informatique II*. Appendices, images, data and planning documents can remain in their own directories. Quarto generates `_book/`, `.quarto/` and rendered output files.

## Configuration responsibilities

| File | Course-specific information | Shared settings |
|---|---|---|
| `_quarto.yml` | Title, author, GitHub URL, chapters, appendices, bibliography, course resources and Python kernel | Loads `_template.yml` using `metadata-files` |
| `_template.yml` | No course title, chapter list or course-specific BibTeX filename | Light/dark themes, CSS/JS, filters, callouts, generic navigation, language and rendering options |
| `slides/_quarto.yml` | Author, bibliography and presentation selection | Loads the `_template.yml` inside `slides/` |
| `slides/_template.yml` | No course title or BibTeX filename | The clean-revealjs format, animations, plugins, layout, resources and filters |

Each `_quarto.yml` includes:

```yaml
metadata-files:
  - _template.yml
```

Keep changes that apply to only one course in its local configuration or the relevant document, so the `_template.yml` files remain reusable. Check the effective metadata when overriding shared values, especially list settings. The documentation uses directory-level `_metadata.yml` for its language and comment overrides after loading the shared template.

The `slides/` subproject explicitly declares `project: type: default` to load its own configuration and metadata. The book retains `project: type: book`.

## Bibliography filenames are course-specific

All BibTeX files belong in **`assets/`**, but the template does not impose a filename.

Current examples:

- *Analyse géospatiale*: `assets/geospatial.bib`.
- *Outils informatique II*: `assets/OI2.bib`.

The book declares its bibliography path in the root `_quarto.yml`. Slides declare their local copy, for example `assets/geospatial.bib`, in `slides/_quarto.yml`; that path refers to `slides/assets/geospatial.bib`. Neither `_template.yml` contains a `bibliography` key.

In the starter template, `assets/references.bib` is only an example to rename when creating a course. Never overwrite a course bibliography when updating the template.

Zotero manages synchronised bibliographies; do not edit their entries manually. When a reference needs to be added, provide its BibTeX in the conversation for import into Zotero.

## Transfer changes from the template to a course

### Create a new course

Copy the starter files, then personalise both `_quarto.yml` files: title, chapter organisation, bibliography, authors and repository URL. Add content to `course/` and `slides/`. Exclude the template's `.git/` directory when creating an independent course repository.

### Update an existing course

1. Compare the shared `_template.yml` files for the book and slides.
2. Transfer the styles, scripts, filters or extensions required by the new feature, together with its YAML changes.
3. **Preserve the local `_quarto.yml` files**, bibliographies, data and lesson content.
4. Review the Git diff, render a chapter and a presentation, then commit the update.

A new plugin often requires a YAML change **and** its directory under `_extensions/`. Copying only the YAML declaration is insufficient. Use the reviewed feature-commit procedure in [GIT_WORKFLOW.md](GIT_WORKFLOW.md) to transfer changes between the connected repositories.

## Transfer changes from a course to the template

When improving a reusable feature in a course, edit the corresponding shared files: `_template.yml`, styles, filters, scripts or extensions. Titles, BibTeX filenames and other local information belong in `_quarto.yml` and should stay with the course.

1. Check that the change is reusable across courses.
2. Review the diff, for example:

   ```sh
   git diff -- _template.yml slides/_template.yml
   ```

3. Transfer the relevant changes and their dependencies into the template repository.
4. Review and commit the diff there.
5. Propagate the improvement to the other courses that need it.

`git add -p` lets you select individual hunks to commit when several changes have been mixed together. Keeping local and generic settings in separate YAML files makes that distinction easier to maintain.

This workflow works **in both directions**, through deliberately selected changes. Git provides history, review and merging. The configured remotes and `git cherry-pick -x` let you transfer individual feature commits. The build scripts do not push course source commits to GitHub; the combined script offers a separate publication prompt for the rendered book.

## File naming

| Material | Convention |
|---|---|
| Chapter | `course/class_01.qmd` |
| Presentation | `slides/slides_class_01.qmd` |
| Notebook | `course/class_01.ipynb` |

Use two digits and the same number for all three materials. Displayed titles may contain spaces and accents; source filenames avoid them.

The historical names `course/semaine_04.qmd` and `slides/slides_semaine_04.qmd` remain supported. The scripts do not require renaming existing *Outils informatique II* files.

## Build materials as in Outils informatique II

The scripts are ordinary local files and locate the project relative to their own location. They are portable across courses and do not depend on the central template directory.

With the appropriate Python environment active, run these commands from a course directory:

```sh
# Book preview and existing profiles
quarto preview
quarto render --profile answer
quarto render --profile question

# One presentation without executing code cells
quarto render slides/slides_class_04.qmd --no-execute

# Presentations and notebooks: select by number or filename
python scripts/render_slides.py 4 --no-pdf
python scripts/render_notebooks.py 4

# Existing build workflow: slides, notebooks, then the book
python scripts/render_all.py --no-pdf
```

The rendering scripts do not synchronise templates. `render_all.py` preserves the *Outils informatique II* workflow, including its final publication prompt: confirm only when you intend to publish. PDF generation requires Decktape; compression also requires Ghostscript. Use `--no-pdf` to skip those steps.

The first class has no practical and is excluded from notebook generation. `quarto convert` produces unexecuted notebooks; book profiles do not filter their source content.

## One book with the existing profiles

`_quarto-answer.yml` and `_quarto-question.yml` come from *Outils informatique II*. The same project is rendered with the selected profile, rather than maintaining separate teacher and student books.

Written answers can use `.content-visible when-meta="answers"`. Document-level overrides take precedence according to Quarto's metadata rules.

## GitHub and independent builds

Commit the configuration, styles, filters, extensions and scripts alongside the course sources. Do not ignore the `_extensions/` directories required for rendering. A course clone then contains its template dependencies without requiring the central folder, a Python template manager or special Git subproject retrieval.

Quarto, Python dependencies and required data must still be installed or supplied. Web resources and GEE services may require internet access. Git remotes and publication are configured as described in [GIT_WORKFLOW.md](GIT_WORKFLOW.md) and the publication section below; no submodule or subtree is used.

## Technical references

- [Shared Quarto metadata](https://quarto.org/docs/projects/quarto-projects.html)
- [Managing extensions and tracking them in Git](https://quarto.org/docs/extensions/managing.html)

## Extract slides as a standalone project

The `slides/` directory can be copied on its own: it contains its YAML files, `_extensions/`, assets, CSL and local bibliography copies. Data and styles used by code must also be present, with paths that stay inside the copied folder.

Bibliography filenames remain course-specific, including under `slides/assets/`. `render_slides.py` refreshes these copies from the course's root `assets/` exports before rendering. After a Zotero update, run this script to refresh the copy before extracting the folder; a direct `quarto preview` uses the local copy already present. For a standalone talk, export its bibliography directly into its own `assets/` directory.

From the extracted folder, `quarto preview` works without the course repository. Copy **the entire folder**, including any required `assets/`, `data/`, `img/` and `_extensions/` directories; the QMD file alone is insufficient.

Links to course pages are reading links and are not required to build the deck. If publishing the deck at another address, update those links to the published course pages where necessary.

## Repeated slide titles

Repeated headings are numbered by default, for example `Terrain (1/3)`. To leave their text unchanged, add this top-level setting to `slides/_quarto.yml` or the front matter of a single presentation:

```yaml
repeated-slide-titles: false
```

The reusable implementation includes the `course/slide-options` filter, its extension directory and `slides/assets/after-body.html`. Link handling remains enabled when title numbering is disabled.

## Profile icons on the title slide

In `slides/_quarto.yml`, the optional `author-links` block defines `researchgate`, `github`, `scholar` and `website` using their full URLs. The icons appear after the first author's ORCID icon; only configured links are displayed. ORCID remains part of the author's standard metadata. The generic template provides commented examples to complete.

Existing URL-only settings remain supported. For additional control:

```yaml
author-links:
  enabled: true
  orcid: true
  order: "github, scholar, researchgate, website"
  github: https://github.com/your-account
  scholar:
    url: https://scholar.google.com/citations?user=YOUR_ID
    enabled: false
  researchgate: false
  website: https://example.org
```

Set a service to `false` to hide it, or use `url` and `enabled` to retain its URL while it is hidden. `order` selects and orders the optional links. `enabled: false` hides all optional links; add `orcid: false` to hide the native ORCID icon too. A bare `author-links: false` disables the custom feature and leaves native ORCID unchanged. Use YAML booleans, not quoted strings.

The reusable implementation is the `course/author-links` filter declared in `slides/_template.yml`, together with `slides/_extensions/course/author-links/`. Personal URLs remain in `_quarto.yml`. The filter uses Font Awesome, already loaded by the presentation theme. When transferring the feature, include both the declaration and its extension directory. The `slides/` folder remains self-contained.

## Template documentation

[Read the documentation](https://e5k.github.io/quarto-teaching-template/) · [GitHub repository](https://github.com/e5k/quarto-teaching-template)

The documentation website starts at [doc/index.qmd](doc/index.qmd). Its four guides cover getting started, books, presentations and maintenance, including local features, examples and the two-way Git workflow.

From `doc/`, run `quarto preview` to browse it or `quarto render` to rebuild the website in `doc/_site/`. The documentation project is independent of the course book. Pre-rendered slide demonstrations live under `doc/assets/demos/slides/` and must be regenerated when the slide theme changes.

### Publish with GitHub Pages

The public repository is [e5k/quarto-teaching-template](https://github.com/e5k/quarto-teaching-template), and the documentation is published at [e5k.github.io/quarto-teaching-template](https://e5k.github.io/quarto-teaching-template/). The `.github/workflows/publish-docs.yml` workflow rebuilds only the `doc/` project after a push to `main` that changes that directory. It updates the `gh-pages` branch, then deploys the same website with GitHub Pages. The workflow can also be started manually from Actions. Generated `doc/_site/` files remain excluded from `main`.

To publish documentation that has already been rendered, run `quarto publish gh-pages doc --no-render --no-browser`. Omit `--no-render` to include rendering.
