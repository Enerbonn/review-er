# Optional practice documents

## Plan before generating

Create only requested outputs/count/scope/difficulty/question types. A visual
guide alone doesn't request a quiz. In Review, preserve discussion and write-up
approval for lesson additions. A direct request for a complete practice document
authorizes its drafting; it does not establish learner understanding or permit
changing approved notes. An existing supplied practice set is source content,
not permission to claim official exam coverage or validated difficulty.

Build a topic blueprint from the checked concept/source map. Assign item counts
proportionally to the agreed priorities, not just the easiest subsection. Record
evidence and answer reasoning locally. State jurisdiction/date/assumed resources
where relevant; distinguish attributed course wording from verified current
guidance. Medical/legal or changing technical claims need primary-source checks.

## One bank, two views

For matching versions, use one canonical bank and one finalized question/option
ordering. Stable option IDs determine the answer; compute the printed letter
after shuffling. Write rationales by option content, not pre-shuffle letters.
Both views must have identical numbering, stems, choices, letters and rationale
mapping. State that the questions match and recommend mock exam first for an
unseen attempt. A different set requires an explicit alternate-set choice.

### Side-by-side answer reviewer

Pair the complete question/options on one side with the key and explanation on
the other. Answers are intentionally visible here. Explain the decisive clue and
why each plausible competing answer is less appropriate, rather than repeating
the key. Keep pairs together. If narrow columns hurt readability, use a wider
profile, fewer items/page, or a clearly paired full-width question/answer layout.
Provide pen space when feasible. If one item cannot fit a page, restructure with
clearly numbered continuation; do not shrink text or omit options/rationale.

### Mock exam

All questions before the key and rationales; answer section starts after the final
question. No correct letters in question styling, captions, running headers or
bookmark titles. Include a complete numbered key and full rationales after it.
Optional score sheet/time are suggestions, not validated test duration. Don't
distribute an answer-bearing bank as part of an unseen exam handout.

## Bundled MCQ helper

`scripts/build-practice.py` validates a local JSON bank and writes requested Typst
view(s), a template copy and a normalized private bank into a new output folder.
It uses Python stdlib only; compile/inspect separately with verify-reviewer.py.
It doesn't assess factual correctness, defensibility, difficulty or learner mastery.
Other question types/layouts can be authored using these rules without the helper.
Each view has its own folder (`reviewer/reviewer.typ`, `exam/reviewer.typ`) and
verification runs, so building one PDF does not stale the other's evidence.

```text
python <skill>/scripts/build-practice.py bank.json -o <lesson>/practice --view both --count 8 --profile tablet --seed 17
```

`--view reviewer|exam|both`; `--profile paper|computer|tablet-portrait|tablet-landscape|mobile`
(`tablet` remains a portrait alias); optional `--seed` shuffles
options once for both views; without a seed input ordering is preserved. Refuses
nonempty destinations. Long pairs stack; measured whole-page overflows switch to
full-width continuing content with the question number retained for its answer.
Inspect all pages and restructure awkward continuations rather than shrinking type.
Mobile always uses full-width stacked question/answer pairs. Other profiles use
side-by-side pairs when readable and stack longer items; continuation thresholds
respect each profile's vertical space. A requested device changes layout, not
bank content, option order, count or answer visibility.

Bank shape (make all items/source fields real for the agreed lesson):

```json
{
  "title": "Requested practice set",
  "blueprint": {"Topic name": 1},
  "items": [{
    "id": "q1", "topic": "Topic name", "stem": "Complete question?",
    "options": [{"id":"x","text":"Choice one"}, {"id":"y","text":"Choice two"}, {"id":"z","text":"Choice three"}, {"id":"w","text":"Choice four"}],
    "correct": "y", "rationale": "Decisive reason for choice two.",
    "distractors": {"x":"Why one is less appropriate.", "z":"Why three is less appropriate.", "w":"Why four is less appropriate."},
    "source": "Local source file and page/timestamp or primary reference"
  }]
}
```

## Validation beyond schema

Exactly requested count; four distinct options for this MCQ format; unique IDs
and stems; one defensible key; no semantic duplicate questions; complete reasoning
and distractors; blueprint coverage. Review plausible distractors, grammatical or
absolute-language cues, consistently longer correct options and answer patterns.
Don't alter correct content just to make letter counts uniform. After shuffling,
compare both PDFs with the finalized bank. Inspect actual text and bookmarks for
answer leaks before the answer section, not just source file order. Schema checks
cannot prove semantic uniqueness or key correctness. Keep factual/visual QA
separate and record actual findings and unresolved limitations.
