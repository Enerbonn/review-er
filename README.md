# review(er)

**Review a lesson. Build a reviewer. Choose how much conversation you need.**

An AI-assisted learning skill for students and curious learners who want help
without handing over the work of understanding. In **Review** mode, you explain,
ask questions, work through mistakes, and build notes along the way. In
**Reviewer** mode, the agent creates the document directly when time is short.

I made this because I enjoy building reviewers and learning through the process,
but sometimes I just need the notes. Long lecture videos can also be hard to sit
through. This gives me a way to study at my own pace, with an AI that can explain
a step again without judgment. It supports the difficult part of learning rather
than pretending a generated PDF means I have learned it.

## Two modes

| Mode | What happens |
|---|---|
| **Review** | Short back-and-forth discussion, corrections and examples; approve each manageable part, then add it to the reviewer. |
| **Reviewer** | Create requested notes directly, without teach-back or repeated section approvals; understanding is recorded as not assessed. |

Switch modes without losing existing work. On first use, the agent asks what you
are studying, the immediate objective, and the broader learning purpose, plus mode
if missing. Exam pointers tell it what to cover; they do not answer what you want
to understand or use it for. If broader purpose is unknown, it asks one short
question before teaching or drafting. "Exam only", "general curiosity", and
skipping personalization are valid answers; no career goal is required.
Explicit or saved answers are reused. Immediate and broader goals and application
preferences are saved separately, and can change without restarting a lesson.
Examples distinguish direct applications from foundational connections; added
examples are labeled separately from instructor content.

Reviewers default to compact study notes: definitions, essential worked examples,
and useful visuals. Dates, source references, approvals, and verification details
stay in local progress files. Covers, bibliographies, and extended notes are
available when requested. Compactness preserves required topics and readability.

## Choose the presentation and outputs

These choices are separate from Review/Reviewer:

| Choice | Use it for |
|---|---|
| **Visual Learning** | Understanding the subject through readable diagrams, comparisons, worked examples and connected explanations. More pages are fine when they help. |
| **Compact Recall** | Efficient revision: concise rules, conditions, formulas, exceptions and traps, without tiny text or silent omissions. |
| **Learning guide** | The requested lesson scope, in either presentation. |
| **Side-by-side answer reviewer** | Questions paired with visible answers and explanations. Long items can use a full-width paired layout. |
| **Mock exam** | Questions first; complete key and rationales after the final question. |

If no new style is requested, existing compact-study behavior remains available.
Practice is optional. Matching answer-reviewer/exam versions use the same checked
bank and option ordering; try the mock exam first if you want an unseen attempt.
The skill does not impose a subject, item count, or universal page limit.

An optional portrait tablet profile starts at 180 x 240 mm with readable body
text and pen space. A4 remains the default; other device/paper layouts can be
adapted. Longer guides can include a linked topic navigator and PDF bookmarks.
Figures must teach an accurate relationship, not decorate the page; corrections
and older/current source comparisons retain clear labels and retrievable evidence.

Example:

> Use Reviewer mode to create a Visual Learning guide and matching 12-question
> answer reviewer and mock exam from these sources. My purpose is general curiosity.
> Use the tablet profile; preserve necessary explanations and keep answers at the end
> of the mock exam. Do not treat document creation as proof I understand the lesson.

See [presentation choices](references/presentation.md) and
[practice documents and bank helper](references/assessments.md).

## Features

- Maps supplied sources first, then follows the current topic using relevant evidence.
- Connects examples and optional real-life applications to your learning goal.
- Offers deeper exploration and optional quizzes, activities or practice problems; decline or skip offers for the session.
- Keeps useful source images and valid instructor analogies, including their original language.
- Shows relevant source images, slide/page excerpts or lecture frames in the conversation when helpful.
- Creates focused diagrams or interactive teaching aids when they improve understanding; keeps text-only explanations when sufficient and respects your preferences.
- Preserves agreed **User's Understanding** notes separately from definitions and instructor explanations.
- Flags source uncertainty and factual disagreements, offering clearly labeled choices for your notes.
- Saves dated local subject/lesson progress, understanding gaps, completed reviewers and the exact resume point.
- Builds a Typst PDF and requires inspection of rendered pages, with evidence that detects stale output.

## Partner: TransVision

[TransVision](https://github.com/Enerbonn/TransVision) turns a recording's visual
content into timestamped frame PDFs, PNGs and optional OCR text. **review(er)**
uses those exports to support learning and build the reviewer. It also works
with ordinary notes, slides, documents and transcripts without TransVision.

Pair a separate **SRT audio transcript** with TransVision's **timestamped PDF
parts or visual transcript**. Export SRT from your audio transcription app and
enable **PDF timestamps** in TransVision. **VTT works equally well**; the skill's
extractor preserves cue times in both formats. Plain TXT remains usable, but if
it has no timestamps, matching speech to visuals depends on topic and context.
Use the same recording start point and report any trimming or clock offset;
never invent timestamps for untimed text.

Audio carries speech; visuals carry what was on screen. When speech is
unclear, the agent can check nearby frames and notes instead of guessing. It
maps sources initially, then retrieves relevant evidence rather than rereading
every source on every turn.

TransVision splits PDFs into parts of at most 100 pages by default. For example,
250 exported frames from `10-11-2026.mp4` produce:

```text
10-11-2026_01.pdf   100 pages
10-11-2026_02.pdf   100 pages
10-11-2026_03.pdf    50 pages
```

At 100 pages or fewer, the PDF keeps the video's base name. The skill follows
part order, timestamps and `pages.json` when supplied. Renamed files are fine.
Give the agent the export folder or complete PDF parts when possible;
`AI_UPLOAD.zip` includes only flagged images, not every selected frame. OCR is a
draft, especially for mathematics, code and handwriting. The skill does not run
TransVision, transcribe audio, or automatically upload materials.

If your lesson includes **SOURCES.md** or a source-index README, supply it too.
The agent uses it to identify notes, speech transcripts, visual parts and related
classes before reading their contents. A supplied practice reviewer can guide
exercise types and exam preparation; it does not automatically establish exam coverage.

The optional [course-resource-organizer companion skill](https://github.com/Enerbonn/review-er/blob/main/companion-skills/course-resource-organizer/SKILL.md)
handles readable naming, verified moves, transcript replacement and source-guide
updates before learning begins. Install that folder separately in your agent's
skills directory when you want resource organization.

## Ways to use review(er)

### With a coding agent that can access local files

This is an instruction package for an agent, not a standalone application.
Download [this repository](https://github.com/Enerbonn/review-er) and copy the whole
package into your project's skill folder:

```text
your-project/.agents/skills/reviewer-building/
  SKILL.md
  README.md
  LICENSE
  agents/
  references/
  scripts/
  assets/
```

The display name is **review(er)**; the machine identifier stays
**reviewer-building**, so the Codex invocation is `$reviewer-building`.
Other agents supporting SKILL.md can use the package; their discovery locations
and invocation syntax may differ.

Example:

> Use $reviewer-building in Review mode with these TransVision PDF parts and my
> SRT audio transcript from the same recording. I am studying linear algebra for computer science and AI
> automation. Save notes and progress in my linear-algebra folder.

Or:

> Use $reviewer-building in Reviewer mode. I have little time; create a reviewer
> from these materials without the learning back-and-forth.

### In a regular AI chat: upload the instructions and lesson files

You can use the conversational workflow without installing a coding agent or
giving an AI access to your computer. Attach [SKILL.md](SKILL.md) to a chat that
can read uploaded files, along with the materials you want to study:

- Lecture notes or a document/PDF.
- An audio transcript, preferably timestamped SRT or VTT; TXT works too.
- TransVision visual transcripts, frame images or timestamped PDF parts.
- Slides/PPTX, if supported by your chat; otherwise export the slides to PDF.

Use whichever sources you have: notes, audio, visuals, or a combination. Having
only one type is fine; missing evidence should be stated rather than invented.
The chat needs image-reading capability to inspect diagrams or image-only PDF
pages. If it cannot read a format, provide a readable export or the relevant pages.

Example message after attaching the files:

> Follow the attached SKILL.md as my study workflow. Use Review mode: help me
> understand one small part at a time and build the notes as I approve them.
> My immediate objective is exam preparation; my broader purpose is understanding
> how these ideas apply to data analysis. Use the attached lesson sources and
> distinguish instructor content from your added examples.

For direct notes, replace Review with **Reviewer** and ask for the requested
reviewer without the learning back-and-forth. You can also say **exam only**,
**general curiosity**, or **skip personalization** instead of giving an application goal.
In an ordinary chat, ask it to follow the attached instructions; skill invocation
syntax such as `$reviewer-building` is not required.

**SKILL.md is the starting point, not the entire package.** It links to supporting
instructions the chat may not be able to open automatically. Attach the relevant
files from [references/](references/) too, especially source handling, progress,
and practice/visual guidance. For the new styles and practice formats, include
[presentation.md](references/presentation.md) and [assessments.md](references/assessments.md).
For Typst output, supply the template assets and
Typst/verification references as well. If the chat cannot read a linked resource,
it should ask for it or state the limitation, rather than claim to have followed it.

File limits and tools vary by chat. Send large lessons in chronological batches,
keeping timestamps and PDF part names, and identify anything not uploaded yet.
A chat without a compiler can still teach and create Markdown notes or Typst
source; it cannot claim a compiled, visually verified PDF. Scripts require an
execution tool, and the template must be available for the formatted Typst output.

**Save your own checkpoint:** ask for a downloadable or copyable progress summary
with your goals, covered parts, understanding/gaps, approved notes, source locations
and exact next question. Save it with the reviewer. When returning or starting a
new chat, attach that checkpoint and the relevant sources again. Without local
file tools, saving progress to your computer is a manual step; chat memory alone
should not be treated as the lesson record.

## Requirements and saved work

- Access to the supplied files, through local tools or chat attachments; image/PDF viewing for visual source reading and output checks.
- Typst CLI for PDF compilation and page rendering. The template needs no global package installation or network package downloads.
- Python 3.10+ for the optional extraction and verification helpers; standard library only.

Learning can begin without a compiler. Missing tools are recorded as pending
checks, rather than claiming output was verified.

Inline images and interactive buttons, tabs or sliders depend on the chat's
display capabilities. The agent uses available visualization tools when useful,
with static diagrams or a local preview as fallbacks. The skill does not add UI
support to a host that lacks it. Conversational visuals do not start a quiz or
bypass Review-mode approval before adding content to the reviewer.

The chosen subject folder holds `_study-progress.md`, a compact lesson index.
Each lesson has `_progress.md`, `reviewer.typ`, its compiled `reviewer.pdf`, local
template/materials and verification evidence. A compatible agent resumes from
these files. This is local memory, not account-wide memory. Private study work
belongs outside the skill package; the `.gitignore` excludes common generated
files using an explicit end-user-file allowlist. Arbitrarily named personal files
are ignored too; forced additions and already tracked files still need review.

Agent procedures: [sources](references/materials.md), [progress](references/progress.md),
[practice and visuals](references/practice-and-visuals.md), [Typst](references/typst.md),
and [output verification](references/verification.md).

## Limits

Teaching quality depends on the agent and sources. The skill cannot guarantee
accurate OCR, enforce every agent decision, or establish mastery from a document.
The verification helper records inspected pages and detects changed artifacts;
the agent must actually view and assess them. Learner feedback is welcome through
[GitHub issues](https://github.com/Enerbonn/review-er/issues).

## Credit and license

Created by **Irvin John J. Parulan**. Source: [Enerbonn/review-er](https://github.com/Enerbonn/review-er).
Partner: [Enerbonn/TransVision](https://github.com/Enerbonn/TransVision).

The skill and bundled template use the [MIT license](LICENSE), including
commercial use. Retain copyright and license notices in copies or substantial
portions; creator and repository attribution is appreciated. This does not grant
rights to imported lecture materials, third-party assets, or TransVision itself.
