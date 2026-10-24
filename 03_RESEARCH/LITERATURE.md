# Verified Literature — Agentic AI Seminar

All entries below were verified via live web search on 2026-09-22 (author list, venue, year, DOI/arXiv ID
cross-checked against the publisher or arXiv page). No fabricated DOIs, page numbers, or venues.

## [1] Acharya, Kuppan & Divya (2025) — Agentic AI survey (primary framing paper)
**Acharya, D. B., Kuppan, K., & Divya, B.** (2025). "Agentic AI: Autonomous Intelligence for Complex
Goals — A Comprehensive Survey." *IEEE Access*, 13, 18912–18936.
DOI: 10.1109/ACCESS.2025.3532853
Use for: defining Agentic AI, contrasting with traditional/generative AI, goal-directed autonomy framing.

## [2] Dong et al. (2024) — LLM-based agents: theories/technologies/applications
**Dong, X., Zhang, X., Bu, W., Zhang, D., & Cao, F.** (2024). "A Survey of LLM-based Agents: Theories,
Technologies, Applications and Suggestions." *2024 3rd International Conference on Artificial
Intelligence, Internet of Things and Cloud Computing Technology (AIoTC)*, pp. 407–413.
DOI: 10.1109/AIoTC63215.2024.10748304
Use for: LLM-as-controller framing (perception, memory, planning, action execution).

## [3] Wang et al. (2024) — LLM-based autonomous agents survey
**Wang, L., Ma, C., Feng, X., et al.** (2024). "A survey on large language model based autonomous
agents." *Frontiers of Computer Science*, 18(6), 186345.
DOI: 10.1007/s11704-024-40231-1
Use for: unified construction framework for LLM agents; applications across social science/natural
science/engineering.

## [4] Yao et al. (2023) — ReAct
**Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y.** (2023). "ReAct:
Synergizing Reasoning and Acting in Language Models." *ICLR 2023*. arXiv:2210.03629.
Use for: the reasoning+acting interleaving pattern that underlies the planning/execution loop; short
attributed tagline permitted: ReAct — "Reasoning + Acting" [4].

## [5] Li et al. (2024) — LLM-based multi-agent systems
**Li, X., Wang, S., Zeng, S., Wu, Y., & Yang, Y.** (2024). "A survey on LLM-based multi-agent systems:
workflow, infrastructure, and challenges." *Vicinagearth*, 1(1), Article 9.
DOI: 10.1007/s44336-024-00009-2
Use for: multi-agent workflow/infrastructure vocabulary, mentioned in Related Work / Research Gap as an
axis largely orthogonal to single-agent reliability (motivates why this seminar scopes to a single
reliability-oriented agent loop rather than multi-agent orchestration).

## [6] Gan et al. (2026) — Security/privacy threats in LLM agents (ACM TOSEM, published version)
**Gan, Y., Yang, Y., Ma, Z., He, P., Zeng, R., Wang, Y., Li, Q., Zhou, C., Li, S., Wang, T., Gao, Y.,
Wu, Y., & Ji, S.** (2026). "Navigating the Risks: A Survey of Security and Privacy Threats in
LLM-Based Agents." *ACM Transactions on Software Engineering and Methodology*.
DOI: 10.1145/3807666.
Verified independently via the Crossref API (`api.crossref.org/works/10.1145/3807666`) on 2026-09-23,
since ACM's own page (dl.acm.org) blocks automated fetches — Crossref is the DOI registration agency's
own metadata record, confirming: title (note — the published ACM title drops "and Ethics" relative to
the original 2024 arXiv preprint, arXiv:2411.09523, which is the same underlying paper), all 13 authors,
venue, and an online-publication date of 2026-05-07. No volume/issue/page number exists yet in the
Crossref record (consistent with an ACM "just accepted" / online-first article) — none is fabricated here.
Use for: risk taxonomy underpinning the seminar's pre-action risk gate and human-in-the-loop design.

## [7] Lewis et al. (2020) — RAG
**Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M.,
Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D.** (2020). "Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks." *NeurIPS 2020*.
Use for: the Memory + RAG block in the proposed architecture.

---

## Revision history
- **2026-09-22 (Phase 1):** Item 6 was initially cited via its 2024 arXiv preprint (arXiv:2411.09523,
  title "...Security, Privacy, and Ethics Threats..."), since the ACM Transactions on Software Engineering
  and Methodology (TOSEM) published version could not be confirmed at the time (dl.acm.org blocked the
  automated fetch, HTTP 403).
- **2026-09-23 (Phase 2 correction):** the published ACM TOSEM version was independently verified via the
  Crossref API — DOI 10.1145/3807666, online-published 2026-05-07, title **"Navigating the Risks: A Survey
  of Security and Privacy Threats in LLM-Based Agents"** (the ACM version drops "and Ethics" from the
  title relative to the arXiv preprint — same paper, revised title at publication). All citations of [6]
  now use this verified 2026 ACM TOSEM record instead of the 2024 arXiv preprint.

## Research Gap
Existing surveys ([1],[2],[3]) establish planning, memory/RAG ([7]), reasoning-acting loops ([4]), and
multi-agent workflows ([5]) as separable capabilities of LLM-based agents, and [6] catalogs the security
and privacy risks that emerge once such agents act autonomously. However, the reviewed literature treats
**capability** (can the agent plan, retrieve, and act?) and **reliability governance** (should this
specific action be allowed, and was it verified afterward?) as largely separate concerns: [1]-[3] focus on
architecture and capability, while [6] focuses on threat cataloguing rather than an in-loop control
mechanism. A practical gap remains in integrating these capabilities into a minimal, teachable reference
architecture that combines pre-action risk assessment, bounded human oversight, and post-action
verification in one demonstrable control loop — which this seminar's proposed architecture is designed to
make explicit and demonstrable in a small prototype (Phase 3), evaluated only qualitatively/structurally,
not with fabricated performance numbers.

**Wording note (Phase 2 correction):** the original phrasing "there is no widely taught, minimal reference
architecture that integrates..." was an absolute, unfalsifiable claim (a negative existence claim over all
of industry/academia cannot actually be verified by a literature search). It has been replaced throughout
both documents with the more defensible formulation above ("a practical gap remains in integrating..."),
which claims only what the reviewed literature supports.
