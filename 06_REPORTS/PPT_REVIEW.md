# PPT REVIEW — Template Compliance & Content Mapping

Source: [05_FINAL/Agentic_AI_Technical_Seminar_FINAL.pptx](../05_FINAL/Agentic_AI_Technical_Seminar_FINAL.pptx)
built from [01_OFFICIAL/TE SEMINAR Presentation PPT FORMAT.ppt](../01_OFFICIAL/TE%20SEMINAR%20Presentation%20PPT%20FORMAT.ppt)
(untouched original, never opened for editing).

Format: **ORIGINAL TEMPLATE ELEMENT → PROPOSED CONTENT → WHY THE CHANGE IS REQUIRED → WHAT REMAINS UNCHANGED**

---

### 1. Slide geometry, border, banner, footer, page-number badge
→ Reused byte-for-byte on every slide (copied via slide-duplication, not redrawn).
→ Required so the deck stays visually identical to the official 12-slide file at 20 slides.
→ **Unchanged:** 13.33×7.5in size, black rounded-rect border, peach header banner (`accent1` @ 40/60 tint), Arial Narrow 36pt bold banner text, purple (`#7030A0`) Arial Narrow 12pt footer, orange oval page-number badge.

### 2. Red instructional placeholder text (e.g. "(use font type & size Times New Roman 21)")
→ Deleted everywhere; replaced with real content set to the exact font/size the instruction specified.
→ Required — the official rule is these notes must never survive into a submitted deck.
→ **Unchanged:** the font/size values the instructions specified are the values actually used (TNR 21pt body, 24pt sub-heads, 15pt references, 12pt captions).

### 3. Outline slide's own numbering defect (duplicate "4"/"5")
→ Replaced with a clean sequential 1–14 section list (approved by student, see [TEMPLATE_AUDIT.md](TEMPLATE_AUDIT.md) Section G).
→ Required because the official file's own numbering repeats "4. Conclusion" and "5. References" out of order — reproducing the bug would misrepresent the seminar structure.
→ **Unchanged:** the Outline slide's own visual style (banner, square Wingdings bullets, TNR 21pt bold).

### 4. 12-slide skeleton → 20 slides
→ Added 8 new content slides (Research Gap, Proposed Architecture, Working Flow, Algorithm, Implementation/Prototype, Evaluation Framework, Applications, Challenges & Limitations), each built by duplicating an existing template slide's shape set, never a new design.
→ Required per the master instruction's suggested structure and the student's explicit approval to expand from 12→~20 slides.
→ **Unchanged:** every new slide reuses the same banner rectangle, footer, page-number badge, border, and font rules as the original 12.

### 5. Title slide
→ "A Seminar Review I Presentation on" kept verbatim (student-approved); title replaced with the approved topic; student name/PRN/guide filled in red bold TNR exactly matching the original template's convention of showing these fields in red.
→ Required to instantiate the template with this seminar's actual data.
→ **Unchanged:** SPPU seal + university logo images, layout, purple Academic-Year line.

### 6. Related Work / Literature Survey slide
→ Converted from a free-text placeholder into a 5-column native PowerPoint table (Ref / Author,Year / Venue / Contribution / Relevance-Limitation) for all 7 verified references, colored with the template's own `accent1` palette for the header row and alternating tint for readability.
→ Required by the supplemental instruction: "the literature survey must not look like a randomly generated table" and must stay legible on one slide (7 rows fit without shrinking text below 11pt).
→ **Unchanged:** banner/footer/border style; body font family (Times New Roman) for cell text.

### 7. Proposed Agentic AI Architecture (new diagram slide) and Working Flow (new diagram slide)
→ Built as native PowerPoint rectangles/diamonds/connectors (no raster image, no AI-generated artwork), colored entirely from the template's own theme accents (`accent1 #D34817`, `accent2 #9B2D1F`, tints thereof, and the theme's neutral `lt2 #E9E5DC`), with a caption crediting "Author's proposed architecture / workflow" and citing [1][2][4][6][7] for the concepts synthesized.
→ Required by both the master instruction (a system diagram is mandatory) and the supplemental visual instructions (handcrafted academic style, template color reuse, no AI-glow decoration, clear pre-action-safety vs. post-action-verification separation, bounded retry loop never placed after a risky action already executed).
→ **Unchanged:** banner/footer/border/page-number treatment identical to every other content slide; caption typography (TNR bold, centered) matches the original figure-caption convention seen on the Methodology slide.

### 8. Agentic AI Algorithm slide
→ Pseudocode (`BoundedAgenticLoop`) set in Consolas monospace at 13.5pt to fit ~22 lines legibly.
→ Required to state a technically correct, provably-terminating bounded loop (explicit `MAX_RETRIES`), addressing the master instruction's "never create an infinite retry loop" rule.
→ **Unchanged:** banner/footer/border.

### 9. Evaluation Framework slide
→ Native table of 8 proposed metrics, each captioned "not yet measured", with an explicit purple italic note: "No experiment has been performed yet — these are proposed metrics..."
→ Required by the master instruction's zero-fabrication rule — no percentages, no invented results.
→ **Unchanged:** table color scheme reuses the Related-Work table's palette for visual consistency across the deck.

### 10. References slide
→ All 7 sample/unrelated biotech references removed; replaced with the 7 web-verified Agentic AI references (IEEE format, 15pt TNR, matching the original reference-slide font size).
→ Required — the original references were unrelated filler content from a different discipline's template reuse.
→ **Unchanged:** numbered `[n]` bracket style, 15pt TNR, banner "References" treatment.

### 11. Thank You slide
→ Left completely untouched (including the small stick-figure clipart already in the official template).
→ No change needed — nothing on this slide referenced content, and the master instruction says not to introduce new decorative graphics.
→ **Unchanged:** entire slide, pixel-for-pixel.

---

## QA fixes applied during build (not visible in the content itself, but material to submission quality)
- Fixed an inherited-bullet XML ordering bug (`<a:defRPr/>` appearing before `<a:buChar>`) that silently suppressed the bullet glyph on the first bullet of several slides — affected 13 paragraphs across the deck, now all render correctly.
- Fixed the retry-loop arrow on the Architecture slide, which initially routed straight through the Human Approval box; re-routed around the right margin.
- Fixed overlapping arrows/labels on the Working Flow slide (Approved-path arrow crossing the Terminate-Safely box; retry-loop dashed line crossing the Verify-Result box); both re-routed through empty margin space.
- Fixed a caption/footer text overlap on the Working Flow slide by repositioning the caption above the footer band.

## Full-deck scan result
A programmatic scan of every shape's text on all 20 slides for leftover instructional phrases ("use font type", "Should be", "Must about", sample biotech content, "XYZ", "9999999", etc.) returned **zero matches** — no placeholder or sample content survives into the final file.

## Presentation timing estimate
20 slides at ~35–45 seconds average (title/outline/thank-you faster, diagram/algorithm slides slower) ≈ **11–14 minutes**, within the 10–15 minute target.
