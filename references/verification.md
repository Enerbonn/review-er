# Verify the actual rendered output

Use the website screenshot-review principle: create the output, render/open it,
inspect what the user will see, fix concrete problems, and inspect again. A
compiler exit code or screenshot file existing is only a technical check; the
agent must actually view the image.

## PDF evidence workflow

The helper uses Python's standard library and an available Typst CLI. It writes
fresh PDF/PNG artifacts and a fingerprinted report for each run. Use absolute
skill/source paths with an explicit working directory:

```text
python <skill>/scripts/verify-reviewer.py build <reviewer>/reviewer.typ
```

1. Check exit status and `verification/<run>/verification.json`. A failed build is
   recorded as failed; an earlier PDF does not prove the new source compiled.
2. Open generated `page-*.png` files with the host's image viewer. After appending,
   inspect the new section and earlier pages affected by reflow. Inspect every
   page for the final handoff. Render at higher resolution or zoom for small
   math, code, or diagram labels.
3. Check clipping, overflow, heading placement, callout splits, table widths,
   page order, missing glyphs, code indentation, equation symbols, diagram labels,
   and captions. Check content against the approved discussion and source evidence.
   Compare source and output visuals; name mismatches rather than saying "looks good".
4. Fix the source or teaching aid without regenerating unrelated approved sections.
   Rebuild and inspect affected output until acceptable. Each build has a fresh
   preview folder, so stale images cannot be mistaken for new ones.
5. Only after viewing the listed pages, record inspection:

```text
python <skill>/scripts/verify-reviewer.py inspect <run>/verification.json --pages 1,2 --notes "Viewed both pages; equations, captions, and layout checked."
```

The helper rejects stale evidence if source, final PDF, run PDF, or PNGs changed.
It records an inspection attestation; it cannot itself see images or prove that
an agent viewed them. Status remains `visual-check-pending` until all pages for
that run have recorded inspection. Incremental progress may mark a section
checked while listing uninspected, unaffected pages; final verification requires
every page to be inspected.

Record report path, inspected pages, findings/fixes, and pending pages in progress.
If viewing is unavailable, keep `compiled; visual check pending`. If Typst is
missing, keep `written; compile pending`. Do not install global tools automatically
or describe unchecked output as verified.

## Presentation and practice checks

Check Visual Learning against the agreed coverage map, not just its appearance.
Compact Recall must retain essential conditions/steps and label agreed abridgment.
Inspect small diagram labels at useful zoom, meaningful color-independent cues,
table reflow, pen margins, topic links, actual bookmarks and PDF text selection.
Do not mark a style successful merely because it has more or fewer pages.

For practice: compare item count, stems/options and computed answer letters with
the finalized canonical bank in both rendered views. Check rationales after option
shuffle, blueprint coverage, semantic duplicates, ambiguity and distractor cues.
Extract/read the exam's actual text and bookmarks as well as viewing all pages:
no keys/rationales before the answer section; every option and explanation must
remain visible. Successful compilation of an oversized unbreakable block can
still hide text. Inspect continuations and final lines; restructure rather than
silently clipping or reducing the font. Helper validation is structural, not
proof of factual correctness, calibrated difficulty, or learner mastery.

## Optional demos

Follow the available visualization tool/skill's checks for inline interactive aids.
Use available browser tools to open a local HTML demo, exercise
discussed scenarios, and capture/read screenshots. For example, change a vector
with its control and compare the displayed result to the expected calculation.
Record tested inputs/outputs and screenshot paths. Use a local server when the
host requires it; do not assume the portfolio's Puppeteer install exists elsewhere.

Apply the same inspection cycle to generated diagrams/images. Include a checked
static version in the PDF when requested. A visual snapshot does not establish
interactive correctness, accurate OCR, or learned understanding.
