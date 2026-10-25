// academic.typ — the reviewer template
// Maroon and gold academic layout. Portable defaults for any learner.
#import "fonts.typ": *

// ─────────────────────────────────────────────────────────────
// PALETTE — deliberately narrow. Four accents, no more.
//   maroon  structure, definitions, headings
//   gold    emphasis, the thing that must survive
//   slate   worked examples, real-world grounding
//   rust    mistakes and warnings
// ─────────────────────────────────────────────────────────────
#let maroon      = rgb("#6F1D28")
#let maroon-deep = rgb("#4E141C")
#let maroon-soft = rgb("#F6EDEE")
#let au          = rgb("#B08A2E")          // `gold` is taken by the business palette
#let au-light    = rgb("#D9BC6A")
#let au-soft     = rgb("#FBF4E2")
#let slate       = rgb("#3F4A52")
#let slate-soft  = rgb("#F1F3F5")
#let brick       = rgb("#8C2F1E")
#let brick-soft  = rgb("#FBEEEA")

#let cream       = rgb("#FBF7EF")
#let cream-2     = rgb("#F5EFE3")
#let warm-ink    = rgb("#221E1C")
#let warm-body   = rgb("#3A3330")
#let warm-muted  = rgb("#7A6F69")
#let warm-rule   = rgb("#E2D9CC")
#let highlight   = rgb("#FBEFA8")

#let font-display = ("Libertinus Serif", "Cambria", "Georgia")
#let font-label   = ("Segoe UI", "Corbel", "DejaVu Sans")

// ─────────────────────────────────────────────────────────────
// INLINE
// ─────────────────────────────────────────────────────────────

// Highlight a term the way a marker pen would. For the words that get asked.
#let hl(body) = box(
  fill: highlight,
  outset: (y: 3pt, x: 1pt),
  radius: 1.5pt,
)[#body]

// A defined term, inline.
#let concept(t) = text(weight: "bold", fill: maroon)[#t]

// Compact inline column vector: (1, 4, 3)^T.
// A real column vector set inline forces the leading open and makes a
// paragraph look broken. Use this in running text; use display math when the
// vector is the point of the sentence.
#let rvec(..c) = {
  let joined = c.pos().map(p => [#p]).join(", ")
  $(#joined)^T$
}

// ─────────────────────────────────────────────────────────────
// CALLOUTS
// ─────────────────────────────────────────────────────────────
#let acallout(label, accent, bg, body, breakable: false) = block(
  width: 100%,
  fill: bg,
  inset: (left: 13pt, right: 13pt, top: 10pt, bottom: 11pt),
  stroke: (left: 2.5pt + accent),
  breakable: breakable,
  above: 11pt,
  below: 11pt,
)[
  #block(below: 5pt)[
    #text(font: font-label, size: 7.8pt, weight: "bold", fill: accent, tracking: 1pt)[#upper(label)]
  ]
  #set text(size: 10.2pt, fill: warm-body)
  #body
]

// The exam-accurate statement. Never softened.
#let definition(name, body, breakable: false) = acallout(
  "Definition", maroon, maroon-soft,
  [#text(weight: "bold", fill: maroon-deep)[#name] --- #body],
  breakable: breakable,
)

// The one sentence that must survive.
#let keypoint(body, breakable: false) = acallout(
  "Key point", au, au-soft, body, breakable: breakable,
)

// A worked example.
#let example(body, breakable: false) = acallout(
  "Example", slate, slate-soft, body, breakable: breakable,
)

// Where the concept actually shows up in real systems.
#let inpractice(body, breakable: false) = acallout(
  "In practice", slate, slate-soft, body, breakable: breakable,
)

// Learner interpretation is separate from a precise definition or teacher analogy.
#let understanding(body, name: none, breakable: false) = acallout(
  if name == none { "User's Understanding" } else { name + "'s Understanding" },
  slate, slate-soft, body, breakable: breakable,
)

#let teacheranalogy(body, breakable: false) = acallout(
  "Instructor's analogy", au, au-soft, body, breakable: breakable,
)

// The mistake people reliably make.
#let gotcha(body, breakable: false) = acallout(
  "Common mistake", brick, brick-soft, body, breakable: breakable,
)

// Ordinary language. Used on request or after demonstrated difficulty.
#let plain(body, breakable: false) = acallout(
  "In plain words", au, au-soft, body, breakable: breakable,
)

// Optional self-check. Deliberately quiet.
#let recall(body) = block(
  width: 100%,
  inset: (left: 11pt, top: 6pt, bottom: 6pt),
  stroke: (left: 1pt + warm-rule),
  above: 11pt,
  below: 11pt,
)[
  #text(font: font-label, size: 7.5pt, fill: warm-muted, weight: "semibold", tracking: 0.8pt)[#upper("Check yourself")]
  #v(3pt)
  #text(size: 9.6pt, fill: warm-muted, style: "italic")[#body]
]

// ─────────────────────────────────────────────────────────────
// STRUCTURES
// ─────────────────────────────────────────────────────────────

// Two ideas side by side — the workhorse of revision.
#let compare(left-title, left-body, right-title, right-body) = block(
  width: 100%, breakable: false, above: 12pt, below: 12pt,
)[
  #grid(
    columns: (1fr, 1fr),
    gutter: 11pt,
    fill: cream,
    inset: 12pt,
    stroke: 0.5pt + warm-rule,
    grid.cell[
      #text(font: font-label, size: 8.6pt, weight: "bold", fill: maroon, tracking: 0.4pt)[#upper(left-title)]
      #v(6pt)
      #set text(size: 9.8pt, fill: warm-body)
      #left-body
    ],
    grid.cell[
      #text(font: font-label, size: 8.6pt, weight: "bold", fill: au, tracking: 0.4pt)[#upper(right-title)]
      #v(6pt)
      #set text(size: 9.8pt, fill: warm-body)
      #right-body
    ],
  )
]

// An ordered process.
#let steps(..items) = {
  let list = items.pos()
  block(width: 100%, above: 11pt, below: 11pt)[
    #for (i, item) in list.enumerate() {
      grid(
        columns: (19pt, 1fr),
        gutter: 9pt,
        align: (center + top, left + top),
        box(fill: maroon, radius: 50%, width: 17pt, height: 17pt)[
          #align(center + horizon)[
            #text(size: 8.2pt, fill: white, weight: "bold", font: font-label)[#(i + 1)]
          ]
        ],
        block(below: 5pt)[#item],
      )
    }
  ]
}

// A horizontal chain of stages: A → B → C. No external packages.
#let flow(..stages, caption: none) = {
  let items = stages.pos()
  let cells = ()
  for (i, s) in items.enumerate() {
    if i > 0 {
      cells.push(align(horizon)[#text(fill: au, size: 13pt)[#sym.arrow.r]])
    }
    cells.push(block(
      fill: cream-2,
      stroke: 0.5pt + warm-rule,
      radius: 2pt,
      inset: (x: 10pt, y: 8pt),
    )[#align(center)[#text(size: 9.2pt, fill: maroon-deep, weight: "semibold")[#s]]])
  }
  block(width: 100%, above: 12pt, below: 12pt)[
    #align(center)[
      #grid(
        columns: cells.len(),
        column-gutter: 7pt,
        align: horizon,
        ..cells,
      )
    ]
    #if caption != none {
      v(7pt)
      align(center)[
        #text(font: font-label, size: 8.2pt, fill: warm-muted, style: "italic")[#caption]
      ]
    }
  ]
}

// A framed figure with a caption — for the professor's own diagrams, or a
// drawing of your own. `src` is any content: an #image(), a cetz canvas, a table.
#let figbox(src, caption: none, label-text: none) = block(
  width: 100%,
  fill: cream,
  stroke: 0.5pt + warm-rule,
  inset: 14pt,
  radius: 2pt,
  breakable: false,
  above: 13pt,
  below: 13pt,
)[
  #if label-text != none [
    #block(below: 8pt)[
      #text(font: font-label, size: 7.8pt, weight: "bold", fill: maroon, tracking: 1pt)[#upper(label-text)]
    ]
  ]
  #align(center)[#src]
  #if caption != none [
    #v(9pt)
    #align(center)[
      #text(font: font-label, size: 8.3pt, fill: warm-muted, style: "italic")[#caption]
    ]
  ]
]

// ─────────────────────────────────────────────────────────────
// THE TEMPLATE
// ─────────────────────────────────────────────────────────────

// New study units inherit the reading size; legacy components remain compatible.
#let study-unit(title, body) = block(above: 12pt, below: 12pt)[
  #block(sticky: true, below: 7pt)[#text(weight: "bold", fill: maroon)[#title]]
  #body
]

#let study-figure(src, caption: none) = block(breakable: false, above: 10pt, below: 10pt)[
  #align(center)[#src]
  #if caption != none { block(above: 7pt)[#text(size: 10.5pt, fill: slate)[#caption]] }
]

#let note-lines(count: 2) = {
  for i in range(count) {
    block(above: 10pt, below: 2pt)[#line(length: 100%, stroke: 0.4pt + warm-rule)]
  }
}

// Paired views: preserve body size, use stacking for long questions/rationales.
#let practice-item(body, max-height: 205mm) = layout(size => {
  let measured = measure(block(width: size.width)[#body])
  block(breakable: measured.height > max-height, above: 9pt, below: 13pt)[#body]
})

#let practice-pair(question, answer, stacked: false, label: "Question", max-height: 205mm) = layout(size => {
  let pair = if stacked {
    [#question #block(above: 9pt, inset: 9pt, fill: cream)[#answer]]
  } else {
    grid(columns: (1.1fr, 1fr), gutter: 12pt,
      question, block(fill: cream, inset: 9pt)[#answer])
  }
  let measured = measure(block(width: size.width)[#pair])
  if measured.height <= max-height {
    block(breakable: false, above: 9pt, below: 13pt)[#pair]
  } else {
    // Oversized content must continue, never silently overflow a whole page.
    practice-item(max-height: max-height)[#question]
    block(sticky: true, above: 10pt)[#strong[#label — answer and explanation]]
    block(breakable: true, fill: cream, inset: 9pt)[#answer]
  }
})

#let reviewer(
  title: "Untitled reviewer",
  course: none,       // "MATH 018 — Linear Algebra with Simulation Software"
  topic: none,        // "Vectors and the RGB colour system"
  date: none,         // ISO
  author: none,
  instructor: none,
  sources: (),
  cover: false,
  section-breaks: false,
  style: "classic",    // classic | visual | compact; unspecified preserves old layout
  profile: "paper",    // paper | computer | tablet-portrait | tablet-landscape | mobile; tablet is a portrait alias
  navigator: false,
  body,
) = {
  assert(style in ("classic", "visual", "compact"), message: "Unknown presentation style")
  assert(profile in ("paper", "tablet", "tablet-portrait", "tablet-landscape", "computer", "mobile"), message: "Unknown page profile")
  let portrait = (width: 180mm, height: 240mm,
    margin: (top: 14mm, bottom: 16mm, left: 13mm, right: 22mm))
  let devices = (
    paper: (width: 210mm, height: 297mm, margin: (top: 25mm, bottom: 21mm, left: 24mm, right: 24mm)),
    tablet: portrait, tablet-portrait: portrait,
    tablet-landscape: (width: 240mm, height: 180mm, margin: (top: 14mm, bottom: 16mm, left: 25mm, right: 35mm)),
    computer: (width: 280mm, height: 175mm, margin: (top: 14mm, bottom: 14mm, left: 55mm, right: 55mm)),
    mobile: (width: 100mm, height: 178mm, margin: (top: 10mm, bottom: 12mm, left: 8mm, right: 8mm)),
  )
  let device = devices.at(profile)
  set document(title: title, author: if author == none { () } else { author })

  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.1cm, left: 2.4cm, right: 2.4cm),
    header: context {
      if counter(page).get().first() > 1 {
        set text(font: font-label, size: 8pt, fill: warm-muted)
        grid(
          columns: (1fr, auto),
          align: (left, right),
          if profile == "mobile" { "Study notes" } else if course != none { course } else { title },
          if profile == "mobile" { "" } else if topic != none { topic } else { "" },
        )
        v(-3pt)
        line(length: 100%, stroke: 0.5pt + warm-rule)
      }
    },
    footer: context {
      if counter(page).get().first() > 1 {
        set text(font: font-label, size: 8pt, fill: warm-muted)
        line(length: 100%, stroke: 0.5pt + warm-rule)
        v(2pt)
        grid(
          columns: (1fr, auto),
          align: (left, right),
          if profile == "mobile" { "Study notes" } else { title },
          [#counter(page).get().first() / #counter(page).final().first()],
        )
      }
    },
  )

  set page(width: device.width, height: device.height, margin: device.margin)

  set text(font: font-display, size: if profile == "mobile" { 12pt } else if style == "visual" { 11.5pt } else { 11pt }, fill: warm-body, lang: "en")
  set par(justify: style == "classic", leading: if style == "compact" { 0.55em } else { 0.75em },
    spacing: if style == "compact" { 0.65em } else { 1.1em }, first-line-indent: 0pt)
  set heading(numbering: "1.1")

  // ── Headings ───────────────────────────────────────────────
  // Level 1: a maroon banner, like a chapter opener.
  show heading.where(level: 1): it => context {
    if (section-breaks and counter(heading).get().first() > 1) or cover { pagebreak(weak: true) }
    block(
      width: 100%,
      fill: maroon,
      inset: if style == "compact" or profile == "mobile" { (x: 10pt, top: 8pt, bottom: 9pt) } else { (x: 16pt, top: 13pt, bottom: 15pt) },
      radius: 2pt,
      above: if style == "classic" and profile not in ("computer", "tablet-landscape", "mobile") { 0pt } else { 14pt },
      below: if style == "compact" { 10pt } else { 17pt },
      breakable: false,
      sticky: true,
    )[
      #if it.numbering != none [
        #block(below: 6pt)[
          #text(font: font-label, size: 8pt, weight: "bold", fill: au-light, tracking: 1.6pt)[
            #upper("Section " + counter(heading).display("1"))
          ]
        ]
      ]
      #text(font: font-display, size: if style == "compact" or profile == "mobile" { 15pt } else { 19pt }, weight: "bold", fill: white)[#it.body]
    ]
  }

  // Level 2: maroon, with a gold hairline beneath.
  show heading.where(level: 2): it => block(above: 19pt, below: 9pt, breakable: false, sticky: true)[
    #text(font: font-display, size: 13.5pt, weight: "bold", fill: maroon)[
      #if it.numbering != none [
        #counter(heading).display(it.numbering)#h(8pt)
      ]
      #it.body
    ]
    #v(4pt)
    #line(length: 100%, stroke: 0.7pt + au-light)
  ]

  // Level 3: quiet.
  show heading.where(level: 3): it => block(above: 14pt, below: 5pt, breakable: false, sticky: true)[
    #text(font: font-display, size: 11.2pt, weight: "bold", fill: warm-ink)[#it.body]
  ]

  // ── Code ───────────────────────────────────────────────────
  show raw.where(block: true): it => block(
    width: 100%,
    fill: cream-2,
    radius: 2pt,
    inset: 11pt,
    stroke: (left: 2pt + au-light),
    breakable: true,
    above: 11pt,
    below: 11pt,
  )[#set text(font: font-mono, size: if style == "classic" { 8.8pt } else { 10.5pt }); #it]

  show raw.where(block: false): it => box(
    fill: cream-2,
    radius: 2pt,
    inset: (x: 2.5pt, y: 0pt),
    outset: (y: 2.5pt),
  )[#set text(font: font-mono, size: 9pt, fill: maroon-deep); #it]

  // ── Tables ─────────────────────────────────────────────────
  set table(
    stroke: (x, y) => (bottom: 0.5pt + warm-rule),
    inset: (x: 9pt, y: 7pt),
    fill: (x, y) => if y == 0 { maroon } else if calc.odd(y) { cream } else { white },
  )
  show table.cell.where(y: 0): set text(
    font: font-label, weight: "bold", fill: white, size: if style == "classic" { 9pt } else { 10.5pt },
  )

  // ── Lists ──────────────────────────────────────────────────
  set list(indent: 7pt, spacing: if style == "compact" { 0.35em } else { 0.72em }, marker: text(fill: au)[#sym.bullet])
  set enum(indent: 7pt, spacing: if style == "compact" { 0.35em } else { 0.72em })
  show link: it => text(fill: maroon)[#underline(offset: 2pt, stroke: 0.4pt + au-light)[#it]]
  show emph: it => text(fill: warm-ink)[#it]

  // ── Cover ──────────────────────────────────────────────────
  if cover {
    page(
      margin: (top: 3.2cm, bottom: 2.6cm, left: 2.8cm, right: 2.8cm),
      header: none,
      footer: none,
      background: place(
        top + left,
        dx: 1.15cm, dy: 1.15cm,
        rect(
          width: 100% - 2.3cm,
          height: 100% - 2.3cm,
          stroke: 0.6pt + au-light,
        ),
      ),
    )[
      #v(1.6cm)
      #align(center)[
        #set par(justify: false)
        #if course != none [
          #text(font: font-label, size: 9pt, weight: "semibold", fill: maroon, tracking: 2.4pt)[
            #upper(course)
          ]
          #v(1.1cm)
        ]

        #text(font: font-display, size: if profile == "mobile" { 24pt } else { 34pt }, weight: "bold", fill: maroon-deep, hyphenate: false)[#title]

        #if topic != none [
          #v(0.55cm)
          #text(font: font-display, size: 13pt, fill: warm-muted, style: "italic")[#topic]
        ]

        #v(1.1cm)
        #line(length: 62%, stroke: 0.8pt + au)
        #v(1.1cm)

        #set text(font: font-label, size: 9.5pt, fill: warm-body)
        #if date != none [ #upper(text(size: 8pt, fill: warm-muted, tracking: 1.2pt)[Date]) #h(6pt) #date #linebreak() ]
        #if instructor != none [ #v(3pt) #upper(text(size: 8pt, fill: warm-muted, tracking: 1.2pt)[Instructor]) #h(6pt) #instructor ]
      ]

      #v(1fr)

      #if sources.len() > 0 [
        #align(center)[
          #block(width: 82%)[
            #line(length: 100%, stroke: 0.5pt + warm-rule)
            #v(9pt)
            #text(font: font-label, size: 7.8pt, weight: "semibold", fill: warm-muted, tracking: 1.2pt)[
              #upper("Built from")
            ]
            #v(6pt)
            #set text(font: font-label, size: 9pt, fill: warm-muted)
            #for s in sources [ #s #linebreak() ]
            #v(9pt)
            #line(length: 100%, stroke: 0.5pt + warm-rule)
          ]
        ]
      ]
      #v(0.6cm)
    ]
  } else {
    // No cover: a compact masthead instead.
    if course != none {
      block(below: 5pt)[
        #text(font: font-label, size: 8.5pt, weight: "bold", fill: maroon, tracking: 1.4pt)[#upper(course)]
      ]
    }
    block(below: 6pt)[
      #text(font: font-display, size: if profile == "mobile" { 20pt } else { 26pt }, weight: "bold", fill: maroon-deep)[#title]
    ]
    if topic != none {
      block(below: 12pt)[
        #text(font: font-display, size: 12pt, fill: warm-muted, style: "italic")[#topic]
      ]
    }
    line(length: 100%, stroke: 1.5pt + au)
    v(14pt)
  }

  if navigator {
    block(above: 12pt, below: 5pt, sticky: true)[
      #text(font: font-label, size: 11pt, weight: "bold", fill: maroon)[Topics]
    ]
    outline(title: none, depth: 2)
    v(10pt)
  }
  body
}
