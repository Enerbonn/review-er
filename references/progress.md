# Local subject and lesson memory

Use files in the chosen subject/course folder so any compatible agent can resume
there. Reuse an existing study tracker where suitable and preserve unrelated
entries. No global learner profiles, scans of unrelated courses, or public uploads.

## Subject index: `_study-progress.md`

Keep subject/source coverage, **immediate objective**, **broader learning purpose**,
**application preferences**, current mode (Review/Reviewer),
language/name if supplied, and optional offer preferences. Maintain a lesson table
with last-worked ISO date in the user's timezone, coverage, observed understanding
and gaps, reviewer status, and links to output/lesson progress. Include the exact
next lesson/part and pending action. The index summarizes and points; lesson
records hold detail. Store each goal field separately with the learner's wording
or a faithful summary, last-updated date and provenance (current request or saved
learner answer). Unknown, exam-only, general curiosity and personalization skipped
are distinct states. Do not populate broader purpose from exam scope or an owner
profile. Application preferences may be unspecified; do not invent them or require
another question when the broader answer is sufficient.

Carry subject defaults into new lessons unless the user supplies a lesson-specific
override; record the override rather than silently changing every subject goal.
On an explicit change, update the appropriate goal/preference and date, preserve
other fields and earlier learning evidence, and use the new preferences going forward.

## Lesson record: `_progress.md`

Save interaction mode separately from presentation (legacy/Visual Learning/Compact
Recall), output selection (guide/answer reviewer/mock exam), device/page profile,
and length preferences. Reuse explicit choices; don't repeat setup or infer mastery.
Keep one checked concept/source map shared by styles and an assessment blueprint
linked to the same scope. Record approved exclusions or abridgment, canonical bank
path/hash and finalized option ordering, correction dates/jurisdiction when relevant,
and inspection coverage per delivered PDF. Reviewer authorization never fabricates
Review discussions or approvals. A restyle preserves approved substance and records
any material scope tradeoff rather than silently overwriting it.

Save the outline and per-part document state. Review uses
`planned -> discussing -> approved -> written -> verified`. Reviewer may use
`planned -> written -> verified`, recording scope-level drafting authorization;
do not fabricate discussions or section approvals.

Record dates, source map (file, role, page/slide/timestamp ranges), current part,
the separate goal/preference fields or a pointer to subject defaults plus lesson overrides,
approved but unwritten content, uncertainties/disputes, optional practice/visual/
deeper-application choices, and verification paths/inspected pages/pending checks.

Track understanding separately with evidence:

| Part | Observed understanding | Evidence/date | Next step |
|---|---|---|---|
| Matrix dimensions | Explained rows/columns; product compatibility unclear | Learner explanation, YYYY-MM-DD | Ask which products are defined |
| Transformations | Not assessed; Reviewer mode | Draft created, YYYY-MM-DD | Optional later Review |

Use concrete observations: explained, applied, uncertain, not assessed. No invented
proficiency percentages, mastery, scores or quotes. Scores require actual agreed
practice. Preserve useful learner phrasing and teacher analogies with provenance,
corrections and agreed inclusion choices.

## Keep tracking out of the reviewer

Local progress/source records hold dates, source filenames/pages/timestamps,
source-versus-added provenance, approval history, coverage and exclusions,
compilation/inspection evidence, and pending actions. These remain required even
when the PDF has no source list or metadata. Do not copy the tracking log or
process commentary into study notes. A source correction may need a concise
content warning in the PDF; its exact citation and verification belong here
unless the user requests visible references. Save compactness preferences and
explicit content exclusions, including changes to earlier approved sections.

## Save and resume

Update both records after meaningful work and before stopping, even before
approval. Save the exact pending question and enough discussion to avoid asking
the learner to repeat it. Reconcile records with actual files and fresh verification
on return; repair stale pointers without erasing learning. Briefly state where
the user stopped, then continue that step without repeated onboarding if purpose
or opt-out is already explicit. Older records saying only "exam preparation" do
not prove exam-only preference: preserve the immediate objective, mark broader
purpose unknown, ask the concise purpose question before teaching/drafting, and
continue the exact pending step afterward. A saved opt-out remains valid on resume;
do not ask again merely because it lacks a career/application goal. Current explicit
answers override stale saved fields without another onboarding exchange.

Mode switches preserve approved work. Review -> Reviewer drafts the requested
remaining scope without claiming it was learned. Reviewer -> Review uses existing
notes as discussion material and assesses only parts actually discussed.

These are private local files, not account-wide memory or release assets.
