# Teaching blocks and chapter numbering

This guide describes the existing HTML book structure supported by the shared Quarto teaching template. It does not introduce a new template layer or change the course's configuration. See the [full book guide](https://e5k.github.io/quarto-teaching-template/book-guide.html#book-structure) for detailed examples and the [getting-started guide](https://e5k.github.io/quarto-teaching-template/getting-started.html#filenames) for build-script constraints.

## Separate the page's role from its filename

The book configuration in root `_quarto.yml` defines the order and role of its content. A teaching block is a **part**. Its introduction can be a QMD file containing objectives, context, prerequisites and links. Classes listed under that part's `chapters` are **chapters**.

In the HTML book:

| Role | Numbering | Where it is defined |
|---|---|---|
| Course overview or welcome page | Unnumbered when its heading uses `.unnumbered`, or when configured as a part landing page | `index.qmd` and its entry in the book configuration |
| Teaching-block introduction | No chapter number; does not consume a chapter position | A QMD file used as `part:` |
| Class or substantial topic | A chapter number in reading order | An entry under `chapters:` |
| Optional supporting page | Unnumbered when explicitly marked `.unnumbered`; does not consume a chapter number | Its heading and chapter entry |
| Appendix | Lettered separately, A, B, etc. | `book.appendices` |
| References page | Unnumbered when explicitly marked `.unnumbered` | Its heading and book entry |

The role comes from the configuration, not from `_intro`, a numeric prefix, a directory name or a displayed word such as “Week”. An introductory filename does not automatically make a page unnumbered. Conversely, an introduction used as `part:` does not need a special filename.

## Define parts and chapters

```yaml
book:
  chapters:
    - index.qmd
    - part: course/exploring-introduction.qmd
      chapters:
        - course/reading-data.qmd
        - course/describing-data.qmd
    - part: course/inference-introduction.qmd
      chapters:
        - course/sampling.qmd
        - course/comparing-groups.qmd
  appendices:
    - appendices/reference-sheet.qmd
    - appendices/references.qmd
```

Assuming the welcome and references headings are marked unnumbered, the main chapter sequence is Reading data **1**, Describing data **2**, Sampling **3**, Comparing groups **4**. Both block-introduction pages remain unnumbered. The second part does not reset the chapter sequence. The reference sheet is Appendix A.

A part can instead be a label without an introduction page:

```yaml
- part: "Statistical inference"
  chapters:
    - course/sampling.qmd
    - course/comparing-groups.qmd
```

Use a file-valued part when the block needs content of its own. List each page only once: adding the same introduction under `chapters` as well as `part` does not create a second independent role for it.

## Keep titles and references stable

For a normal chapter, use either a YAML title or a top-level heading:

```markdown
# Reading data {#sec-reading-data}

## Inspect the observations
```

The current shared template enables HTML section numbering. For chapter 1, the subsection above becomes 1.1. An explicit identifier such as `sec-reading-data` stays meaningful when the chapter moves. Refer to a numbered chapter or section with `@sec-reading-data`; Quarto resolves its current number.

Do not manually prefix a chapter title with its generated number. A teaching-session label such as “Week 3” is separate scheduling information; it need not equal chapter 3.

For an explicitly unnumbered page:

```markdown
# Optional notes {.unnumbered}
```

For references:

```markdown
# References {.unnumbered}

::: {#refs}
:::
```

Use ordinary source links for an unnumbered introduction, for example `[Block overview](exploring-introduction.qmd)` from a chapter in the same directory. Do not rely on chapter-based figure or table cross-reference numbering inside unnumbered pages; keep numbered analytical material in chapters.

## What is flexible today

Quarto accepts descriptive chapter and introduction filenames when they are listed in `_quarto.yml`. The book order follows that list, not alphabetical order or a filename's digits. Optional subdirectories organise files but do not automatically create parts.

The current build scripts have narrower rules:

| Build path | Current behaviour |
|---|---|
| Native `quarto render` for the book | Uses the explicit book structure, including arbitrary listed QMD filenames |
| Native slide rendering | Uses the slide project; filenames must be covered by its `project.render` entries |
| `render_slides.py` | Discovers top-level `slides/*.qmd`; selectors can use matching stems or recognised class numbers |
| `render_notebooks.py` | Discovers only top-level `course/class_XX.qmd` and `course/semaine_XX.qmd`, and excludes number 01 |
| `render_all.py` | Calls the slide and notebook builders before rendering the whole book; inherits their limitations |

Therefore, arbitrary book filenames already work, but arbitrary notebook-source names, nested notebook discovery, a configurable first-class exclusion and explicit chapter-to-deck mappings are **not implemented**. There is no supported `slides:` or `notebook:` mapping field to add to a chapter yet. Keep the current numbered filenames when using the existing notebook pipeline, or render the book directly if it has no generated-notebook requirement.

## What is visible in navigation

The shared `assets/custom.css` hides chapter-number spans in the left sidebar. This is a display choice: chapter numbers still exist in page headings, section numbers and cross-references. It does not turn chapters into unnumbered pages.

Book parts, page numbering and repeated slide-title counters are separate features. `repeated-slide-titles` affects presentation heading suffixes only; it has no effect on book chapters.

This guide's numbering convention is verified for the current HTML book. Other output formats handle parts differently; check their output separately before assuming the same presentation.

## Apply this to an existing course

Preserve the local root `_quarto.yml`: its parts, chapter order, bibliography and resource paths belong to the course. Reuse `_template.yml` and companion assets for appearance and functionality. No runtime template change is needed to obtain unnumbered part introductions with numbered classes; it is already native Quarto behaviour.

Reordering the book does not require renaming source files. After an intentional reorganisation, render the book and check chapter titles, cross-references, page navigation and links. Also review slide/notebook associations maintained in the content, since the current scripts do not infer those from the book structure.
