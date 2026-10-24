# FINAL DOCUMENT AUDIT — Phase 2 Checkpoint

Topic: **"Agentic AI: Autonomous Goal-Oriented Intelligent Systems for Planning, Reasoning and Task Execution"**
Student: Korde Ayush Sandeep | PRN 72406771M | Roll 32 | T.E. IT, Sem I, AY 2026–27
Guide: Prof. V. A. Khairnar | Coordinator: Prof. S. D. Pingale | HOD: Dr. S. R. Lahane

---

## What was created

| Deliverable | Location | Status |
|---|---|---|
| Template audit | [TEMPLATE_AUDIT.md](TEMPLATE_AUDIT.md) | Done, approved by student |
| Verified literature | [03_RESEARCH/LITERATURE.md](../03_RESEARCH/LITERATURE.md) | 7 papers, all web-verified |
| Content master (source of truth for both documents) | [02_WORKING/CONTENT_MASTER.md](../02_WORKING/CONTENT_MASTER.md) | Done |
| Final PPT | [05_FINAL/Agentic_AI_Technical_Seminar_FINAL.pptx](../05_FINAL/Agentic_AI_Technical_Seminar_FINAL.pptx) | Done |
| Final Synopsis (Word) | [05_FINAL/Agentic_AI_Seminar_Synopsis_FINAL.docx](../05_FINAL/Agentic_AI_Seminar_Synopsis_FINAL.docx) | Done |
| Final Synopsis (PDF) | [05_FINAL/Agentic_AI_Seminar_Synopsis_FINAL.pdf](../05_FINAL/Agentic_AI_Seminar_Synopsis_FINAL.pdf) | Done |
| PPT review | [PPT_REVIEW.md](PPT_REVIEW.md) | Done |
| Synopsis review | [SYNOPSIS_REVIEW.md](SYNOPSIS_REVIEW.md) | Done |
| Prototype | *(not started — Phase 3, gated on this checkpoint's approval)* | Not started |

## Slide count / page count
- **PPT: 20 slides** (official template was 12; expanded per student-approved plan in [TEMPLATE_AUDIT.md](TEMPLATE_AUDIT.md) Section G).
- **Synopsis: 6 pages** (official template was 4; growth from the mandatory figure, bulleted motivation/objective lists, and 7 full IEEE-style references vs. the original 5 short samples).

## Template compliance
Both documents were built by duplicating the official template's own slides/paragraphs (never redesigned) and inserting real content into them. Visual identity preserved exactly: PPT banner/border/footer/page-number badge/theme colors; Synopsis page geometry/margins/footer/signature table. All red instructional placeholder text was removed from both documents; a full-document/full-deck programmatic scan for leftover placeholder or sample-content strings returned zero matches in both files. Full detail in [PPT_REVIEW.md](PPT_REVIEW.md) and [SYNOPSIS_REVIEW.md](SYNOPSIS_REVIEW.md), including the QA bugs found and fixed during the build (bullet-glyph XML ordering bug, diagram arrow routing, spurious auto-numbering, double reference brackets).

## Literature sources used
7 papers, all individually web-verified (author list, venue, year, DOI/arXiv ID) on 2026-09-22 — see [LITERATURE.md](../03_RESEARCH/LITERATURE.md):
1. Acharya, Kuppan & Divya (2025), IEEE Access — Agentic AI survey
2. Dong et al. (2024), IEEE AIoTC Conf. — LLM-based agents survey
3. Wang et al. (2024), Frontiers of Computer Science — LLM autonomous agents survey
4. Yao et al. (2023), ICLR — ReAct
5. Li et al. (2024), Vicinagearth — LLM multi-agent systems survey
6. Gan et al. (2024), arXiv / ACM TOSEM (in press) — security/privacy/ethics threats in LLM agents
7. Lewis et al. (2020), NeurIPS — Retrieval-Augmented Generation

One correction was made during verification: the master instruction's draft title for [6] omitted the word "Ethics" — the verified real title includes it, and the correct title is used throughout.

## Research gap
> Existing research addresses planning, memory, retrieval, tool use, multi-agent collaboration, and security/privacy risk as individual, separately-studied components [1]–[3][5][6]. Reliable integration of these capabilities with an explicit pre-action risk gate, bounded human oversight, and post-action verification — inside one demonstrable control loop — remains an open, under-addressed design and evaluation challenge.

## Proposed architecture
A 5-layer architecture (Input → Planning & Reasoning → Knowledge & Tools → Safety & Oversight → Execution & Verification) with an explicit bounded retry loop from Verification back to the Planner, and a pre-action Human Approval gate that sits *before* execution (never after a risky action has already run). Rendered as native, editable PowerPoint/Word vector shapes in the template's own color palette — not an AI-generated image. A companion "Working Flow" diagram shows the same logic as a step-by-step flowchart with explicit decision diamonds. Both are original diagrams, captioned "Author's proposed architecture/workflow" and cited to the synthesizing literature.

## Unresolved limitations (stated openly in both documents, not hidden)
- No experiment has been run; the Evaluation Framework lists **proposed** metrics only, explicitly labeled "not yet measured."
- The Phase 3 prototype does not exist yet — the Implementation Details slide and synopsis Methodology section describe *planned* scope only, with an explicit disclaimer that claims will be updated once Phase 3 is built.
- This seminar's own evaluation is structural/qualitative, not a controlled experiment — stated as a limitation on the Challenges slide.
- Multi-agent extension is explicitly out of scope (deferred to future work), to keep the seminar's claims matched to what is actually proposed.

## Items requiring student approval before Phase 3 (prototype)
1. **Confirm the PPT and synopsis content above is accurate and ready to submit** — in particular the abstract, research gap wording, and the architecture/working-flow diagrams, since these are the seminar's core intellectual content.
2. **Confirm the Phase 3 prototype scope** described in the Implementation Details slide/synopsis section (small RAG index, 2–3 safe non-destructive tools, bounded retry, one mock high-risk action requiring approval) is what you want built, or specify changes before implementation starts.
3. **LLM API choice for the prototype** — the seminar currently says "LLM API (used only in the Phase 3 prototype)" without committing to a specific provider; confirm which API/key you'll supply, or whether the prototype should use a fully local/offline stand-in instead (affects the `.env.example` and setup instructions Phase 3 will produce).

## Recommended presentation speaking time
20 slides, ≈35–45 seconds average per slide → **11–14 minutes**, within the stated 10–15 minute target. Slides most likely to need practice for timing: Proposed Architecture, Working Flow, and Algorithm (denser content, ~60–75 seconds each is realistic).

---

**STOP — Phase 1 (PPT + Synopsis) and Phase 2 (review) are complete. Awaiting your approval of this audit before starting Phase 3 (prototype).**
