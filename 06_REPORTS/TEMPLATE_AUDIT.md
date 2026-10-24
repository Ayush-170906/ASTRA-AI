# TEMPLATE AUDIT — PVG IT Technical Seminar (T.E., AY 2026–27)

Prepared: Phase 1A. Source files inspected are the untouched official copies in
`01_OFFICIAL/` (`TE SEMINAR Presentation PPT FORMAT.ppt`, `Seminar Synopsis-2026-27.docx`).
Working inspection copies (`.pptx`/`.pdf`/slide PNGs) live in `03_RESEARCH/` and were
generated via PowerPoint/Word COM automation — **the originals in `01_OFFICIAL/` were
never opened for editing and remain byte-identical to the Downloads source.**

---

## A. PPT TEMPLATE AUDIT

**File:** `TE SEMINAR Presentation PPT FORMAT.ppt` (legacy binary, 12 slides)

### A.1 Slide geometry
| Property | Value |
|---|---|
| Slide size | 13.33 in × 7.5 in (widescreen 16:9) |
| Aspect ratio | 1.7778 |
| Master layouts available | Title Slide, Title and Content, Section Header, Two Content, Comparison, Title Only, Blank, Content w/ Caption, Picture w/ Caption, Title and Vertical Text, Vertical Title and Text — **but every actual slide in the deck uses the "Blank" layout with manually placed shapes**, not the named layouts. Content is built from free text boxes + a rectangle "header bar" shape, not placeholder-driven layouts. |

### A.2 Visual language (must be reused, not reinvented)
- **Border/frame:** every slide has a black rounded-rectangle outline frame drawn around the full slide edge (decorative border, no fill).
- **Header bar:** a rectangle spanning near-full width at the top of each content slide, filled with `schemeClr accent1` tinted `lumMod 40% / lumOff 60%` (a light peach/salmon over the theme's rust-orange accent). Theme `accent1 = #D34817`. Header text: **Arial Narrow, bold, 36pt (28pt on Outline slide's own header... actually consistently 36pt/sz=3600)**, color = text1 (black), centered.
- **Slide number badge:** a filled orange/rust oval (accent1 full strength) bottom-left corner, white number text.
- **Footer text:** "Department of Information Technology | PVG's COE&SSDIOM Nashik" — **Arial Narrow, 12pt, color `#7030A0` (purple)**, centered near bottom.
- **Title-slide only elements:** SPPU seal (left) + University "Vidya Vikas" logo (right) images, ~4.3×1.8in combined, centered lower-middle; "Academic Year 2026–27" line rendered in the same purple `#7030A0`.
- **Body text:** Times New Roman throughout. Sizes actually used in placeholders:
  - Outline / body bullet text: **21pt bold** (except sub-bullets, still TNR)
  - Section sub-heading (e.g. "1.1 Motivation"): **24pt bold**
  - Reference list entries: **15pt**
  - Figure captions: **12pt**
  - "Thank You" slide title: 60pt; "Any Questions?" 54pt, italic.
  - Header banner text: Arial Narrow 36pt bold (not Times New Roman — this is the one place the template departs from TNR).
- **Theme accent palette (for any diagrams/charts placed on slides):** accent1 `#D34817` (rust/terracotta — primary), accent2 `#9B2D1F`, accent3 `#A28E6A`, accent4 `#956251`, accent5 `#918485`, accent6 `#855D5D`, dk2 `#696464`, lt2 `#E9E5DC`. This is a warm earth-tone palette — diagrams should draw from these, not a blue/tech palette.

### A.3 Slide-by-slide structure (as literally present in the file)
1. **Title slide** — "A Seminar Review I Presentation on" / Title bar ("Title of the Seminar") / "Submitted to SPPU..." / "Presented By — XYZ | PRN" / "Guided By — Guide Name" / Dept + College name / Academic Year, plus SPPU + university seal images.
2. **Outline** — single slide listing all major sections (Introduction incl. 1.1–1.3 sub-points, then 2–9 as flat numbered items).
3. **1. Introduction** (section header reused as banner text) — instructional placeholder only ("Must about the current scenario… Must cite the References").
4. **1.1 Motivation** — banner still says "1. Introduction"; instructs 2+ points.
5. **1.2 Objective** — banner still "1. Introduction"; instructs 2–3 bullets.
6. **1.3 Problem Statement** — banner still "1. Introduction"; instructs 1–2 paragraphs.
7. **2. Related Work / Literature Survey** — instructs tabular/bulleted IEEE-cited content.
8. **3. Proposed Methodology / Prototype / Idea / Algorithm** — instructs paragraph/bullet content **and a required system diagram/flowchart/prototype image**, with sample figure "Figure 2.1: Production of Pekilo Protein" (generic unrelated sample figure to be replaced) and 12pt caption style.
9. **5. Hardware / Software Specification** — banner numbered "5." (template's own numbering skips "4."); Hardware / Software as two labeled sub-lists.
10. **4. Conclusion** — banner numbered "4." (appears *after* slide 9's "5." in file order — the official template's own slide order/numbering is internally inconsistent; see A.4).
11. **5. References** — numbered reference list, sample references present (unrelated biotech topic, to be fully replaced), 15pt.
12. **Thank You / Any Questions?** — big banner "Thank You!", "Any Questions?" text, small stick-figure clipart image (to be kept or swapped for something equally minimal — not a decorative addition).

### A.4 Explicit template quirks / requirements found in-file (not guessed)
- Every placeholder carries **red Times-New-Roman instructional text** in parentheses specifying exact required font/size (e.g. "(use font type & size Times New Roman 21)"). These are editing instructions embedded by the college, not content — **all red instructional text must be deleted and replaced with real content in the matching font/size**, never left in the final deck.
- The Outline slide's own numbered list has a **built-in inconsistency**: items go 1 (Introduction, unnumbered bullet) → 2 → 3 → 4 (Implementation Details) → 5 (Hardware/Software) → 6 (Results/Observations) → then **"4. Conclusion" and "5. References" again**, duplicating numbers 4 and 5. The section-banner slides (9→10→11) likewise carry "5. Hardware/Software" then "4. Conclusion" then "5. References" out of numeric order. This is a pre-existing defect in the official file, not something to silently "fix" by renumbering the college's template — the audit flags it; the **content plan below (Section H) proposes a clean, strictly sequential 1–9 numbering** consistent with the synopsis and with what the outline says the sections *should* be, and this will be called out explicitly to the student before finalizing (see open item in Section G).
- Literature survey slide explicitly says "take the reference of IEEE base paper" — confirms citation is a grading requirement, not optional polish.
- Methodology slide explicitly requires "a prototype / System diagram / flowchart / working model" with a captioned figure — confirms a diagram is mandatory, not decorative.
- No dedicated "Research Gap" or "Challenges/Limitations" slide exists in the official 12-slide skeleton — these are **additions** the master instructions ask for; they must be built using the same banner/footer/font visual language as the rest of the deck (Arial Narrow 36pt banner, TNR 21pt body, same peach banner + purple footer) so they read as native to the template, not bolted on.
- No "Evaluation Framework" slide exists either — "6. Results / Observations" in the Outline is the natural home for it, worded as proposed/expected metrics per the master instructions' no-fabrication rule.

---

## B. SYNOPSIS TEMPLATE AUDIT

**File:** `Seminar Synopsis-2026-27.docx` (4 pages as paginated by Word)

### B.1 Page setup
| Property | Value |
|---|---|
| Page size | 8.5in × 11in (US Letter) |
| Margins | 1.0in all sides |
| Header distance | 0.5in |
| Footer distance | 0.15in |
| Footer text | "Department of Information Technology \| PVG'sCOE&SSDIOM, Nashik" + right-aligned "Page X \| 4", present from page 2 onward (title page has no footer) |

### B.2 Page-by-page structure
- **Page 1 — Title page.** "A Seminar / On / "Title of the Seminar"" (title in 21pt bold TNR, rest 14pt TNR, centered, "No Spacing" style) → "Submitted to Savitribai Phule Pune University for the partial fulfillment of Under Graduate Degree in Information Technology" → "Presented By / Name of Student | PRN: 9999999" → "Guided By / Dr./Mr./Mrs. Guide Name" → SPPU seal + university logo images (centered) → "Department of Information Technology" (15pt bold) / "PVG's College of Engineering & S. S. Dhamankar Institute of Management, Nashik" (18pt bold) / "Academic Year 2026–27" (14pt bold).
- **Page 2 onward — body**, repeating the title block in miniature at the top of page 2 ("A Seminar / On / "Title of the Seminar"(...)"), then:
  1. **Abstract:** (14pt bold label) — body text 12pt, instructed 200–300 words.
  2. **Keywords:** (14pt bold-italic label) — instructed comma-separated, no bullets, 12pt.
  3. **1. Introduction** (14pt bold heading) — 12pt body.
     - **1.1. Motivation:** (14pt bold) — 12pt body, instructed in bullets.
     - **1.2. Objective:** (14pt bold) — 12pt body, instructed in bullets.
     - **1.3. Problem Statement:** (14pt bold) — 12pt paragraph.
  4. **2. Methodology / Prototype / Idea / Algorithm** (14pt bold) — 12pt body, instructed paragraph/bullets with IEEE citation, **must include a captioned figure** (sample: "Figure 3.1: Production of Pekilo Protein", caption style 10pt bold TNR, centered).
  5. **Expected Outcomes:** (12pt bold, note: smaller label size than other headings — template inconsistency, preserved as-is) — 12pt body.
  6. **Applications areas, if any:** (14pt bold) — appears here, **before** Conclusion (not after, as a naive read of "Applications" as a late section might assume).
  7. **3. Conclusion** (14pt bold) — 12pt body.
  8. **References** (14pt bold heading, no number prefix) — 12pt, numbered `[1] ... [5]` in the sample, un-bulleted hanging style.
  9. **Signature table** — a 2-row × 3-column borderless table: row 1 = "Dr. / Mr. / Mrs. [Guide name]" / "Ms. S. D. Pingale" / "Dr. S. R. Lahane"; row 2 (labels) = "Guide" / "Seminar Coordinator" / "Head". This table is fixed college-provided data (coordinator and HOD names are pre-filled) — only the Guide's name/title placeholder is student-editable.
- No explicit "Motivation:" bullet **sub-list** styling beyond "List Paragraph" style noted on one methodology placeholder — otherwise all section bodies use "No Spacing"/"Normal" styles, justified alignment.

### B.3 Explicit college requirements found in-file (not guessed)
- All red bracketed text ("(use font type & size Times New Roman 12)", "(...in Bullets)", "(...in bold italic keyword must separated by comma not in bullet)") is instructional and must be fully removed and replaced with real content honoring the stated font/size/style.
- Keywords: **comma-separated only, explicitly no bullets** — a common student error to avoid.
- The methodology section explicitly demands "(take the reference of IEEE base paper). Give citation for figure" and "Need a prototype / System diagram / flowchart / working model" — a figure is mandatory, not optional, and must be numbered/captioned/cited exactly as shown (e.g., "Figure 2.1: <caption> (Source: ...)").
- The signature block's Seminar Coordinator (Ms. S. D. Pingale) and Head (Dr. S. R. Lahane) names are **already fixed by the college in the template** — this matches the student-provided info (Prof. S. D. Pingale, Dr. S. R. Lahane) exactly, confirming no discrepancy.
- Sample figure and sample references (biotech "Single Cell Protein" content) are placeholder filler from a prior discipline's template reuse — entirely unrelated to any topic and must be fully replaced; nothing about their content should leak into the Agentic AI synopsis.
- There is **no separate "Related Work / Literature Survey" heading** in the synopsis (unlike the PPT) — literature is expected to be woven into Introduction/Methodology narrative with IEEE-style bracket citations `[1]`–`[n]`, consistent with the References section format already modeled.

---

## C. CROSS-DOCUMENT CONSISTENCY

| Item | PPT | Synopsis | Consistent? |
|---|---|---|---|
| Body font | Times New Roman | Times New Roman | ✅ |
| Citation style | Numbered `[1]`, IEEE-style | Numbered `[1]`, IEEE-style | ✅ |
| Guide/Coordinator/Head names | Not present in PPT template (title slide only has "Guide Name" placeholder) | Fixed: Pingale (Coordinator), Lahane (Head) | ✅ (use same names supplied by student on both) |
| Section count/order | 9 outline items (Intro w/ 3 sub-points, Related Work, Methodology, Implementation, HW/SW, Results, Conclusion, References) + numbering defect (Section A.4) | 3 numbered top-level sections (Intro w/ 3 sub-points, Methodology, Conclusion) + unnumbered Abstract/Keywords/Expected Outcomes/Applications/References | PPT is more granular (one slide per subsection) — expected, since a synopsis is compact prose and a PPT is one-idea-per-slide. Content must stay the *same story*, just re-partitioned. |
| Peach/orange accent visual identity | Yes (header bars, slide-number badge) | No color styling in docx (plain B/W academic doc, as expected for a Word template) | ✅ no conflict — synopsis is intentionally unstyled prose per college norms |

---

## D. STUDENT INFORMATION TO INSERT (from user instruction, not template)
- Name: **Korde Ayush Sandeep**, PRN **72406771M**, Roll No **32**
- Class: T.E. Information Technology, Semester I, AY **2026–27**
- Guide: **Prof. V. A. Khairnar**
- Seminar Coordinator: **Prof. S. D. Pingale** (matches template's pre-filled "Ms. S. D. Pingale")
- Head of Department: **Dr. S. R. Lahane** (matches template's pre-filled "Dr. S. R. Lahane")
- Topic: **"Agentic AI: Autonomous Goal-Oriented Intelligent Systems for Planning, Reasoning and Task Execution"**

---

## E. TEMPLATE COMPLIANCE RULES DERIVED (binding for Phase 1B/1C)

1. Never alter slide master/layouts, theme colors, header-bar treatment, footer text/color, border frame, or slide-number badge — copy them slide-by-slide as new content is added.
2. Never alter section-page geometry, margins, footer text, or the fixed signature table in the synopsis.
3. Font/size table to follow exactly (no deviation without a stated reason):
   - PPT banner: Arial Narrow, 36pt, bold, black.
   - PPT body: Times New Roman; 21pt bullets, 24pt sub-headings, 15pt references, 12pt captions.
   - Synopsis headings: Times New Roman 14pt bold; body 12pt; figure captions 10pt bold; title-page title 21pt bold.
4. All red bracketed instructional text is removed in the final files — none may survive into `05_FINAL/`.
5. New slides/sections not in the original 12-slide/4-page skeleton (Research Gap, Challenges/Limitations, Evaluation Framework) must visually match existing slides pixel-for-pixel in banner/footer/font/color treatment.
6. Diagrams use the template's warm earth-tone accent palette (`#D34817` primary, plus the five secondary accents/greys listed in A.2), not a blue/tech or AI-glow palette — per the supplemental visual instructions.
7. The Outline slide's numbering defect (A.4) will be corrected to a clean sequential 1–9 in the working copy, flagged to the student as a deliberate deviation from the literal (buggy) college file — this is the one place "fix" vs "preserve" needs explicit sign-off (see Section G).

---

## F. FILE INVENTORY CREATED THIS PHASE

```
01_OFFICIAL/
  TE SEMINAR Presentation PPT FORMAT.ppt      (untouched original copy)
  Seminar Synopsis-2026-27.docx                (untouched original copy)
03_RESEARCH/
  OFFICIAL_PPT_INSPECT.pptx                    (COM-converted, inspection only)
  OFFICIAL_PPT_INSPECT.pdf                     (rendered, inspection only)
  OFFICIAL_SYNOPSIS_INSPECT.pdf                (rendered, inspection only)
  slide_images/Slide1.PNG ... Slide12.PNG      (rendered slide previews)
06_REPORTS/
  TEMPLATE_AUDIT.md                            (this file)
```

---

## G. OPEN ITEMS — RESOLVED (student decisions, 2026-09-22)

1. **Outline numbering fix (A.4):** ✅ **APPROVED — expand to ~20 slides, clean sequential numbering.** Final section sequence: 1 Title, 2 Outline, 3 Introduction, 4 Motivation, 5 Objectives, 6 Problem Statement, 7 Related Work/Literature Survey, 8 Research Gap, 9 Proposed Methodology, 10 Proposed Agentic AI Architecture, 11 Working Flow, 12 Agentic AI Algorithm, 13 Implementation Details/Conceptual Prototype, 14 Hardware/Software Specification, 15 Evaluation Framework, 16 Applications, 17 Challenges & Limitations, 18 Conclusion & Future Work, 19 References, 20 Thank You. All new slides reuse the exact banner/footer/font/border/badge treatment from the original 12-slide file (Section E).
2. **Title-slide banner label:** ✅ **APPROVED — keep verbatim.** "A Seminar Review I Presentation on" stays exactly as in the official template.
3. **PRN format:** ✅ Confirmed — use **72406771M** exactly as given.

Everything else in this audit is read directly from the files, not guessed.

---

**Phase 1A approved. Proceeding to Phase 1B (literature research and content development).**
