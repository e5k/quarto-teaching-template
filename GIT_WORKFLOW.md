# Two-way updates with Git

The template and each course are independent repositories with ordinary local files. Use Git remotes to read the other repository, then cherry-pick a reviewed commit that changes shared functionality. There is no directory restructuring or synchronisation manager.

## Connections

Both courses have a `template` remote pointing at the central template folder. The template has `outils-info-2` and `analyse-geospatiale` remotes pointing at the courses. Outils informatique II keeps its existing GitHub `origin` unchanged. The other two repositories use local connections until their GitHub repositories are created.

These remotes exchange committed changes. They do not copy uncommitted edits. A normal push to GitHub only updates the repository you push; it does not update other courses.

## Make a shared feature commit

Work in either a course or the template. Inspect `git status --short`. Keep lesson edits and personal metadata out of the shared feature commit. Stage exact files or use `git add -p` for mixed files.

```sh
git diff -- _template.yml slides/_template.yml
git add -- slides/_template.yml slides/_extensions/course/author-links/
git diff --cached
git commit -m "Template: describe the shared feature"
git rev-parse HEAD
```

The staging paths above illustrate the profile-icons feature. Replace them with every file required by your actual change, including new plugin assets. Check the complete staged diff before committing. Git commits everything staged when no path arguments are supplied.

## Template to a course

In the destination course repository:

```sh
git fetch template
git log --oneline teaching-template-baseline-2026-11-04..template/main
git show COMMIT
git cherry-pick -x COMMIT
```

Replace COMMIT with the actual hash of the feature commit you inspected. The initial baseline is already present in the course: never cherry-pick the template's initial commit. Review each later commit before importing it. A later commit that changes the starter lesson or generic course metadata is not a shared feature commit.

## Course to template and onward

First commit only the reusable feature in the source course. In the central template:

```sh
git fetch outils-info-2
git log --oneline outils-info-2/main
git show COURSE_COMMIT
git cherry-pick -x COURSE_COMMIT
git rev-parse HEAD
```

Use `analyse-geospatiale` instead of `outils-info-2` when that is the source. Then fetch `template` in each other course and cherry-pick the resulting template commit. Cherry-pick creates a new hash; `-x` records the original hash in the commit message.

Do not re-import the same feature into the source course. It already contains the change. A commit that mixes a lesson and a shared feature should be split in the source repository first; do not cherry-pick the whole mixed commit.

## Local changes and conflicts

Use a clean working tree for an import. Commit work you want to keep in its own course commit first. If you prefer to set it aside temporarily, `git stash push -u -m "Before template update"` also includes untracked files; restore it with `git stash pop` after the import and resolve any reported conflicts. A stash is local, not a remote backup.

If cherry-pick reports a conflict, inspect `git status`, edit the conflicting files, stage the resolved files and run `git cherry-pick --continue`. To abandon that import, use `git cherry-pick --abort`. Do not resolve conflicts by replacing all course files with the template copy.

Do not merge or pull an entire course branch into the template. Those branches also contain chapters, bibliography paths and other local settings. Import the individual feature commits.

## Validate an imported feature

Review `git show --stat HEAD` and the changed content, then render a relevant chapter and slide deck. Check both answer/question profiles for profile changes, and extract slides for portability changes. Push each repository to its own GitHub origin when you intend to publish its history.

## Baseline and existing work

Setup created a shared-files baseline commit in each course and an initial template commit. In Outils informatique II only the shared files were committed; existing lesson edits, configuration changes, bibliography deletion and rendered changes remained uncommitted. Analyse géospatiale initially tracks only the shared files: its course content, personal YAML and planning files remain untracked until deliberately added. Review data sizes and distribution rights before adding planning datasets.

The tag `teaching-template-baseline-2026-11-04` identifies the template's initial commit and is available in both courses. It is a history marker, not a lock file or a synchronisation mechanism.

## Files shared at setup

The following 53 files matched byte for byte in all three folders. New reusable files can be included in later feature commits. Course `_quarto.yml` files, lessons, bibliographies, data and personal metadata are excluded.

- `_extensions/coatless-quarto/custom-callout/_extension.yml`
- `_extensions/coatless-quarto/custom-callout/assets/css/fontawesome.css`
- `_extensions/coatless-quarto/custom-callout/assets/webfonts/fa-solid-900.woff2`
- `_extensions/coatless-quarto/custom-callout/customcallout.lua`
- `_extensions/coatless-quarto/custom-callout/fa.lua`
- `_extensions/quarto-ext/fontawesome/_extension.yml`
- `_extensions/quarto-ext/fontawesome/assets/LICENSE.txt`
- `_extensions/quarto-ext/fontawesome/assets/css/all.css`
- `_extensions/quarto-ext/fontawesome/assets/css/all.min.css`
- `_extensions/quarto-ext/fontawesome/assets/css/latex-fontsize.css`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-brands-400.ttf`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-brands-400.woff2`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-regular-400.ttf`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-regular-400.woff2`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-solid-900.ttf`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-solid-900.woff2`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-v4compatibility.ttf`
- `_extensions/quarto-ext/fontawesome/assets/webfonts/fa-v4compatibility.woff2`
- `_extensions/quarto-ext/fontawesome/fontawesome.lua`
- `_quarto-answer.yml`
- `_quarto-question.yml`
- `_template.yml`
- `assets/book-index-link.html`
- `assets/bulletin-of-volcanology.csl`
- `assets/custom.css`
- `assets/dark.scss`
- `assets/plots.mplstyle`
- `assets/theme-toggle.html`
- `assets/webex.css`
- `assets/webex.js`
- `scripts/notebook-links.lua`
- `scripts/render_all.py`
- `scripts/render_notebooks.py`
- `scripts/render_slides.py`
- `slides/_extensions/course/author-links/_extension.yml`
- `slides/_extensions/course/author-links/author-links.lua`
- `slides/_extensions/fradav/animate/_extension.yml`
- `slides/_extensions/fradav/animate/animate.lua`
- `slides/_extensions/fradav/animate/js-yaml.min.js`
- `slides/_extensions/fradav/animate/plugin.js`
- `slides/_extensions/fradav/animate/svg.min.js`
- `slides/_extensions/grantmcdermott/clean/_extension.yml`
- `slides/_extensions/grantmcdermott/clean/clean.scss`
- `slides/_extensions/grantmcdermott/clean/mathjax-config.js`
- `slides/_extensions/martinomagnifico/verticator/_extension.yml`
- `slides/_extensions/martinomagnifico/verticator/verticator.css`
- `slides/_extensions/martinomagnifico/verticator/verticator.js`
- `slides/_template.yml`
- `slides/assets/after-body.html`
- `slides/assets/bulletin-of-volcanology.csl`
- `slides/assets/js/same-title-counter.js`
- `slides/assets/plots.mplstyle`
- `slides/mathjax-config.js`

## Native Git reference

- https://git-scm.com/docs/git-cherry-pick
- https://git-scm.com/docs/git-fetch
- https://git-scm.com/docs/git-remote


## GitHub publication added on 4 November 2026

The central template is now published at https://github.com/e5k/_quarto-teaching-template. The template repository has that URL as `origin`; both courses use it as their `template` remote. The template’s course-source remotes still point to the local course repositories. The repository is public, and its documentation is automatically published at https://e5k.github.io/_quarto-teaching-template/ by `.github/workflows/publish-docs.yml`.
