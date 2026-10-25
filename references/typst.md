# Portable Typst output

Copy `assets/template/` from this skill into the reviewer's `template/` folder.
Import it relatively; no global package installation is needed. Preserve the
template's LICENSE with the copy. Do not import `@local/parulan` or assume CeTZ,
Tinymist, fonts, or a compiler are installed. Check the available Typst CLI first.

Initialize `reviewer.typ` with a short title and useful course/topic labels. Keep
workflow dates, people/source metadata, and provenance out of the PDF by default,
even when supplied for progress. Populate those optional fields only when the
user requests them:

```typst
#import "template/academic.typ": *
#show: reviewer.with(
  title: "Lesson reviewer",
  course: none,
  topic: none,
  date: none,
  instructor: none,
  author: none,
  sources: (),
  cover: false,
)
```

Replace the generic title when the topic is known. Use the default compact masthead (`cover: false`); a cover is opt-in for a
longer document. Keep metadata fields `none` and `sources: ()` by default.

## Components

Optional choices: `style: "visual"` or `style: "compact"`; default `"classic"`
preserves the previous layout. `profile: "tablet"` selects 180 x 240 mm portrait
with pen margin; default `"paper"` remains A4. `navigator: true` adds a linked
topic outline. Use headings for PDF bookmarks; inspect the actual navigation.
These are independent of Review/Reviewer and output selection. Read
[presentation.md](presentation.md) before designing explicit styles.

New units inherit the main body size (11.5 pt visual, 11 pt compact), rather than
the fixed small sizes of legacy callout/compare helpers. Prefer `study-unit` with
prose/diagrams or full-width `table.header` tables for learning pages, not long
legacy comparison boxes. Do not squeeze long content into an unbreakable unit.

| Component | Use |
|---|---|
| `#study-unit("Relationship")[...]` | heading attached to explanatory content; body may continue |
| `#study-figure(image("diagram.svg"), caption: [Interpretation])` | figure and readable caption kept together |
| `#note-lines(count: 2)` | annotation space |
| `#practice-pair([question], [answer], stacked: true)` | explicit full-width fallback for long question/answer pairs |

Use native shapes/grid/lines for original vector diagrams; label direction,
conditions and units. The medium should teach a relationship, not add decorations.
For practice generation and bank schema read [assessments.md](assessments.md).

| Component | Purpose |
|---|---|
| `#definition("Term")[...]` | precise definition |
| `#keypoint[...]` | essential takeaway |
| `#example[...]` | worked example |
| `#inpractice[...]` | practical connection |
| `#understanding[...]` | agreed learner interpretation; generic label by default |
| `#understanding(name: "Learner")[...]` | named label only when the learner supplies that preference |
| `#teacheranalogy[...]` | valid instructor analogy; exact attribution saved in progress |
| `#gotcha[...]` | common mistake |
| `#plain[...]` | requested explanation or demonstrated difficulty |
| `#recall[...]` | optional self-test, on request |
| `#compare("A", [a], "B", [b])` | short comparison |
| `#steps([first], [second])` | ordered process |
| `#flow([A], [B], [C], caption: [Process])` | short horizontal sequence |
| `#figbox(image("materials/lecture/media/image1.png", width: 90%), caption: [Transformation of the vector])` | source figure |
| `#hl[...]`, `#concept[...]` | selective emphasis |
| `#rvec(1, 4, 3)` | compact inline column vector |

Level-1 headings flow on the current page by default; use level 2 for short
subtopics. Set `section-breaks: true` only when chapter openings on new pages
help the requested document. Keep related short ideas together; do not add page
breaks merely because a new conversation part was approved. Preserve readable
font sizes and necessary worked steps; compact repetition and oversized boxes first.
Avoid tall inline matrix/vector math; use `rvec` or display math. Callouts are
unbreakable by default: split long ones logically or pass `breakable: true` to a
callout that supports it. Use vertical steps or tables for sequences too wide for
`flow`; long `compare` boxes also need another layout.

Use fenced, language-tagged code blocks. Escape Typst markup in literal source
text and keep code or OCR text in raw blocks; never evaluate untrusted source as
Typst code. The bundled template has no network package imports. An optional
external drawing package requires checking availability; simple diagrams can use
native shapes, flows, or tables without downloads.

## Compile and inspect

Prefer [verification.md](verification.md) and the bundled `verify-reviewer.py`
helper for fresh render folders, input fingerprints, and recorded inspection.
The commands below are a manual fallback; preserve the same evidence and status.

Run in the reviewer directory with an explicit working directory:

```text
typst compile reviewer.typ reviewer.pdf
typst compile reviewer.typ "page-{p}.png" --ppi 120
```

Check exit status and diagnostics. Inspect rendered PNGs with the host's image
viewer; the existence of a PDF is not a visual check. Check small labels, missing
glyphs, overflow, figure legibility, heading placement, and pagination. Remove
stale preview pages from earlier renders only within the known preview directory.

If the compiler is unavailable, preserve the approved `.typ` section and record
`written; compile pending`. If rendering/viewing is unavailable, record `compiled;
visual check pending`. Report the limitation and continue discussion if the learner
wants; don't claim verified pages or automatically install tools globally.
