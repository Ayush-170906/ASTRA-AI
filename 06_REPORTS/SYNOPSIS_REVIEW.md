# SYNOPSIS REVIEW — Template Compliance & Content Mapping

Source: [05_FINAL/Agentic_AI_Seminar_Synopsis_FINAL.docx](../05_FINAL/Agentic_AI_Seminar_Synopsis_FINAL.docx)
built from [01_OFFICIAL/Seminar Synopsis-2026-27.docx](../01_OFFICIAL/Seminar%20Synopsis-2026-27.docx)
(untouched original, never opened for editing).

Format: **ORIGINAL TEMPLATE ELEMENT → PROPOSED CONTENT → WHY THE CHANGE IS REQUIRED → WHAT REMAINS UNCHANGED**

---

### 1. Page setup (8.5×11in, 1in margins, footer "Dept | PVG's COE&SSDIOM, Nashik — Page X | N")
→ Not touched at all; only body content was edited in place.
→ No change needed.
→ **Unchanged:** section/page geometry, header/footer distance, footer text and its page-count field (auto-updates to the new 6-page length).

### 2. Title page (page 1) and mini title-block (top of page 2)
→ "Title of the Seminar" → the approved topic (in curly quotes, 18pt/16pt bold, matching the template's own 21pt title convention scaled to fit two lines); "Name of Student | PRN" → "Korde Ayush Sandeep | PRN: 72406771M"; "Dr./Mr./Mrs. Guide Name" → "Prof. V. A. Khairnar".
→ Required to instantiate the template with this seminar's actual data.
→ **Unchanged:** SPPU seal + university logo images, "Submitted to Savitribai Phule Pune University..." line, Department/College/Academic-Year lines (already correct in the template), page layout and centering.

### 3. Abstract
→ Red instruction removed; replaced with a 220–260 word abstract (within the template's stated 200–300 word target) at 12pt TNR justified, matching the "Abstract:" 14pt bold label style already in the template.
→ Required — the abstract must describe the actual seminar content, not the instructional placeholder.
→ **Unchanged:** "Abstract:" heading style/size, paragraph justification.

### 4. Keywords
→ Red instruction removed; replaced with 12 comma-separated keywords in bold italic, **no bullets** (matching the template's explicit instruction "keyword must separated by comma not in bullet").
→ Required by the template's own stated rule.
→ **Unchanged:** "Keywords:" bold-italic label style.

### 5. 1. Introduction / 1.1 Motivation / 1.2 Objective / 1.3 Problem Statement
→ Introduction and Problem Statement written as flowing paragraphs (no bullets, per template); Motivation (3 points) and Objective (5 points) converted to genuine bulleted lists using the "List Paragraph" style with a manual bullet glyph and hanging indent, since the template defines no built-in "List Bullet" style — required because the template's own red instruction explicitly says "(...in Bullets)" for these two subsections only.
→ Required to satisfy the template's own formatting rule while keeping Introduction/Problem Statement as plain paragraphs as instructed.
→ **Unchanged:** the "1.", "1.1.", "1.2.", "1.3." numbering is Word's own auto-numbering field on the heading paragraphs (`numPr`), never touched — only the heading and body text runs were edited.

### 6. 2. Methodology / Prototype / Idea / Algorithm (+ mandatory figure)
→ Five-point bulleted approach summary (Goal Understanding → Task Decomposition & Planning → Knowledge Grounding → Pre-Action Risk Gate → Post-Action Verification), followed by a transition sentence, the proposed architecture figure, and a properly formatted caption: "**Figure 2.1**: Proposed reliability-oriented Agentic AI architecture. ... Source: Author's proposed architecture, synthesized from [1], [2], [4], [7] and the risk taxonomy in [6]."
→ Required — the template explicitly demands "a prototype / System diagram / flowchart / working model" with a cited, numbered figure; the original sample figure (an unrelated biotech "Pekilo Protein" diagram) had to be fully replaced.
→ **Unchanged:** the figure is centered, sized to page width (6.3in, well inside the 6.5in text width), with a 10pt bold caption directly beneath it — the same caption position/size/weight the original template used for its own sample figure.
→ **Attribution discipline:** the caption explicitly says "Author's proposed architecture" (never presented as another researcher's figure), per the supplemental instruction's diagram-attribution rule.

### 7. Expected Outcomes / Applications areas, if any
→ Rewritten using "evaluate / propose / demonstrate / assess"-style wording, explicitly avoiding any invented percentage or unperformed-experiment claim.
→ Required by the master instruction's zero-fabrication rule.
→ **Unchanged:** heading style/order relative to Methodology and Conclusion (Expected Outcomes and Applications sit between Methodology and Conclusion, exactly as in the official template — this is *not* the order a naive reading of the master instruction's checklist would suggest, but it is what the official file's own structure requires, so the official file's order wins).

### 8. 3. Conclusion
→ Replaced with a real conclusion tied back to the stated research gap and future work (completing the Phase 3 prototype, multi-agent extension, empirical evaluation).
→ Required.
→ **Unchanged:** numbered heading style (Word auto-number field, untouched).

### 9. References
→ All 5 sample biotech references replaced with the 7 web-verified Agentic AI references; 2 additional reference paragraphs were added (copying the existing reference paragraph's formatting) since the template only pre-provisioned 5 placeholder slots for 7 needed entries.
→ Required — the sample references were entirely unrelated filler.
→ **Unchanged:** the `[n]` numbering is the template's own Word auto-number field (`numPr`) — during the build this was briefly double-printed ("[1] [1] ...") because the reference text also carried a manual "[1]" prefix; this was caught during QA and fixed by stripping the manual prefix so the template's own auto-number is the only numbering shown, exactly as the original 5 sample references did.

### 10. Signature table (Guide / Seminar Coordinator / Head)
→ Only the "Dr. / Mr. / Mrs." Guide cell was changed, to "Prof. V. A. Khairnar".
→ Required — this is the one student-editable cell.
→ **Unchanged:** "Ms. S. D. Pingale" (Seminar Coordinator) and "Dr. S. R. Lahane" (Head) — these were already correctly pre-filled by the college in the official template and match the student-provided names exactly, confirmed with no discrepancy.

---

## QA fixes applied during build
- **Numbering leak**: the Problem Statement body paragraph, when inserted after the "1.3. Problem Statement:" heading, inherited that heading's auto-number field and rendered as a spurious "1.4." — fixed by stripping `numPr`/`ind` from the body paragraph so only the heading is numbered.
- **Double reference brackets**: reference paragraphs render `[n]` via the template's own auto-number field; the drafted reference text also included a literal `[n]` prefix, producing "[1] [1] ...". Fixed by stripping the manual prefix from all 7 entries.
- **Leftover instructional paragraph**: a standalone red-text instruction paragraph in the Methodology section ("Should be in paragraph or in bullet form...") was not part of the body paragraph replaced earlier and was found by a full-document scan; deleted.

## Full-document scan result
A programmatic scan of every paragraph for leftover instructional phrases, sample-content fragments ("Pekilo", "Waites", "9999999", "Name of Student", "Guide Name", "Title of the Seminar", etc.) returned **zero matches** after the fixes above.

## Page count
**6 pages** (official template was 4 pages before this seminar's content was added; growth is expected and appropriate given the added figure, bulleted objectives/motivation, and 7 full references vs. the original 5 short sample ones).
