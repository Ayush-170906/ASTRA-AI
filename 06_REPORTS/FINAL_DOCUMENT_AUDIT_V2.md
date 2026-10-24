# FINAL DOCUMENT AUDIT V2 — Phase 2 Corrections

This supersedes [FINAL_DOCUMENT_AUDIT.md](FINAL_DOCUMENT_AUDIT.md) (Round 1). It documents the 9 corrections
requested by the student after independently reviewing the rendered Round-1 PPT and synopsis, all applied
to the same files in `02_WORKING/` and re-published to `05_FINAL/`. **Phase 3 (prototype) was not started.**

---

## 1. CRITICAL — Synopsis figure error (CONFIRMED AND FIXED)

The student's report was correct and this was a real defect, not a false alarm. Root cause: when the
Figure 2.1 image was replaced in Phase 1, the **old unrelated "Pekilo Protein" fermentation-diagram image
was never deleted** — it was left sitting in a separate paragraph immediately after the new architecture
image, so the document rendered *both* images in sequence (correct one, then the leftover one), with the
caption text landing directly under the wrong image. This was missed during the original QA pass because
that pass read the PDF's extracted text (which looked correct) without scrutinizing the second embedded
image closely enough.

**Fix:** the leftover image paragraph (and two now-unneeded blank spacer paragraphs around it) were deleted
entirely. The synopsis now contains exactly two images: the SPPU/university seal on the title page, and
the one correct Figure 2.1 (Proposed reliability-oriented Agentic AI architecture) in Section 2 — verified
by an automated count (`2` images found, matching the expected `2`) and a full visual re-render of every
page (see Section 9 below).

## 2. Reference [6] — corrected to the verified 2026 ACM publication

Independently verified via the **Crossref API** (`api.crossref.org/works/10.1145/3807666`), which is the
DOI registration agency's own metadata record — not ACM's own page, which still blocks automated fetches.
Crossref confirms:
- **Title:** "Navigating the Risks: A Survey of Security and Privacy Threats in LLM-Based Agents" (the
  published ACM title drops "and Ethics" relative to the original arXiv preprint — same underlying paper).
- **All 13 authors**, in order: Yuyou Gan, Yong Yang, Zhe Ma, Ping He, Rui Zeng, Yiming Wang, Qingming Li,
  Chunyi Zhou, Songze Li, Ting Wang, Yunjun Gao, Yingcai Wu, Shouling Ji.
- **Venue:** ACM Transactions on Software Engineering and Methodology.
- **Online-publication date:** 2026-05-07 (confirms year **2026**, matching the student's correction).
- **DOI:** 10.1145/3807666 (matches the student's correction exactly).
- No volume/issue/page number exists yet in the Crossref record — consistent with an ACM "just accepted" /
  online-first article; none is fabricated.

Updated everywhere the citation appears: PPT References slides (now split, see §5), PPT Related Work
table, synopsis References list, and both `03_RESEARCH/LITERATURE.md` and `02_WORKING/CONTENT_MASTER.md`
(the source-of-truth documents), with a revision-history note explaining the change from the 2024 arXiv
preprint to the 2026 ACM version.

## 3–5. Literature slide, Algorithm slide, References — split/redesigned for readability

- **Literature Survey**: split into two slides (refs [1]–[4], then [5]–[7]), same banner text repeated on
  both (matching the template's own established convention of repeating a section banner across multiple
  slides, already used for "1. Introduction" across 4 slides). Font increased from 11–12pt to 14–15pt.
- **Algorithm**: the dense 22-line pseudocode textbox was removed entirely and replaced with a native
  PowerPoint box-and-arrow flow diagram (no image, fully editable), following the exact sequence
  requested: **Plan → Retrieve → Select Tool → Risk Check → Human Approval (if High Risk) → Execute →
  Observe → Verify → Bounded Retry → Escalate/Return**, laid out as two rows of five boxes at 13.5pt with
  a wrap-around arrow between rows and a dashed bounded-retry loop-back arrow to "Plan," routed clear of
  the wrap-around arrow (an initial version had the two arrows overlapping on the same column, which was
  caught and fixed during this round's visual QA).
- **References**: split into two slides (refs [1]–[4], then [5]–[7]), same banner repeated, font increased
  from 15pt to 17pt with more paragraph spacing.

PPT slide count: **12 (official) → 20 (Round 1) → 22 (Round 2)**, all 3 new slides (1 literature split + 1
references split) built by duplicating an existing slide's shapes — never a new design — and the Algorithm
slide's content was rebuilt in place (same slide, same banner/footer/border) without changing slide count.

## 6. Title slide spacing — a real defect was found and fixed, not just cosmetics

Investigating "improve spacing" surfaced a genuine content-hiding bug, not merely tight spacing: the title
banner ("Rectangle 7") was resized in Round 1 to hold a two-line seminar title, but its fixed height (0.65in,
inherited from the official template, which only ever held a one-line title) was **never increased** to
match. Because a sibling shape ("Title 1," containing "Submitted to Savitribai Phule Pune University / for
the partial fulfillment of Under Graduate Degree in / Department of Information Technology") draws
*underneath* the banner in z-order and its text naturally flowed into that same vertical region, those
three lines were **fully hidden behind the opaque banner** in the Round-1 file — invisible on the rendered
slide, though present in the underlying XML. This existed in the PPT sent to the student and was not caught
by Round 1's QA screenshots, which is exactly why the student's independent review was valuable here.

**Fix:** the banner rectangle's height was increased (0.65in → 1.05in, same width/position/fill/border —
not redesigned) to fully contain its two-line title, and the paragraph immediately above it in the body
textbox was given enough trailing space to push "Submitted to..." below the now-taller banner. Re-rendered
and visually confirmed all three previously-hidden lines are now fully visible with clean, even spacing.

## 7. Research Gap / Problem Statement wording — absolute claim replaced

The phrase **"there is no widely taught, minimal reference architecture that integrates..."** was an
absolute, unfalsifiable negative-existence claim (a literature review cannot actually verify the non-
existence of something across all of academia/industry). Replaced everywhere it appeared — PPT Problem
Statement slide, synopsis "1.3. Problem Statement," `LITERATURE.md`, and `CONTENT_MASTER.md` — with the
student-suggested, defensible formulation:

> "A practical gap remains in integrating these capabilities into a minimal, teachable reference
> architecture that combines pre-action risk assessment, bounded human oversight, and post-action
> verification in one demonstrable control loop."

This claims only what the 7-paper literature review actually supports.

## 8. Synopsis page count — re-evaluated and compressed

6 pages → **5 pages**. After removing the leftover image (§1), page 6 held only the signature table on an
otherwise blank page. Rather than leaving that waste, excessive blank-paragraph runs between sections
(several 2–4-blank-line gaps left over from the template's own original spacing) were trimmed down to a
single blank line each — a purely spacing-level change, no content or section was removed, and no section
was made harder to read (re-verified visually, see §9). This pulled the signature table back onto the same
page as the end of the References list, eliminating the near-empty trailing page.

## 9. Visual QA performed after all corrections

- **Full PPT re-render**: all 22 slides exported as images and inspected. Confirmed: title slide's
  previously-hidden text now visible with correct spacing; Problem Statement and Research Gap wording
  updated; both split Literature slides render cleanly with larger, readable text and no unrelated
  imagery; both split References slides render cleanly at 17pt; the Algorithm flow diagram's two arrows
  (wrap-around and retry-loop) are now visually distinct (an overlap bug from the first build attempt was
  caught and fixed in this same session); Architecture/Working Flow diagrams, Evaluation table, and
  Thank You slide are unaffected and still correct; page-number badges auto-updated correctly on every
  slide (verified 9, 11, 16, 22 spot-checked against their new positions).
- **Full synopsis re-render**: all 5 pages inspected. Confirmed exactly one figure (the correct
  architecture diagram) with the correct caption directly beneath it; corrected reference [6]; corrected
  Problem Statement wording; signature table intact; no clipped text, no orphaned headings, no tiny text.
- **Programmatic full-text scans** (both files) for: the old absolute claim, the old arXiv ID, the old
  "Security, Privacy, and Ethics" title, "Pekilo"/"Waites" sample content, the old "arXiv / ACM TOSEM"
  venue string, and "Gan et al., 2024" — **zero hits in both files**.
- **Image count check** (synopsis): exactly 2 images found (title-page seal, architecture figure) —
  matches expectation exactly.

---

## Reported figures

**Exact PPT slide count: 22**
**Exact synopsis page count: 5**

**Corrected reference list (all 7, as they now appear in both documents):**
1. D. B. Acharya, K. Kuppan, and B. Divya, "Agentic AI: Autonomous Intelligence for Complex Goals — A Comprehensive Survey," IEEE Access, vol. 13, pp. 18912–18936, 2025.
2. X. Dong, X. Zhang, W. Bu, D. Zhang, and F. Cao, "A Survey of LLM-based Agents: Theories, Technologies, Applications and Suggestions," in Proc. 3rd Int. Conf. Artificial Intelligence, Internet of Things and Cloud Computing Technology (AIoTC), 2024, pp. 407–413.
3. L. Wang, C. Ma, X. Feng, et al., "A survey on large language model based autonomous agents," Frontiers of Computer Science, vol. 18, no. 6, p. 186345, 2024.
4. S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, "ReAct: Synergizing Reasoning and Acting in Language Models," in Proc. ICLR, 2023.
5. X. Li, S. Wang, S. Zeng, Y. Wu, and Y. Yang, "A survey on LLM-based multi-agent systems: workflow, infrastructure, and challenges," Vicinagearth, vol. 1, no. 1, art. 9, 2024.
6. **Y. Gan, Y. Yang, Z. Ma, P. He, R. Zeng, Y. Wang, Q. Li, C. Zhou, S. Li, T. Wang, Y. Gao, Y. Wu, and S. Ji, "Navigating the Risks: A Survey of Security and Privacy Threats in LLM-Based Agents," ACM Transactions on Software Engineering and Methodology, 2026, doi: 10.1145/3807666.** *(corrected this round, Crossref-verified)*
7. P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in Proc. NeurIPS, 2020.

**Confirmation every synopsis figure is relevant:** Yes. The synopsis contains exactly two images: (1) the
official SPPU seal + university emblem on the title page (unchanged, part of the official template), and
(2) Figure 2.1, the proposed Agentic AI architecture diagram — the same diagram used on PPT slide 11,
cropped to remove slide chrome, captioned and cited correctly. The previously-present unrelated fermentation
diagram has been completely removed and no longer exists anywhere in the file.

## Remaining issues, if any

None found in this round's scans and visual review. Two items from Round 1 remain open and are unrelated to
this round's corrections — carried forward for the student's decision before Phase 3:
1. **Prototype scope confirmation** (small RAG index, 2–3 safe tools, bounded retry, one mock high-risk
   action) — as drafted in Round 1, not yet confirmed.
2. **LLM API choice for the prototype** — local/offline-capable design recommended in Round 1, with an
   optional real LLM API if the student supplies a key; not yet decided.

---

**STOP — awaiting student approval of this V2 audit. Phase 3 (prototype) has not been started.**
