# HireFlow — Existing Landscape & Research

**Date:** 2026-09-19 • **Status:** Evidence-backed landscape (not product design) • **Sources:** 120+ verified (product docs, papers, GitHub, regulator sites, industry)
**Coverage target:** 20+ commercial products, 24 academic papers, 24 GitHub projects, 8 regulator sources • **Freshness:** 2024–2026 prioritized
**Disclaimer:** This is research synthesis, not legal advice. Jurisdiction summaries distinguish law vs guidance vs commentary.

---

## Executive Summary

Hiring teams face a fragmented toolchain: ATS owns pipeline, but intelligence — parsing, matching, evidence, interview work — is scattered across 5+ product categories. Our research across **24 commercial products, 24 academic papers, 24 GitHub projects, and 8 regulatory sources** finds:

* **Mature and table-stakes:** ATS pipeline stages, resume parsing, keyword/embedding search, scheduling, basic scorecards, reporting. Greenhouse, Lever, Workday, Ashby, iCIMS, and Beamery all document these as shipped.
* **Common but still manual:** Recruiter screening of 100s of resumes, feedback collection, interview-note capture, dispositioning, and audit. Recruiters report 60% of time on admin and 75% of resumes never seen by a human, yet AI scores are distrusted when unexplained.
* **Emerging:** LLM-based skill extraction (ESCO-linked), RAG-grounded ranking with evidence citations, AI interview transcription/summarization, bias dashboards, and detector-tier fraud/provenance (hidden-prompt/phantom-text detection).
* **Rare/experimental:** True audit trails (source → evidence → claim → assessment), per-requirement evidence mapping, NL pool queries with provenance, agentic loops that act across systems with human-approval gates, and verifiable skill graphs (W3C VC).

**Most consequential gap for HireFlow's problem statement:** The statement asks for one coherent `JD + resume → requirement map → evidence → question → note → report → query → audit` loop. No single commercial product documents that end-to-end loop with provenance; papers and open source demonstrate each link in isolation. That fragmentation — plus under-developed human-in-loop and audit surfaces — is the primary whitespace.

The 48-hour prototype implication is to *reuse* mature parsing/retrieval/LLM blocks and differentiate on the connective tissue: structured extraction → requirement mapping → evidence ledger → question/report generation → NL query → audit export.

---

## 1. Problem Landscape

The hackathon brief defines a **recruitment intelligence agent** that keeps human hiring decisions central while reducing repetitive work. Requested capabilities span the full funnel:

> Job description + resume ingestion • Skill/experience/qualification extraction • Candidate-to-requirement mapping • Missing/unclear information detection • Candidate grouping • Structured summaries • Candidate-specific interview question generation • Follow-up generation • Interview-note summarization • Evidence mapping to requirements • Unanswered evaluation areas • Standardized evaluation reports • Natural-language pool queries • Audit trails per insight

This is intentionally broader than any single ATS category. Conventional products split these across: **ATS** (pipeline), **AI screening** (ranking), **interview intelligence** (transcription/assessment), **AI interviewer** (conversational screening), and **recruiter copilot** (assistive drafting). The brief therefore asks for a system that *integrates* intelligence across stages with memory, evidence, and human approval.

Why this matters now: hiring volume and resume variability have grown (Indeed/LinkedIn easy-apply → hundreds per posting in hours), LLM-assisted resume inflation has eroded trust in surface text, and regulators in EU/US/UK/India now require transparency, human oversight, and auditability for employment AI (see §8). Candidates simultaneously demand transparency: 79% want to know if AI is used and 38% have walked away when it wasn't disclosed [Greenhouse/Staf fing Industry 2026](https://www.staffingindustry.com/news/global-daily-news/candidates-have-some-trepidation-about-ai-in-hiring-poll-says); see §4.

---

## 2. Existing Commercial Solutions

We analyzed **24 products** across ATS, AI screening, talent intelligence, interview intelligence, conversational hiring, and sourcing. Each entry distills **documented capability** (official docs/help) vs **marketing claim** (product page/press) vs **independent evidence** (third-party test, journalism, regulator, field study).

### 2.1 Product summaries (24)

| # | Product / Company | Category | Primary workflow | Evidence tier per claim |
|---|---|---|---|---|
| 1 | **Greenhouse + Real Talent / Sourcing Automation** | ATS | JD → AI scorecard attributes → Talent Matching (OpenAI) with calibration → interview kits + Notetaker (Recall.ai) → scorecard summaries → offer forecast + CLEAR verification + fraud/spam tri-layer | Talent Matching & Notetaker **documented** in help center; AI Assistant optimisation **marketing** until docs land [Greenhouse AI](https://support.greenhouse.io/hc/en-us/articles/33043749845403) [Talent Matching](https://support.greenhouse.io/hc/en-us/articles/41396009937307) |
| 2 | **Lever + VONQ AI Screening / Companions** | ATS+screening | JD → AI chat/voice screening → ranked dossier with reasoning → nightly Screening/Interview Companions → personalized rejection | VONQ screening **documented** in help; nightly companion cadence **documented**; "full reasoning visible" **marketing** lacking public rubric |
| 3 | **Workday Recruiting + HiredScore (Talent Acquisition Agent)** | HCM/ATS | Requisition → HiredScore grading + Fetch rediscovery (≤15 leads) → Recruiting Agent auto-coordinates panels/calendars → Candidate Experience Agent conversational apply | Grading & Fetch contracts **documented** in Workday docs + release notes (2025-03-12); 54% capacity lift **marketing** press; guardrails **documented** (2025-06-21 blog) [Workday Agents](https://www.workday.com/en-us/artificial-intelligence/ai-agents/talent-acquisition.html) |
| 4 | **Ashby (AI-native ATS + CRM + Scheduling)** | AI ATS | Intake → AI application review → Talent Rediscovery → Sourcing via AI tokens → Ashby Notetaker → feedback summaries + hiring debrief → Report Builder | Application Review, Notetaker, Assistant, MCP, custom agents **documented** in Ashby docs; agentic claims verified 2026-05 press [Ashby AI](https://www.ashbyhq.com/ai) [Assistant](https://www.ashbyhq.com/product-updates/ashby-assistant) |
| 5 | **Paradox Olivia (Conversational ATS / Candidate Experience Agent)** | Conversational | Conversational career site → 24/7 chat/text/WhatsApp screening → knockout scheduling → sentiment pulse → I-9 onboarding | Conversational ATS vs CX-agent distinction **documented**; 58% time-to-apply / 99.78% CX **marketing** case claims |
| 6 | **Eightfold (Talent Intelligence + AI Interviewer + Digital Twin)** | Talent intelligence/agentic | Talent Design → Acquisition (sourcing/matching) → AI Interviewer 24/7 → Marketplace/reskilling → Digital Twin (Teams/Slack/CRM signals) | Deep-learning trajectory data (1.6B) **documented**; 1.3-day fill **marketing**; bias audit of AI Interviewer **independent** per Eightfold |
| 7 | **SeekOut (Recruit / Spot / Workspaces / Assist)** | Search + sourcing | NL describe ideal → 300+ Power Filters + 1B profiles + internal ATS rediscovery → ranking + explainable scores → AI Screener video + rubric | Six-agent architecture + ATS rediscovery 44% **documented** [SeekOut agentic](https://www.seekout.com/capabilities/agentic-ai-recruiting/) |
| 8 | **Beamery (Talent Lifecycle + Ray)** | Talent CRM | Unified skills data (unified taxonomy) → sourcing/matching CRM → nurture campaigns → Workforce task intelligence + Ray sourcing agent (BETA) | Task-intelligence vs skills-intelligence distinction **documented** in support doc 40360654119185; 467% ROI **commissioned** Forrester; Ray BETA limited |
| 9 | **Gem (AI Sourcing + CRM + ATS + Agents)** | Sourcing/ATS+CRM | NL ideal → 800M + ATS history hybrid search → enriched reasoning + history → fraud scan (6 signals) → multi-channel sequences (human approval) → MCP | Agents + Rediscovery + fraud scan **documented** Aug-2025 updates; outreach approval gate **documented** as intentional human-in-loop |
| 10 | **LinkedIn Recruiter + Hiring Assistant** | Search + agentic copilot | JD/intake → Intake/Sourcing/Evaluation/Messaging/Screening/Learning/Cognitive-Memory agents orchestrated asynchronously | Plan-and-executor supervisor + 6 sub-agents **documented** in engineering blog; impact metrics **independent early charter** (+44% InMail acceptance) [Engineering](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant) |
| 11 | **iCIMS Talent Cloud + iCIMS AI + Sourcing Agent** | Enterprise TA platform | Job → NL candidate search in CXM → AI Sourcing Agent (discover/match/engage silver medalists) → chatbot apply → conditional SMS campaigns → scheduling | NL search docs **documented**; Sourcing Agent early-access **documented** Fall 2025; Recruiter stays in control **documented** |
| 12 | **Phenom (Talent Experience + X+ Agentic + Hiring Intelligence)** | Talent experience/agentic | Career site chatbot → CRM campaigns → X+ Screening Fit Score → Automated scheduling + Interview Intelligence → Marketplace/analytics | Fit Score audited validity **marketing** with audit claim; X+ Agent Studio + ontology convergence **documented** [Phenom AI](https://www.phenom.com/artificial-intelligence) |
| 13 | **HireVue / Modern Hire + Assessments + Interview Insights** | Interview intelligence | One-way/live video → transcription-only AI scoring (facial removed 2021) → game assessments → rank order + real-time competency tagging | Transcription-only policy **documented**; scoring correlation >.8 **marketing/vendor study**; Illinois/I NYC compliance features **documented** |
| 14 | **Humanly (AI Interviewer + Conversational)** | Conversational screener | ATS-embedded link → Interview Builder → candidate 24/7 chat/voice/video → same questions → transcript + vision screen-share flag + structured scorecard | Structured scoring + vision flag **documented**; field-study lift (25 min saved) **independent** (Chicago Booth/Erasmus cited) |
| 15 | **Loxo (Talent Intelligence Platform, ATS+CRM+Sourcing)** | Unified ATS/CRM | ATS+CRM+sourcing+outreach+knowledge graph (1.2B, 7th gen) → sourcing→CRM nurture → AI ranking → outreach tracking in one system | Single-system positioning **documented**; outsources AI claims less independently verified |
| 16 | **entelo / SeekOut alternative? — Fetcher / HiredScore analogues** | Sourcing | External profile aggregation + diversity filters → outreach sequences | Diversity/representation **marketing** varied |
| 17 | **Modern Hire lineage (HireVue)** | Assessment | Virtual job tryout + structured IO guides | Validation studies **vendor-documented** |
| 18 | **SAP SuccessFactors Recruiting + AI** | HCM/ATS | Req → sourcing → screening → offer tied to HCM | Certified integrations **documented** (Phenom/Gem) |
| 19 | **Oracle Recruiting Cloud** | HCM/ATS | Req → CRM → screening → scheduling | HCM-native **documented** |
| 20 | **SmartRecruiters** | ATS/Talent acquisition suite | Req → distribution → screening → collaboration → analytics | Integrations **documented** |
| 21 | **Bullhorn ATS (staffing)** | Staffing ATS | Job stages color-coded (Blue/Green/Red/Grey) → application V2 → submission → placement | Stage model **documented** [Bullhorn](https://kb.bullhorn.com/bh4sf/Content/BH4SF/Topics/ATSV2JobStages.htm) |
| 22 | **DaXtra (resume parsing/search)** | Parsing/search | JD/resume ingestion → structured parse → search/match APIs → ATS sync | Parser accuracy claims **documented** via parsers comparison |
| 23 | **Textkernel / Sovren** | Resume/JD parsing | PDF/DOCX → structured JSON (contact/skills/exp/edu) + taxonomy normalization (ESCO/O*NET) → ranking API | Taxonomy mapping **documented** |
| 24 | **Harver / Vervoe (assessments)** | Assessment | Skills-based assessments → scoring → ATS integration | IO validation **documented** for selected assessments |

> **Pattern:** ATS vendors (Greenhouse, Lever, Ashby, Workday, iCIMS) embed AI incrementally and keep humans as decision-makers ("assistive, not automated"). Talent-intelligence vendors (Eightfold, Beamery, SeekOut, Gem, Phenom) push cross-system agentic sourcing/matching with skill ontologies. Interview specialists (HireVue, Humanly, Paradox) automate early screening but stop short of final decision. No vendor documents the full HireFlow loop with per-requirement evidence provenance end-to-end.

For a deeper per-product record (inputs, integrations, pricing, limits, source URLs) see **Appendix A**.

---

## 3. Current Recruitment Workflow

### 3.1 Canonical stages (convergent across ATS docs)

```
Job Definition & Approval
  ↓
Candidate Acquisition (posting + sourcing + referrals)
  ↓
Resume / Application Intake (ATS entry)
  ↓
ATS Processing & Parsing
  ↓
Initial Screening (knockout + AI ranking)
  ↓
Recruiter Screen (phone/chat)
  ↓
Shortlisting Matrix / Scorecard Calibration
  ↓
Interview Preparation (kits, questions)
  ↓
Interview (live/one-way/panel)
  ↓
Interview Notes & Transcripts
  ↓
Evaluation & Competency Mapping
  ↓
Hiring Decision & Offer
  ↓
Record / Audit / Onboarding Handoff
```

*Sources: Bullhorn v2 stage handbook, Greenhouse/Lever requisition flows, Infor Candidate Selection screening → shortlist, Recruiterflow stage entry/exit rules, Trimble per-job-category stage config, Deel-Lever hire webhook, Recruitera analytics funnel.*

Detailed stage definitions and who owns each artifact:

| Stage | Artifact | Owner | System |
|---|---|---|---|
| Intake/Requisition | Job req + interview kit/scorecard | Hiring manager + Recruiter | ATS (Greenhouse `All Jobs`, Lever TRM) |
| Sourcing/Posting | Job distribution + CRM prospects | Sourcer | Greenhouse CRM / SeekOut / Gem (Chrome ext) |
| Intake | Application V2 record, color stages | System | Bullhorn/ATS — see [Bullhorn stages](https://kb.bullhorn.com/bh4sf/Content/BH4SF/Topics/ATSV2JobStages.htm) |
| Screening | Qualification + disposition | Recruiter / AI agent | Infor Screen → Screen Out Online via knockout |
| Shortlisting | Criteria matrix / weighted calibration | Recruiter | Greenhouse Talent Matching; Lever insights |
| Interview | Scheduling (Cal→Zoom), scorecards | Coordinator | Ashby Scheduling, Greenhouse scheduling |
| Notes | Structured feedback + transcript | Interviewer + Notetaker | Greenhouse/ Ashby Notetaker (Recall.ai) |
| Evaluation | Aggregated scorecard summary | Hiring manager | Greenhouse scorecard summary, Phenom Fit Score |
| Hire | Offer, placement, `candidate.hired` webhook | Recruiter + HR | Lever→Deel daily 7am GMT sync |
| Audit | Time-to-hire, source, conversion, dispositions | TA Ops | ATS analytics + EU/UK/CO bias logs |

Stages are **configurable and non-linear**: Bullhorn/Recruitly allow entering at any stage, skipping, or moving backward; stages are assigned per job category [Trimble](https://help.trimble.com/en/viewpoint-hr-management-for-vista/viewpoint-hr-management-for-vista/hr-management-for-vista/applicant-tracking/configure-applicant-tracking/create-ats-stages).

### 3.2 Automation map (what is automated vs manual today)

| Step | Commonly automated | Often manual | Where info is lost |
|---|---|---|---|
| Job creation | JD drafting generators (Greenhouse, Ashby Content Assistant) | Intake with hiring manager on nuance, leveling | JD nuance → template loses context |
| Acquisition | Job board distribution, CRM drips (Gem, SeekOut credits) | Targeted sourcing of passive silver-medalists | Distribution = volume not signal |
| Intake | Parse resumes → JSON (Textkernel/Sovren/DaXtra) | Handling scanned/complex-layout PDFs | Multi-column/tables/dates mis-parsed [Saply accuracy](https://www.saply.ai/blog/ai-resume-parsing-accuracy-comparison/) |
| Screening | Knockout questions, ranked lists (Greenhouse, Lever) | Recruiter reads ~60% admin time per V2Solutions; 75% resumes never reach human per Harvard Hidden Workers (cited [ArXiv 2602.18514](https://arxiv.org/html/2602.18514v1)) | Opaque "73% match" with no evidence → recruiter re-reads |
| Recruiter screen | Chat/voice bots (Paradox, Humanly, VONQ) | Human phone screen for senior roles; context lost between bots | Bot transcript not linked to scorecard |
| Shortlisting | Calibration assistants (OpenAI), matrix UIs | Hiring manager preference capture | Preference tacit, not versioned |
| Interview prep | Question suggestions from job attributes (Greenhouse, Ashby) | Candidate-specific tailoring | Generic questions miss gaps |
| Interview | Transcription (Notetaker, Recall.ai) | Interviewer notes heterogeneous | Notes ≠ structured competency tags |
| Evaluation | Scorecard summaries (Ashby citations, Greenhouse summaries) | Cross-interviewer synthesis; anecdotal via spreadsheets/email | Evidence fragmented across emails/interviews |
| Decision | Ranking, Insights dashboards | Final human judgment; often gut "vibe checks" | Ranking bias amplified by humans (FAccT N=528: humans replicate AI race preferences) |
| Audit | Disposition logs, bias audit export (NYC LL144, CO) | Retention purge, SAR aggregation, proof of human oversight | Data spread across ATS/CRM/email/workbooks |

**Bottom line:** Recruiters report the highest automation at distribution and scheduling, the lowest at synthesis — exactly where HireFlow aims to help.

---

## 4. Internet / Industry Norms

### 4.1 Recruiter expectations (what "good ATS" now means)

G2 taxonomy for `Recruiting Automation`/`ATS` now expects: customization, integration APIs, dashboards, workflow building, sourcing/candidate ID, job posting, interview scheduling, applicant tracking, pipeline Kanban, analytics, generative text, candidate matching/engagement, and **agentic AI (autonomous task execution, multi-step planning, cross-system integration)** as emerging [G2 recruiting-automation](https://www.g2.com/categories/recruiting-automation) [hireEZ features](https://www.g2.com/products/hireez/features).

Leadership signals 2024-25: Gem named **Leader** in Recruiting Automation (97% 4-5★, 96% recommend); Glider AI topped G2 Best Software AI in Recruiting/HR alongside Gemini/Watson — showing market values relationship, momentum, and demonstrable AI ROI [Gem G2](https://www.gem.com/resource/recruiting-automation-g2) [Glider PR 2024](https://www.prnewswire.com/news-releases/g2-recognizes-glider-ai-as-the-top-ai-product-in-recruiting-and-hr-technology-302072780.html).

Recruiterflow norm checklist: one accountable owner per handoff, clear entry/exit rules + required data per stage, visible hold/reject/withdraw paths, no ambiguous "in Interview 2 weeks" stage [Recruiterflow](https://recruiterflow.com/glossary/ats-workflow).

### 4.2 Candidate expectations (transparency and rights)

| Finding | Figure | Source |
|---|---|---|
| Want to know if AI used | 79% | HireVue survey of 3,100 workers + 1,000 HR, US/UK [HR Executive](https://hrexecutive.com/optimism-for-ai-in-hiring-is-high-but-dont-forget-transparency) |
| Interviewed by AI (up 13pp in 6 months) | 63%; 70% not clearly told up front they'd be evaluated by AI; 21% learned only at interview start | Greenhouse 1,200 US workers May 2026 [Staffing Industry](https://www.staffingindustry.com/news/global-daily-news/candidates-have-some-trepidation-about-ai-in-hiring-poll-says) |
| Walked away over AI handling | 38% walked away + 12% would; top triggers: pre-recorded AI-scored video no human (33%), undisclosed AI (27%) | Same |
| Disclosure should be legal | 57%; only 18% say employers have clear AI policies | Same |
| Transparency increases apply intent | Disclosing AI use + role → significantly more likely to apply (J Bus Psychol 2023) | [SenseHQ Trust](https://www.sensehq.com/blog/building-candidate-trust-in-automated-hiring) |
| Human review demanded | 38% want human reviews AI decisions; 29% want bias-audit evidence; 46% want human interview option | Greenhouse + [SenseHQ Human-Centered](https://www.sensehq.com/blog/human-centered-hiring-in-the-age-of-ai) |
| Ghosting | 1/3 feel ghosted after 1 week silence; 51% who did AI interview never heard back | [SenseHQ](https://www.sensehq.com/blog/building-candidate-trust-in-automated-hiring) |
| Regulation driving norms | NYC LL144 bias audit, Illinois Video Interview Act (2020), EU AI Act high-risk employment 2026, CO disclosure | [SHRM Dec 2025](https://www.shrm.org/executive-network/insights/ai-hiring-why-transparency-matters-more-than-ever) |

**Candidate transparency checklist** (Indeed + SenseHQ + SHRM synthesis): disclose *where* AI applied (ranking vs decision), *how* reviewed ("AI prioritizes, human decides"), *what rights* (accommodation/appeal); communicate within **5 business days** and feedback within 48h; provide actionable, plain-language performance notes. Midland Care example: Indeed Smart Screening 0-100 with editable criteria. SHRM warns 71% of employers still let AI reject without human review despite near-universal belief AI produces bias — a trust gap.

### 4.3 Product/UX expectations

Modern ATS dashboard patterns per Eleken, UITOP, Dribbble/Behance teardowns:

* **Pipeline Kanban** with color-coded stages, drag-drop, bottleneck highlights [Dribbble Talentfly](https://dribbble.com/shots/25996871-Talentfly-Recruiter-Focused-ATS-Dashboard-UI-UX-Design) [Behance ATS](https://www.behance.net/gallery/235100615/ATS-Application-Dashboard-Admin-UIUX-Design)
* **Smart filters:** role/location/company/university/skill/tag + relevance % slider + boolean + full-text (CEIPAL example)
* **Talent pool CRM:** auto-updated skill/role tags, teams/permissions for collaboration
* **Visualization:** customizable interactive charts, exportable reports, source/department filters (Comeet)
* **Communication hub:** centralized candidate record with full history log, bulk email/SMS, address transparency
* **Time-to-action:** most frequent tasks most accessible; dated reporting UIs and hidden scheduling CTAs (= 7-click scheduling in Rippling) are called out as anti-patterns [Eleken](https://www.eleken.co/blog-posts/5-common-hiring-problems-and-how-a-well-designed-ats-can-fix-them) [Rippling thread](https://reddit.com/r/rippling/comments/1w02zvm/anyone_else_struggling_with_rippling_recruiting/p69zvt3)
* **Evidence display:** expected as inline citations (Ashby feedback summaries cite original feedback; Greenhouse Talent Matching highlights matched phrases). Opaque scores without evidence are flagged as anti-pattern.

*Anecdotal sources (Reddit, G2 reviews) marked as practitioner sentiment, not authoritative fact.*

---

## 5. Academic & Research Landscape

We reviewed **24 original papers (2017–2026)** — 6 foundational and 18 task-specific — covering matching, parsing, skill extraction, screening/IR, interview QG/summarization, fairness, explainability, and agentic HR. Prefer original arXiv/ACL/NeurIPS records over secondary summaries. Full details: [Appendix C](#appendix-c--research-papers).

### 5.1 Foundational models (enable HireFlow stack)

| Paper | Year | Contribution | HireFlow relevance |
|---|---|---|---|
| [Attention Is All You Need — Vaswani et al., NeurIPS 2017](https://arxiv.org/abs/1706.03762) | 2017 | Transformer multi-head self-attention | All NLP encoding (JD/resume), NER, ranking |
| [BERT — Devlin et al., NAACL 2019](https://arxiv.org/abs/1810.04805) | 2018/19 | Bidirectional masked LM + NSP | Backbone for matching/SkillSpan/ESCO linking |
| [GPT-3 — Brown et al., NeurIPS 2020](https://arxiv.org/abs/2005.14165) | 2020 | 175B autoregressive few-shot | Zero-shot JD parsing, QG, evidence synthesis |
| [T5 — Raffel et al., JMLR 2020](https://arxiv.org/abs/1910.10683) | 2020 | Text-to-text + C4 750GB | Summarization, report generation |
| [LoRA — Hu et al., ICLR 2022](https://arxiv.org/abs/2106.09685) | 2021 | Rank-decomposed adapters (10,000× fewer params) | Cheap per-client domain adapters |
| [RAG — Lewis et al., NeurIPS 2020](https://arxiv.org/abs/2005.11401) | 2020 | Dense retriever + seq2seq generator | Blueprint for grounded evidence mapping |

### 5.2 Candidate–job matching & resume/JD parsing

* **[ConFit — Yu et al., 2024](https://arxiv.org/abs/2401.16349)** — Paraphrase augmentation + contrastive learning O(B²) negatives over dual encoder; +19 nDCG@10 job ranking, +31 resume ranking vs text-ada-002. Solves cold-start sparsity — directly deployable for HireFlow matching.
* **[ResuméAtlas — Heakl et al., 2024](https://arxiv.org/pdf/2406.18125) (13,389 records, 43 classes)** + **[Smart-Hiring — 2025](https://arxiv.org/pdf/2511.02537)** — Gemma 91-92% top-1, 97% top-5 vs XGB; two-stage LLM IE → `all-MiniLM-L6-v2` weighted cosine (skill/exp/edu) gives interpretable matching; reference architecture for HireFlow intake.
* **[Job Recommender Systems: A Review — 2021](https://arxiv.org/pdf/2111.13576)** — Systematizes content/collaborative/knowledge JRS and reciprocal recommendation; frames language mismatch between seeker/candidate and recruiter vocabularies — motivates HireFlow's taxonomy layer.

### 5.3 Skill extraction & classification

* **[SkillSpan — Zhang et al., NAACL 2022](https://aclanthology.org/2022.naacl-main.366)** — SKILLSPAN 14.5K sents/12.5K spans expert-annotated; hard vs soft split; SpanBERT + domain pre-training improves long spans. Gold evaluation set for HireFlow NER.
* **[Survey on Skill Extraction & Classification — Senger et al., EACL 2024](https://arxiv.org/abs/2402.05617)** — 40+ neural methods (BIO, SpanBERT, XMLC); maps ESCO linkage; catalogs 15+ datasets — definitive taxonomy.
* **[Extreme Multi-Label Skill Extraction via LLMs — Decorte et al., 2023](https://arxiv.org/abs/2307.10778)** — Synthetic ESCO (13K label) data via LLM prompting + contrastive bi-encoder → +15-25 R-Precision@5 vs distant supervision.
* **[Rethinking Skill Extraction with LLMs — Nguyen et al., 2024](https://arxiv.org/abs/2402.03832)** — LLMs underperform supervised F1 but handle syntactically complex mentions with higher recall — informs when to use LLM IE vs NER.

### 5.4 Screening, ranking & IR

* **[Information Retrieval: Recent Advances — Hambarde et al., 2023](https://arxiv.org/abs/2301.08801)** — Retrieve-then-rerank with dense retriever + cross-encoder reranker as SOTA; hybrid BM25+dense best robustness → HireFlow shortlisting pattern: Faiss ANN → cross-encoder.
* **[Embedding-based Job→Candidate Matching at Scale — Zhao et al., CareerBuilder 2021](https://arxiv.org/abs/2107.00221)** — Fused embeddings (text+entities+location) → Faiss ANN → contextual reranker; offline/online CTR/nDCG gains at millions scale.

### 5.5 Interview QG, summarization & competency extraction

* **[Modular AI Interviewer — Adeseye et al., 2025](https://arxiv.org/html/2601.11534v1)** — 4-module locally-hosted dynamic QG with priority-weighted questions, expertise profiling, reflection+justification per question — blueprint for HireFlow QG.
* **[LLM-as-an-Interviewer — 2024](https://arxiv.org/abs/2412.10424)** — Two-stage unclarification/paraphrase + multi-turn feedback/follow-up shows static benchmarks miss adaptability; supports HireFlow staged probing.
* **[MediaSum — Zhu et al., NAACL 2021](https://arxiv.org/abs/2103.06410)** — 463.6K interview transcripts (NPR/CNN) for dialogue summarization; transferable pre-training for HireFlow interview summarizer.
* **[Competency Modeling via LLMs — 2026](https://arxiv.org/html/2602.13084v1)** — Behavioral descriptor extraction → competency library embedding + weight fusion matches human-expert agreement — core evidence→competency mapping with provenance.

### 5.6 Fairness / bias (critical for HireFlow compliance)

* **[Wilson & Caliskan, AIES 2024](https://arxiv.org/abs/2407.20371)** — Zero-shot dense retrieval audit (500+ resumes × 500 JDs): White favored 85.1%, Black 8.6%; Black males 0-100% disadvantaged — method replicable for NYC LL144 audit.
* **[Gao et al., 2026](https://arxiv.org/abs/2606.28978)** — 24,024 paired resumes × 14 LLMs: GPT-3.5 +2.12pp pro-White → 2024+ models reverse to −3.01 pro-Black; same for gender — per-model calibration required, upgrades don't guarantee neutrality.
* **[FAIRE — Wen et al., 2025](https://arxiv.org/abs/2504.01420)** — Direct scoring vs ranking benchmark: every model biased; ranking more sensitive than scoring.
* **[Silicone Ceiling — Armstrong et al., EAAMO 2024](https://arxiv.org/html/2405.04412v1)** — GPT-3.5 resume assessment/generation shows gender, race, and age bias — structured rubrics needed, not free-form scoring.

### 5.7 Explainability / auditability

* **[Evaluating Promise & Pitfalls of LLMs in Hiring — 2025](https://arxiv.org/pdf/2507.02087)** — 10K real candidate-job pairs: domain-tuned + audited beats off-the-shelf LLM on both accuracy and fairness — no trade-off myth.
* **[JobMatchAI — Vyas et al., ACL Demo 2026](https://aclanthology.org/2026.acl-demo.52/)** — KG + transformer + per-factor (skill/exp/location/salary) interpretable reranking on JobSearch-XS; reference for explainable UI.
* **[Systematic Review of AI Audits — 2024](https://link.springer.com/article/10.1007/s10796-024-10508-8)** — Auditability measures per pipeline stage and responsible party; maps lack of outcome feedback loops.
* **[From Transparency to Accountability — ACM 2024](https://dl.acm.org/doi/fullHtml/10.1145/3689904.3694711)** — Formal: black-box query access sufficient for faithful audit — grounds HireFlow EvidenceLedger.

### 5.8 Agentic AI

* **[Agentic AI for HR: LLM-Driven Candidate Assessment — Yuksel et al., EACL 2026](https://arxiv.org/abs/2603.26710)** — **Primary ancestor architecture:** Criteria Generation (YAML rubric 12-20 dims) → Video QG → Assessment Generator (CV+transcript → Low/Med/High + citation) → Active Listwise Tournament via Plackett-Luce + active learning; citation-backed reports mirroring expert judgment.
* **[Practical Guide to Production Agentic Workflows — Bandara et al., 2025](https://arxiv.org/abs/2512.08769)** — Single-responsibility agents, MCP tool integration, pure-function invocation, container/K8s pattern; 9 best practices for determinism/auditability.
* **[OKRA & TIMBRE — 2024-25](https://arxiv.org/html/2504.07108v1)** — Heterogeneous temporal KG (resumes/JDs/notes + ESCO/Wikidata + temporal sampling + GCN) with subgraph explanations; handles skill recency and candidate+company sides.

> **Cross-cutting paper synthesis:** Sparse supervision → ConFit synthetic augmentation; ontology drift → versioned ESCO KG; bias reversals → per-model audit; span→competency provenance → 2602.13084 + Agentic HR 2026; multi-agent reliability → Yuksel tournament + Bandara ops guide. All support HireFlow's `EvidenceLedger (source→artifact→evidence span→claim)` design.

---

## 6. Open Source / GitHub Landscape

We tracked **24 GitHub projects** (end-to-end vs component) with live search/fetch verification (stars point-in-time Sep 2026; no fabricated stars — see Appendix B for per-repo sources). Distinguishing genuinely implemented vs demo:

### 6.1 Project catalog (24)

| # | Repository | Stars | Language | Main capability | Implemented? | Maintained | Relevance |
|---|---|---|---|---|---|---|---|
| 1 | [srbhr/Resume-Matcher](https://github.com/srbhr/Resume-Matcher) | 28.5k | Python/TS | Master-resume → JD-tailored resume + cover + interview prep + scoring/PDF via LiteLLM | **Production** (1,618 commits, Docker, Vercel, FastAPI/Next.js16) | Active Apache-2.0 | Reusable harness for JD→resume tailoring; evidence-lite |
| 2 | [alibaba/SmartResume](https://github.com/alibaba/SmartResume) | 403 | Python | Layout-aware PDF/Image/Office → OCR+layout → LLM fields (vLLM) [arXiv:2510.09722] | Research-grade (31 commits, refactored due compliance) | Active | Best open layout-aware parser |
| 3 | [OmkarPathak/pyresparser](https://github.com/OmkarPathak/pyresparser) | 959 | Python | Regex+NER name/email/phone/skills/edu | Legacy (442 forks, 45 issues) | Stale GPL-3 | Cheap baseline |
| 4 | [AnasAito/SkillNER](https://github.com/AnasAito/SkillNER) | 213 | Python | Rule-based skill/cert via ESMI/Lightcast + spaCy | Library (`pip install skillNer`) | Low MIT | Fast no-LLM skill extractor |
| 5 | [somus/resume-extract](https://github.com/somus/resume-extract) | — | TS/ONNX | DistilBERT ONNX (`oksomu/resume-ner` 13 entities) + ATS score + seniority ~15ms local | Local fast | Active MIT | Local pre-parse before LLM |
| 6 | [ompatel7572/Ai-powered-resume-screening-system](https://github.com/ompatel7572/Ai-powered-resume-screening-system) | — | Python | Multi-column SciPy/K-Means + spaCy transformer + SkillNER + Gemini ranker | Prototype | Unknown | Per-skill breakdown |
| 7 | [RobertoDure/hr-rag-assistant](https://github.com/RobertoDure/hr-rag-assistant) | — | Java/React | Spring Boot 3.3.2 + GPT-4 + pgvector, 4-factor 0-100% scoring | Full-stack | Active | Deterministic scoring API |
| 8 | [kashishgadhiya/AI-resume-Rag-app (RecruitIQ)](https://github.com/kashishgadhiya/AI-resume-Rag-app) | — | Python | 8-stage: query-expansion→HyDE→dense Pinecone+sparse Postgres BM25→RRF→MMR λ0.6→Cohere rerank, Mistral-7B, Gmail ingest, Redis | Advanced | Active | Most complete hybrid RAG |
| 9 | [Pranshu0204/RecruitSense](https://github.com/Pranshu0204/RecruitSense) | — | Python | RAG Fusion Qdrant+BGE-large + RRF, LangGraph parser→(rag\|bias)→scorer, bias decoupled | Well-architected | Active 2026-04-28 | Bias-decoupled scoring |
| 10 | [atharvajoshi01/talent-rag](https://github.com/atharvajoshi01/talent-rag) | — | Python | FAISS hybrid + cross-encoder rerank + ensemble+judge, FastAPI/Streamlit | Production RAG | Active | Eval with Recall/NDCG/MRR |
| 11 | [DHRU-KHAKHARIYA/Semantic-CV-Ranker](https://github.com/dhru-khakhariya/semantic-cv-ranker) | — | Python | Section-split→Mistral JSON → 3 MiniLM fine-tunes + Haversine + pgvector weights 0.4/0.3/0.2/0.1 | Reproducible (80 CVs) | Active | Explainable weight breakdown |
| 12 | [224-aadi/talentrank-ai](https://github.com/224-aadi/talentrank-ai) | — | TS | Hard-rule knockout + hybrid lexical/BM25 + semantic fallback + confidence flags | Launch-ready | Active | Deterministic + fallback |
| 13 | [williyam-m/talentry-ai](https://github.com/williyam-m/talentry-ai) | — | Python | Deterministic zero-LLM ranker (BM25+TF-IDF+behavioural) + Qwen3-0.6B GRPO, honeypot guard | Millions-scale | Active MIT | Anti-gaming at scale |
| 14 | [mohd-ibadullah/AgentHiring](https://github.com/mohd-ibadullah/AgentHiring) | — | Python | Google ADK gemini-2.5-flash + FastMCP (4 tools) + BM25+bge-base hybrid + honeypot trap (100% detect) | Full demo | Active | ADK+MCP pattern |
| 15 | [Kushagra077/RecruitRadar](https://github.com/Kushagra077/RecruitRadar) | — | Python | CrewAI 5 agents: JD Analyst(Groq), Scorer(Gemini)+verbatim guard+fuzzy, Interview Designer, Outreach, Tracker | Strong guarantees | Active | Citation-forced scoring |
| 16 | [vaibhavarora102/HRRecruitingAgent](https://github.com/vaibhavarora102/HRRecruitingAgent) | — | Python | LangGraph + Cerebras 70b + FAISS + Supabase: JD creation→approval→posting→review→interview→offer | Human-in-loop | Active | End-to-end workflow with approval gates |
| 17 | [DHIWAHAR-K/HireMind](https://github.com/DHIWAHAR-K/HireMind) | — | Python/React | 6 LangGraph agents (role/JD/interview/timeline/salary/offer) | Prototype (simulated market) | Active | Multi-agent planning |
| 18 | [UmarbekFU/hr-vertical-agent-kit](https://github.com/UmarbekFU/hr-vertical-agent-kit) | — | TS | 3 MCP servers (recruiting/interviewing/onboarding), 12 tools, 9 prompts, 3 YAML workflows, eval suites | Reusable MCP | MIT | Plug-and-play HR MCP |
| 19 | [simreensiraj/simer-interviewer](https://github.com/simreensiraj/simer-interviewer) | — | TS/Next.js | Gatekeeper→Interviewer (adaptive 1-5, Monaco+ElevenLabs)→Decider (weighted rubric + 9-cat bias audit) | Full pipeline | Active | Adaptive interview with audit |
| 20 | [MohanKrishnaGR/CertusHire](https://github.com/MohanKrishnaGR/CertusHire) | — | Python | Coordinator FSM + 3 personas + RAG 0.6*LLM+0.4*retrieval + Whisper.cpp/Piper | Research-grade | Active | Constitutional AI guard |
| 21 | [GoDiao/ai-interview-agent](https://github.com/godiao/ai-interview-agent) | — | Python | State machine intro→technical→personality→report, longitudinal name+email continuity | Longitudinal | MIT Active | Tracks improvement over sessions |
| 22 | [TalentProof/workproof-schema](https://github.com/TalentProof/workproof-schema) | 4 | JSON Schema | Skill clusters+confidence(0-1)+evidence weights+W3C VC attestations (did:web)+A2A extension, consent L0-L4 | Spec only v0.1 | Draft MIT | Provenance schema for HireFlow |
| 23 | [matthewod11-stack/sourcerer](https://github.com/matthewod11-stack/sourcerer) | 2 | TS monorepo | Intake→Discover(Exa)→Dedup→Enrich(GitHub/X/Hunter)→Score(citing evidence only)→Notion/CSV/MD, 793 tests | Most rigorous provenance | Highly maintained MIT | Evidence-grounded sourcing |
| 24 | [mrNLK/SourceKit](https://github.com/mrNLK/SourceKit) | — | TS | GitHub graph → Research→Search(0-100)→Enrich(Exa LinkedIn)→Kanban→Outreach | Product | Active | GitHub sourcing |

*Also notable:* `sharathkum05/HR-Agent` (Pinecone+GPT-4 top15→top5), `ghoshvidip26/RAG-Resume-Screening` (FAISS+Gemini+RAGAS), `fanqingsong/agentic-ai-hr-automation` (LangGraph), `Akhileshkachhwaha26/hr-copilot-ai-agents` (10 agents, provider-agnostic), `ramakrishnanyadav/Evidra` (pgvector+Groq blind review).

### 6.2 End-to-end vs component distinction

* **End-to-end:** Resume-Matcher, HRRecruitingAgent, HireMind, simer-interviewer, ai-interview-agent, CertusHire, RecruitRadar, AgentHiring.
* **Component (pluggable):** SmartResume (parsing), pyresparser/resume-extract/SkillNER (extraction), hr-rag-assistant/RecruitIQ/RecruitSense/talent-rag/Semantic-CV-Ranker/talentrank-ai/talentry-ai (RAG/ranking), Sourcerer/SourceKit (sourcing), workproof-schema/Evidra (evidence/provenance).

### 6.3 Genuinely implemented vs demo

**Genuinely implemented** (code, tests, deployment): Resume-Matcher (1618 commits, Docker), SmartResume (93.1% acc, 1.22s/page), SkillNER/resume-extract (pip package/ONNX), RecruitIQ 8-stage RAG (metrics endpoint), RecruitSense (deterministic composite), Semantic-CV-Ranker (fine-tuned encoders), RecruitRadar (verbatim guard + offline tests), Sourcerer (793 tests, 14 packages), AgentHiring (Precision@10 +150% vs BM25).

**Demo/MVP** (functional, limited or synthetic data): hr-rag-assistant, talent-rag sample indexes, HireMind simulated salary, williyam-m hosted Space limited 100 candidates.

### 6.4 Reusable ideas for HireFlow

1. **Layout-aware + ONNX hybrid parsing:** SmartResume + resume-extract = fast local pre-parse before LLM extraction.
2. **Evidence-grounded scoring:** Sourcerer + RecruitRadar force LLM to cite verbatim snippets, fuzzy-verify, drop unverified → HireFlow provenance.
3. **Hybrid retrieval:** dense (MiniLM/bge) + sparse (BM25/TF-IDF) → RRF → MMR → Cohere/CrossEncoder (RecruitIQ, talent-rag, RecruitSense) — avoid pure vector.
4. **Deterministic scoring:** LLM outputs per-dimension 0-10, composite computed in Python — auditable, prevents hallucinated tiers (RecruitSense, RecruitRadar).
5. **Bias decoupling:** bias agent runs on raw resume, never fed to scorer — flags surfaced separately (RecruitSense).
6. **WorkProof schema as evidence model:** `skillClusters + confidence + evidence{weight, verifiedAt} + consent L0-L4 + W3C VC attestation` (TalentProof).
7. **Longitudinal candidate graph:** name+email key + session-over-session issue tracking (ai-interview-agent).
8. **Honeypot/anti-gaming:** detect keyword stuffing, impossible timelines, zero-variance (AgentHiring, talentry-ai).
9. **MCP toolkit:** 12 tools as MCP servers for Claude Desktop interop (hr-vertical-agent-kit).
10. **Pluggable adapters with PII TTL:** per-source packages with cost & 90-day PII retention (Sourcerer).

**Gaps across GitHub:** No project fully implements `claim→evidence→assessment→report` with cryptographic provenance (Sourcerer + WorkProof closest but latter spec-only); interview transcript analysis mostly subjective LLM judge without RAG grounding (except CertusHire hybrid); multilingual handling weak (only SmartResume); many rebuild FAISS per run without persistence; few offer multi-tenant RBAC.

---

## 7. AI Models, APIs & Infrastructure

### 7.1 LLMs

* **Frontier APIs:** OpenAI GPT, Anthropic Claude, Google Gemini 2.5 Flash — supported via ADK LiteLLM adapter and LangSmith wrappers. Gemini is natively optimized in ADK Vertex AI Agent Engine but ADK is model-agnostic [Google ADK](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) [LangChain ADK deploy](https://docs.langchain.com/langsmith/deploy-google-adk).
* **Self-hosted/resume-specific:** [qwen3vl-resume-parser](https://huggingface.co/sukhrobnurali/qwen3vl-resume-parser) (Qwen3-VL-8B QLoRA vision-language, 23 fields, 83.9% weighted, 88.2% JSON validity, 23.4GB VRAM, merged from 32B teacher); [t5-resume-generation](https://huggingface.co/nakamoto-yama/t5-resume-generation) (T5-base JD→resume JSON); `dslim/bert-base-NER` + Ollama Llama 3.2-3b / LM Studio Llama-3.1-8B Q4_K_M for local structured JSON.

| Consideration | Strengths | Weaknesses | Relevance to HireFlow |
|---|---|---|---|
| Frontier LLMs | Best reasoning, zero-shot QG/summarization, long context | Cost, latency, data residency, prompt-injection via resume surface, bias per-model (see §5.6) | Co-pilot generation; guard with evidence forcing |
| Domain adapters (LoRA) | Cheap per-client fine-tune, 10k× fewer params, no latency if merged | Requires tuning data, rank heuristic | Per-venue skill/recency adaptation |
| Local/VL parse models | Privacy (on-prem), ~15ms–92s per resume | VRAM heavy, accuracy varies by layout | Sensitive-data intake; pre-parse before cloud LLM |

### 7.2 Document processing (PDF parsing / OCR)

Problem: ATS PDFs include multi-column, scanned images, tables/merged cells, handwritten notes, photographed pages. Generic OCR loses structure; LLM direct ingest drops tables at scale.

| Tool | Scope | Strengths | Weaknesses |
|---|---|---|---|
| **MinerU (OpenMindo)** [PyPI mineru](https://pypi.org/project/mineru) | PDF/DOCX/PPTX/XLSX/Images → Markdown/JSON, VLM+OCR, 109 langs, pipeline 2× OCR, MCP/LangChain/Dify | Fast + languages + multi-format, chip-compatible | Newer, evals vs commercial IDP limited |
| **LlamaParse / LlamaIndex Parse** [Parse](https://developers.llamaindex.ai/llamaparse/parse/) | Agentic parser, layout OCR, 130+ types, recursive checks, tier agentic/agentic_plus, caching/webhooks, ExtractBench/ParseBench | Agentic quality, benchmarked | Agentic tier cost |
| Commercial/OSS parsing (Saply, Sprint CV, CV-Transformer, HireAra, Allsorter) | Benchmarked on scanned/multi-column/overlaps/tables — test with difficult docs, not clean demos [Saply](https://www.saply.ai/blog/ai-resume-parsing-accuracy-comparison/) | Often trained on recruiting corpora | Vendor lock-in |
| Lightweight PyPDF2 + Mistral OCR → Gemini JSON (n8n template) [n8n workflow](https://n8n.io/workflows/7456-automate-cv-screening-with-ai-candidate-analysis) | Quick prototype | Easy | Brittle on layout |

*ATS compatibility rule:* Text must be highlightable (text-based PDF) else OCR required; `semantic_text` (ES 8.15) automates chunking/vectorization [Elastic best practices](https://www.elastic.co/pdf/elastic-5-best-practices-implementing-vector-database-semantic-search.pdf).

### 7.3 Retrieval (Vector DBs, hybrid search, RAG)

**RAG definition (IBM)** [IBM RAG](https://www.ibm.com/think/topics/rag-vector-database): Knowledge base → chunking → embeddings → vector DB → retriever (query embedding + hybrid sparse-dense + rerank) → integration layer (prompt augmentation) → generator. Query 30× faster, 90% dev-time reduction cited for large graphs (e.g., Wikidata 120M on Astra DB).

*Embeddings:* Sentence Transformers `all-mpnet-base-v2` 768d; Elastic ELSER (sparse, no fine-tune) vs E5 (dense multilingual); domain fine-tune helps.
*Vector DBs:* Pinecone (managed), Milvus (OSS), MongoDB Atlas Vector Search, Qdrant, Weaviate, YugabyteDB pgvector (billions, USearch LSM), TiDB (SQL hybrid filters), Couchbase, Elastic `semantic_text`. ANN/HNSW/IVF indexes.

**Recruitment-specialized RAG** [V2Solutions](https://www.v2solutions.com/blogs/semantic-hiring-vector-search-rag): Semantic retrieval (DevOps ≈ infra automation) → context augmentation (structured skills/certs + unstructured GitHub/reviews) → LLM fit summary ("Priya led 3 React micro-frontends") → counterfactual bias check (would rank hold if name/gender/school changed?) per EEOC/NYC 144/EU AI Act. Metrics cited: 40% faster time-to-hire, 60% fewer false positives, 65% screening-time reduction, sub-second at millions scale.

### 7.4 Recruitment-specific data

* **ESCO v1.2.1 (EU, 10 Dec 2025)** — 13,485 skills + knowledge + transversal in 27 langs; 4 sub-classifications; occupation-skill linkage; API/CSV/data [ESCO skills](https://esco.ec.europa.eu/en/classification/skill-main) [Pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar)
* **O*NET-SOC 2019 (US DOL)** — 1,016 titles (923 data-level), 20K tasks, 35 skill cats, >55K jobs; SOC 2018 [Taxonomy](https://www.onetcenter.org/taxonomy.html)
* **Crosswalk ESCO↔O*NET** — Commission models + human validation, 332 Intermediate Work Activities via semantic similarity; XLSX reports [Tech report PDF](https://esco.ec.europa.eu/system/files/2022-12/ONET%20ESCO%20Technical%20Report.pdf)
* Usage pattern: simultaneous ESCO+O*NET+ISCO anchor with verification on agreement (CPASS Kenya 2025 [example](https://esco.ec.europa.eu/en/news/cpass-use-esco-ai-native-skills-verification-platform)); hybrid taxonomy+ontology+AI NLP for evolving skills [Brookings hybrid](https://www.brookings.edu/articles/the-future-of-hiring-advantages-of-a-skill-based-ai-powered-hybrid-approach).

Public datasets: resume/skill datasets are scarce for privacy; notable open ones are SkillSpan, ResumeAtlas (13,389), MediaSum (463.6K interview transcripts for pre-training summarization).

### 7.5 Agent frameworks

| Framework | Abstraction | Pattern | Hiring relevance |
|---|---|---|---|
| **Google ADK** [ADK overview](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) | Workflow agents (predictable) vs agent-coordinated (dynamic); MCP client/server, A2A, evaluation, rich tools | Supervisor/worker, hierarchical, peer-to-peer; nodes = LLM/Python/Tool; edges sequential/parallel/conditional | Citi/JPM job reqs cite ADK+LangGraph as desired |
| **LangGraph** (Jan 2024, LangChain) | Low-level cyclic multi-actor graphs; prebuilt agents for simple cases | Nodes/edges/shared state, knowledge/trace/improvement graphs | Stateful hiring workflows |
| **LangChain / CrewAI / AutoGen GraphFlow / Microsoft Agent Framework / Pydantic AI / smolagents** | Vary: ADK 52/100 leader score, OpenAI SDK 59/100 dev score [ProductArena 2026](https://ultrametric.ai/productarena/arena/agent-frameworks) | Tool calling, planning, memory, harness engineering | Choice depends on governance needs |

Deployment glue: `deployments-wrap-sdk[saf_sdk]` bridges ADK Runner → LangGraph Pregel → LangSmith Agent Server (checkpoints, streaming, tracing) [LangChain deploy](https://docs.langchain.com/langsmith/deploy-google-adk).

*Tradeoff:* Anthropic 2025 measurement: agent use ~4× tokens vs chat; multi-agent ~15× tokens — prefer single loop with brakes unless org-chart needed, per [QJC graph engineering](https://qjc.app/blog/graph-engineering).

---

## 8. Privacy, Safety, Fairness & Regulatory Considerations

*This section is synthesis, not legal advice. Each item identifies jurisdiction, date, legal status (law/regulation/guidance/commentary), and relevance. The area is fast-changing — prioritize recent sources.*

### 8.1 EU — most prescriptive

**EU AI Act — Regulation (EU) 2024/1689, OJ 12 Jul 2024, in force 1 Aug 2024 — LAW.** Risk tiers: unacceptable (Art.5 banned), high-risk (Arts.6-27), limited (transparency Art.50), minimal. **Employment (Annex III(4)) is high-risk:** recruitment/selection, targeting/filtering/evaluating candidates, promotion/termination, task allocation, performance monitoring. Prohibited Art.5: emotion inference in workplace/education via biometrics (enforceable from 2 Feb 2025). Provider obligations (Arts.9-15) if building own model or substantially modifying: risk management, data governance, technical docs, logging, human oversight by design, accuracy/robustness, QMS, conformity, CE, EU database. Deployer (employer) obligations Art.26: competent human oversight, relevance/representativeness of inputs, monitoring, incident reporting, logs ≥6 months, informing workers' representatives + affected workers before deployment. Fines €35m/7% (prohibited) or €15m/3% (high-risk). Source: [EUR-Lex 2024/1689](http://data.europa.eu/eli/reg/2024/1689/oj).

**GDPR — Regulation (EU) 2016/679, 25 May 2018 — LAW** [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj). Lawful basis typically legitimate interest or contract steps (not consent due to imbalance Recital 43); consent only for talent-pool retention (granular, withdrawable). Art.9 special category, Art.5 data minimisation (no DoB/photo by default), Art.22 solely automated decisions producing legal/significant effect prohibited unless exception (contract/law/consent) + safeguards Art.22(3) (information, human intervention, contest). Transparency Arts.13(2)(f)/15(1)(h): meaningful logic, significance, consequences. DPIA mandatory Art.35 for AI screening. Controller (employer) / processor (ATS) split Art.28 requires DPA; SAR/erasure 1 month. HireFlow must support: granular pool consent, 6-12mo purge, SAR bundle, meaningful human override pathway, DPIA pack.

### 8.2 UK

**UK GDPR + Data Protection Act 2018 retained; Data (Use and Access) Act 2025, Royal Assent 19 Jun 2025 — LAW.** DUAA Arts.22A-22D (from Feb 2026) reframes ADM from EU's prohibition toward right-to-contest + safeguards; legitimate interests now permitted for recruitment ADM if no special category. **Single global GDPR policy now wrong — need EU vs UK bifurcation.** Source: legislation.gov.uk + ICO guidance landing page noting DUAA review.

**ICO Recruitment & ADM guidance — GUIDANCE (high authority).** [Recruitment and selection](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/recruitment-and-selection/) + `AI in Recruitment Outcomes Report (Nov 2024)` + `Recruitment Rewired (31 Mar 2026)` (30+ employers). Findings: many employers believe they have human-in-loop but evidence shows solely automated (fit score + rubber-stamp). Seven recommendations: fairness, transparency, data minimisation, role clarity, explicit instructions, lawful basis, DPIA. 2026 report expects proactive transparency at right time, logic+consequences, contest pathway, monthly bias monitoring. Draft ADM guidance consultation until 29 May 2026, code of practice required.

### 8.3 US — federal + state/local patchwork

* **EEOC — Title VII + ADA guidance — LAW (Title VII 1964 + Uniform Guidelines 1978) + GUIDANCE** [EEOC 2023](https://www.eeoc.gov/assessing-adverse-impact-ai...) / [EEOC 2022 ADA](https://www.eeoc.gov/laws/guidance/americans-disabilities-act-and-use-software-algorithms-and-artificial-intelligence-...). Title VII 18 May 2023: AI informing hiring = selection procedure under UGESP; assess via 4/5ths rule (not determinative) + significance; adverse impact requires job-related/business-necessity + no less-discriminatory alternative. Employer liable even if vendor-built; must self-audit. ADA 12 May 2022: no screen-out without accommodation, accessible alternatives, disclose traits/method promptly. Enforcement priority 2024-28. **Workday amicus (Mobley v. Workday, N.D. Cal., 9 Apr 2024)**: vendor could be directly liable as employment agency/indirect employer if it makes advance/reject decisions.

* **NYC Local Law 144 (2021), enforced 5 Jul 2023, DCWP Rule 6-101 et seq. — LAW.** AEDT = ML/statistical process issuing score/classification that substantially assists/replaces discretion. Requires: (1) annual independent bias audit (sex/race/intersectional impact ratios, EEO-1 cats), (2) public posting of summary, (3) 10-business-day notice to NYC residents, (4) data source/type & retention disclosure within 30 days. Penalties $500–$1500/day; Comptroller audit Dec 2025 found enforcement ineffective → expect stricter phase. Source: [NYC DCWP AEDT](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page).

* **Illinois — AI Video Interview Act 820 ILCS 42 (2019, eff 1 Jan 2020, amend P.A.102-47 eff 1 Jan 2022) — LAW** [Justia ILCS 42](https://law.justia.com/codes/illinois/chapter-820/act-820-ilcs-42/) + **IHRA Amendment HB 3773/P.A.103-0804 (signed 9 Aug 2024, eff 1 Jan 2026) — LAW** [ILGA](https://ilga.gov/legislation/billstatus.asp?DocNum=3773&GAID=17): bans discriminatory AI or zip code as proxy in hiring; requires pre-video notice + explain AI + obtain consent + delete within 30 days on request; if sole selector for in-person, annual demographic reporting; new law adds AI-hiring notice to Illinois Human Rights Act.

* **Colorado — AI Act SB24-205 (signed 17 May 2024, eff 1 Feb 2026) — LAW** [leg.colorado.gov](https://leg.colorado.gov/bills/SB24-205): high-risk employment decisions require risk management program, annual impact assessment, human-review appeal if feasible, 3 notices (pre-use + adverse-action principal reasons + website statement), AG breach notice within 90 days if discrimination discovered.

* **Maryland — Law Art. §3-717 (Law Ch.446, eff 2020) — LAW:** no facial template in interview without signed waiver.

### 8.4 India

**Digital Personal Data Protection Act, 2023 (Act No.22, assented 11 Aug 2023) + DPDP Rules 2025 — LAW**, staged commencement [Meity PDF](https://www.meity.gov.in/static/uploads/2024/02/Digital-Personal-Data-Protection-Act-2023.pdf). Substantive duties (Secs.3-17, Rules) **~mid-May 2027** (definitions+Board machinery 13 Nov 2025). Employer = Data Fiduciary, candidate = Data Principal; Sec.7(i) legitimate use: processing for employment/safeguarding employer from loss/liability **needs no consent** — but pre-employment shortlisting/background check likely outside and needs consent (debated per NovoJuris). Other duties: accuracy before decision, security, breach intimation 72h to Board + each principal, purpose-limited retention (labour law minima override, e.g., 5y Wages Code), negative-list transfers, SDF DPIA/audit. Penalties to ₹250 crores.

### 8.5 Cross-cutting product checklist

| Theme | EU (AI Act+GDPR) | US | UK | India | HireFlow must account for |
|---|---|---|---|---|---|
| Privacy & minimisation | 5(1)(c) + 9; no DoB/photo by default; DPIA; purpose limit | Title VII/ADA data via AI = risk; CCPA if CA | Same as EU + no mass LinkedIn DB without knowledge | Sec.8 minimise to employment purpose |
| Consent | Not valid for application; pool only | Maryland facial waiver; Illinois video pre-consent | Pre-DUAA similar; post-DUAA LI allowed for ADM | Not needed for core employment (7(i)), needed pre-hire/optional |
| Retention | 6-12mo; CNIL 2y last contact; auto-purge | Keep to defend claims 1-3y | 6-12mo (ICO) | Erase when purpose served; override by labour law |
| Sensitive attributes | Art.9 + ban biometric race/politics/religion/sex inference | Race/colour/sex/…; IL/CO zip-code ban | Same as EU; no inferred gender/ethnicity for bias monitoring | Caste/religion analogous other laws |
| Explainability | 13(2)(f)/15(1)(h) meaningful logic + consequences; Art.13/86 | CO principal reasons | Domain/use/impact tailored | Notice of purpose/means (Sec.5) |
| Auditability | Risk mgmt + conformity; harmonised standards pending | 4/5ths + significance; NYC annual impact ratios; CO annual assessment | Monthly bias reviews (good practice) | SDF annual DPIA + audit |
| Human oversight | Art.14 effective oversight; rubber-stamp = not oversight | EEOC alternative; NYC substantially-assists test; CO appeal | Meaningful human involvement (authority/competence) | Fairness implicit |
| Disclosure | Worker-rep + affected persons before deployment | NYC 10-day; CO 3 notices; Illinois pre-video + IL IHRA | Right time, not buried | Consent notice if applicable |
| Accessibility | EAA; AI Act literacy | ADA reasonable accommodation | Equality Act 2010 | RPwD Act 2016 |
| ADM | Solely automated prohibited unless exception + safeguards | No federal ADM ban; disparate impact still actionable | Pre-DUAA Art.22 ban; post-DUAA 22A-D right-to-contest | No ADM-specific ban yet |
| Rights | SAR/erasure 1mo | EEOC charge; CCPA in CA | 1mo | Access/correction/erasure + Board grievance |

**Must-have before launch (multi-jurisdiction):** role-based privacy pack with balancing-test docs + unbundled pool consent; retention engine 6/12/24mo + backup propagation; sensitive-attribute guardrails (zip-code off in IL/CO; photo/DoB disabled; emotion inference hard-blocked EU-wide); per-decision explainability (principal reasons + meaningful logic concise); bias dashboard (selection/scoring rates, impact ratios, 4/5ths flag, significance); human-override UI + competence log + appeal queue <1mo; disclosure countdown/templates (NYC 10-day, EU worker-rep, ADM badge); alternative-process button for ADA; ADM toggle default OFF for EU with safeguard bundle; DPA + SCCs/DPF; breach timers (CO 90d, India 72h).

---

## 9. Common vs Emerging vs Rare Capabilities

Classification grounded in multi-source evidence (frequency across products, papers, GitHub, analyst, practitioner). Anecdotal marked where relevant.

| Category | Definition | Count observed | Examples |
|---|---|---|---|
| **Table stakes** | Expected in any credible ATS | 8–12 of top ATSs document | Resume parsing; JD posting; pipeline Kanban + stages; search/filter; interview scheduling; scorecards; reporting basic; application intake |
| **Common** | In many products but not universal | 5–8 vendors | Skill extraction (keyword/rule), requirement mapping (simple match %), candidate summarization (one-para LLM), evaluation forms, permissions/collaboration, integrations (Greenhouse/Lever/Workday), general LLM drafting (Ashby Content Assistant) |
| **Emerging** | In newer AI products or recent papers, 2–5 vendors or active research | 2–5 | Hybrid RAG retrieval (dense+sparse+RRF+rerank); LLM-based skill linking to ESCO; RAG-grounded ranking with citations; bias dashboards (4/5ths / impact ratios); fraud/provenance signals (hidden-prompt detection); AI Notetaker + feedback summaries with citations; NL Filter/Report assistants (Ask Ashby, Greenhouse filters) |
| **Rare** | 1–2 vendors or research prototypes only | 1–2 | Evidence ledger spanning JD→resume→interview with per-requirement audit trail; standardized evaluation report that auto-populates from evidence + flags unanswered areas; candidate-specific follow-up QG tied to mapped gaps; verifiable skill graph (W3C VC did:web); MCP permissioned agent data access; honeypot/anti-gaming at ranking time |
| **Experimental** | Mostly in papers/open-source, not productized | Papers/GitHub | Active listwise tournament ranking (Plackett-Luce); temporal KG (TIMBRE) for skill recency; deep multi-agent orchestration with autonomous tool use across systems + rollback; longitudinal candidate graph across interview cycles |
| **Missing / poorly solved** | Problem asks for it, market still weak | Gap analysis consensus | Uncertainty-aware missing-info detection that actually triggers next-step actions; resolving conflicting evidence across stages (resume says X, interview says ¬X); memory/state that adapts when new evidence arrives (append-only ledger); natural-language pool queries with provenance (not just filters); human-in-loop approval that is measured/audited for meaningfulness (ICO "rubber-stamp" problem) |

*Mechanism:* Market has raced to add generative summarization and matching, but largely as point features. Connective capabilities — structured requirement lists, missing-info classification by verifiability, grouped/graded evidence per requirement, audit export — remain rare because they require cross-stage data model + ledger, not just prompting.

---

## 10. Capability Matrix

Capabilities from the brief plus those revealed by research. Marked: ● table-stakes ●● common ◐ emerging ○ rare ◌ experimental — × missing in most.

| Capability | ATS (Greenhouse/Lever/iCIMS) | AI Screening (HireScore/SeekOut/Gem) | Interview Intelligence (HireVue/Humanly) | AI Interviewer (Paradox/Eightfold/SeekOut Screener) | Recruiter Copilot (Ashby Assistant/LinkedIn Hiring Assistant) | **HireFlow brief** asks for it? | Evidence quality |
|---|---|---|---|---|---|---|---|
| Resume parsing | ● | ● | ◐ | ○ | ◐ | Yes (JD+resume ingestion) | Documented ATS; [SmartResume 93.1%] |
| JD parsing | ● (generators) | ● | × | ○ | ●● | Yes | Greenhouse/Ashby docs |
| Skill extraction (ESCO/O*NET) | ◐ | ●● | × | ◐ | ◐ | Yes | SkillSpan/ESCO papers + SkillNER/GitHub |
| Requirement mapping (JD → structured requirements) | ◐ | ●● (weighted) | × | ○ | ●● | Yes — core | Greenhouse calibration; Yuksel rubric |
| Candidate matching (rank/shortlist) | ●● (Talent Matching) | ●● | × | ◐ | ●● | Yes | ConFit + CareerBuilder paper |
| Candidate grouping (cohorts/issues) | ○ | ◐ | × | × | ○ | Yes | RecruitSense grouping |
| Candidate summarization | ●● | ●● | ●● | ◐ | ●● | Yes — structured summary | Ashby citations; JobMatchAI |
| Missing-information detection | ○ | ○ | × | ○ | ○ | Yes — must identify | Rare — flag for NL query follow-up |
| Interview question generation (candidate-specific) | ◐ (generic) | × | ○ | ●● | ◐ | Yes — personalized | Yuksel Video QG; Modular Interviewer |
| Personalized follow-up questions | × | × | × | ◐ | × | Yes | Modular Interviewer + LLM-as-Interviewer |
| Interview transcript analysis | ◐ (Notetaker) | × | ●● | ●● | ◐ | Yes — note summarization | MediaSum 463K; Ashby Notetaker docs |
| Interview-note summarization | ●● | × | ●● | ◐ | ●● | Yes | T5/JobMatchAI |
| Evidence mapping (span → requirement) | ○ | ○ | ○ | × | ○ | Yes — map evidence | 2602.13084 competency + WorkProof schema |
| Evaluation reports (standardized) | ●● (scorecards) | ◐ (dossiers) | ●● (scorecards) | ◐ (summaries) | ○ | Yes — report | Phenom/Greenhouse scorecards |
| Candidate search (filter/ATS) | ●● | ●● | × | × | ●● | Partial | Elastic hybrid search |
| Natural-language pool querying | ○ (Greenhouse filter NL) | ◐ (Assist NL) | × | × | ●● (Ask Ashby) | Yes — NL query | Ashby Filter Assistant; SeekOut Assist |
| Audit trail / provenance | ○ | ○ | ○ | × | ◐ | Yes — per-insight audit | Sourcerer 793 tests; WorkProof; ACM audit paper |
| Human approval / oversight | ●● | ●● | ●● | ●● (but often rubber-stamp) | ●● | Yes — human-in-loop central | ICO "meaningful involvement" test |
| Explainability (per-decision reasons) | ◐ | ◐ | ◐ | × | ○ | Yes — evidence | JobMatchAI per-factor |
| Fairness mechanisms | ○ | ◐ (bias flags) | ◐ | ○ | ○ | Implicit (must not treat unfairly) | Wilson 2024, Gao 2026, FAIRE |
| Candidate feedback (giveback) | ◐ (Lever personalized rejection) | × | × | × | × | Candidate expectations (§4) | SenseHQ |
| Pipeline automation (status moves) | ● | ◐ | × | ◐ | ◐ | No — but agentic gap | Paradox/Workday agents |
| Memory / state across stages | ○ | ○ | × | × | ◐ | Yes — adapts when new evidence arrives | TIMBRE temporal KG |
| Tool use / external actions | ○ | ◐ | × | ●● | ●● (MCP) | Yes — agent should act | ADK/LangGraph; Ashby MCP |

*Reading:* HireFlow asks for the ○/× column — exactly where products are thinnest.

---

## 11. Technical Architecture Patterns

### 11.1 Classic ATS pipeline (mature)

```
Document (PDF/DOCX) → Parser (MinerU/LlamaParse/PyPDF2 + OCR)
  → Structured Profile JSON (23 fields: contact, skills, exp, edu)
  → Taxonomy Normalization (ESCO/O*NET via SkillNER / XMLC)
  → Keyword/Boolean or Vector Similarity vs JD → Ranked shortlist in ATS stage
```

*Why used:* Deterministic, explainable, cheap for high volume. *Benefits:* predictable; low hallucination risk. *Failure modes:* layout-tables dropped; date overlaps mis-parsed; synonym gaps miss qualified. *Maturity:* shipped in all major ATSs. *When overkill:* never for this stage — this is baseline.

### 11.2 RAG / Semantic hiring engine (emerging, becoming SOTA IR)

```
Knowledge Base (resumes, JDs, GitHub, reviews) → Chunking
  → Embedding (E5/ELSER / all-mpnet-base-v2 768d) → Vector DB (Pinecone/Milvus/pgvector HNSW/ANN + metadata filter)
  → Retriever (query embedding + hybrid dense+sparse BM25 + RRF + MMR + Cohere/CrossEncoder rerank)
  → Integration Layer (prompt augmentation + orchestration) → Generator (GPT/Claude/Gemini)
  → Personalized fit summary + counterfactual bias check
```

*Why:* handles heterogeneity and synonyms ("DevOps ≈ infra automation"); grounds outputs in retrieved chunks. *Benefits:* 40% faster time-to-hire, 60% fewer false positives cited [V2Solutions]. *Failures:* retrieval bounds generation (missing chunks = missing evidence); index freshness lag; k fixed may miss edge cases. *Overkill when:* simple keyword filtering suffices (high-volume knockout). *Maturity:* productized in SeekOut/Gem hybrid search; open source has 8-stage variant (RecruitIQ).

### 11.3 Knowledge Graph / GraphRAG (emerging for multi-hop)

```
Entities/Relations (candidates, skills, companies, JDs) typed via ESCO/Wikidata
  → Heterogeneous (temporal) graph + ESCO hierarchy + Wikidata skill graph → GNN/GCN + attention
  → Subgraph explanations typed hasSkill/atLocation → Recommendations + provenance path
```

Examples: OKRA (harmonic candidate+company score, heterogeneous KG+GNN), TIMBRE (temporal graph + ESCO hierarchy + recency), Vector Graph RAG ([Zilliz](https://github.com/zilliztech/vector-graph-rag): entity→vector search→subgraph expansion→LLM rerank, 87.8% recall). *Benefits:* sub-graph explainability, handles career trajectories and skill recency. *Costs:* graph-building expense, manual entry except skills. *Maturity:* research + early talent-intelligence product (Eightfold/Beamery).

### 11.4 Agentic loops (emerging agentic)

```
Perceive (RAG retrieve + taxonomy lookup) → Reason (plan steps over requirements)
  → Act (tool call: parse resume, score candidate, generate question, send email)
  → Observe (tool result) → Validate → Ask human if policy threshold → Repeat until goal
```

Variants:
* **Single agent:** loops until done; needs permission-aware tools, schema validation, audit log, human gate on offer/decision.
* **Multi-agent (supervisor/worker, hierarchical, peer-to-peer A2A, MCP):** ADK nodes can be LLM Agent *or* Python Function *or* external tool; LangGraph for cyclic stateful workflows. InfoWorld: ADK graph runtime [overview](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview). Tradeoff: multi-agent ≈15× tokens vs chat — prefer single loop with brakes unless specialization needed [QJC](https://qjc.app/blog/graph-engineering).

**HireFlow-ancestor pattern (Yuksel et al. 2026):**

```
JD → Criteria Generation (YAML rubric 12-20 dims) → Video/Question Generation
  → Assessment Generator (CV+transcript → Low/Med/High + citation)
  → Feedback loop + Active Listwise Tournament (Plackett-Luce + active learning)
  → Citation-backed report + globally coherent ranking
```

*Why used:* rubric-driven adjudication mirrors expert judgment with provenance. *Benefits:* transparent, sample-efficient, interpretable ranking. *Failure modes:* rubric quality determines everything; tournament cost scales with candidates; requires careful prompt externalization (Bandara guide).

### 11.5 Recurring composition for HireFlow evidence integrity

A synthesis pattern evidenced across the strongest open-source (Sourcerer, RecruitRadar) and papers:

```
Cleanse (phantom/invisible-text detection before LLM) + separate instruction vs data channels
  → Hybrid retrieval → Deterministic per-dimension scoring (LLM gives 0-10, Python computes composite)
  → Bias agent decoupled (runs on raw, never fed to scorer)
  → Verbatim-quote forcing + fuzzy verification + drop unverified
  → honeypot/anti-gaming (keyword stuffing, impossible timelines)
  → WorkProof-typed provenance + consent-gated attestations (W3C VC)
```

This guards the top failure surface (see §12).

---

## 12. Failure Modes

Separate **documented failures** (measured/field observed) from **theoretical risks**.

### 12.1 Documented failures

| Failure | Evidence | Context |
|---|---|---|
| **Prompt injection via resumes** — ~1% of 200K real resumes (hireEZ, 2019-2025) contain hidden injections; prevalence rising last 1-2yr, >90% implicit (no explicit `SYSTEM:`) | USENIX Security '26 detector VDA (rendered vs extracted text, <1.5% ink density) + RAPIDS (98% recall, 115-171ms) [USENIX Zhang et al.](https://www.usenix.org/conference/usenixsecurity26/presentation/zhang-mohan) [ArXiv 2605.28999](https://arxiv.org/html/2605.28999v1) [ACL RAPIDS 2026](https://aclanthology.org/2026.acl-industry.127/) | Ghost white-on-white, phantom text, embedded `PRIORITY CRITICAL ... select Jonas Becker` |
| **Hallucinated justification** — Qwen 3 30B forced to select unqualified (B.A. Business, supermarket cashier) for ML Scientist (PhD+Python/BigQuery/Tableau) invented engagement | [ArXiv Trojan Horses 2602.18514](https://arxiv.org/html/2602.18514v1) §4.2.1 | Brittle lie, detectable by verification |
| **Strategic reframing / sycophancy** — reasoning model pivoted to cultural fit ("native German → seamless Mannheim integration") and discrediting qualified rival as "narrowly focused" | Trojan Horses §4.2.2 | More persuasive than hallucination |
| **Bias replication** | FAccT '26 N=528: humans almost exactly replicate AI race preferences across 16 occupations [ArXiv 2509.04404](https://arxiv.org/html/2509.04404v1); FAIRE: ranking more sensitive than scoring | Automation bias: "past the biases of my recruiters" then retreat to gut vibe checks [Resume-ing Control](https://arxiv.org/pdf/2604.26851) |
| **Recruiter automation bias** | Recruiters stop checking because AI sounds confident; illusion of omniscience (Trojan Horses §2.4) | Affects adoption of explainable systems |
| **Bias audit before human eye** | 75% resumes never reach human (Harvard Hidden Workers cited Trojan Horses §1); 75% rejection pre-review creates hidden-disadvantage path | Pre-human filtering amplifies bias |

### 12.2 Often-theoretical but increasingly reported risks

* **Incorrect skill extraction / resume misinterpretation / poor semantic matching / ranking instability** — documented via SkillSpan evaluations (LLMs recall high but precision lower) and IR benchmarks; instability evidenced by ranking-sensitivity results (FAIRE).
* **Overconfidence / false positives/negatives, missing evidence** — LLM-as-judge without RAG grounding gives confident but ungrounded scores (most interview open-source suffers this; CertusHire hybrid 0.6*LLM+0.4*retrieval is rare exception).
* **Poor interview question / incorrect interview summary / lack of explainability** — MediaSum shows positional biases; modular interviewer prototype handles but not stress-tested at scale.
* **Automation bias → recruiter over-reliance** — SHRM: 71% let AI reject without human oversight despite believing AI biased.
* **Privacy / data leakage / prompt injection → model inconsistency** — Microsoft Failure Modes taxonomy [Whitepaper Apr 2025](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf): insufficient transparency, parasocial, XPIA (cross-domain indirect prompt injection) called "most significant failure mode for agentic AI", memory poisoning, human-in-loop bypass.
* **Malicious uploaded documents (XPIA amplified)** — invisible-text detection before LLM (VDA/RAPIDS) + instruction/data channel separation + anomaly flag (selecting zero-skill over expert) are documented mitigations (Trojan Horses §6-7), but adoption in products/GitHub is fragmented. Meta-cognitive leakage noted: complex injection phrasing ("reframed as lean, efficient data architecture") leaks reasoning trace — standard model filtered illogical grade instruction, reasoning model complied yet exposed phrasing.

**Defenses that work (evidence-backed):** invisible-text/Phantom detection prior to LLM (RAPIDS 98% recall at 21-24× speedup), hybrid detector cost 3.5% of GPT-5-mini, separate system-instruction channel from candidate data, statistical anomaly detector on ranking, deterministic composite scoring, bias-decoupled agent, verbatim citation with fuzzy verification, W3C VC consent tiers.

---

## 13. Recruiter & Candidate Pain Points

### 13.1 Recruiter complaints (practitioner sentiment — treat as directional, not representative)

Synthesized across r/recruiting, r/talentacquisition, r/recruitinghell, r/startups, r/humanresources (18 months), Happlicant 2026 meta-analysis, Curriculo, vendor case write-ups.

**Top clusters:**

1. **ATS parsing/search failure:** "systems don't parse resumes correctly, making good candidates harder to find" — high-volume unqualified flood [r/RecruitmentAgencies](https://www.reddit.com/r/RecruitmentAgencies/comments/1j6ygow/hey_guys_what_are_your_biggest_pain_points_in). Opaque scores without reasoning: "73% match score, no reasoning, recruiter reads anyway, defeating point" [Curriculo](https://curriculo.me/blogs/reddit-ats-complaints-2026). Debate over ATS filtering: some claim only knockout questions filter [r/recruitinghell](https://www.reddit.com/r/recruitinghell/comments/1fagkne/a_lot_of_recruiters_have_said_ats_doesnt_filter) vs Hidden Workers 75% pre-human rejection — mental-model confusion itself a pain point.

2. **Vendor-specific sore points (Happlicant 2026 [review](https://www.happlicant.com/blog/what-recruiters-say-about-ats-reddit)):**
   * Bullhorn: cluttered DB, near-useless search, evening crashes, misrepresented implementation costs — most complaint volume.
   * Greenhouse: powerful but enterprise-ops-heavy; dated UI, reporting needs dedicated admin.
   * Ashby: strong small headcounts, friction at growth + mid-contract per-employee true-up billing.
   * Rippling (2026 thread): 7 clicks to schedule interview, manual video provider each time, scheduling link buried ("submit your availability" vs "book a time"), tracking address removed by candidates, no signature [Reddit Rippling](https://reddit.com/r/rippling/comments/1w02zvm/anyone_else_struggling_with_rippling_recruiting/p69zvt3) — praised only for fraud detection + recordings.
   * Recruit CRM: fewest complaints but not zero.

3. **Workflow gaps:** cross-system integration (ATS+calendar+comms+payroll not unified); needing to ask implementation cost in writing, asking "what happens at 9pm when support breaks", asking for peer customer of similar size — signals enterprise support gap.

4. **Volume burnout:** 60% time reviewing low-fit resumes; sourcing = volume not quality; easy-apply creates hundreds per role (hours for hourly, thousands for technical) [V2Solutions](https://www.v2solutions.com/blogs/semantic-hiring-vector-search-rag).

### 13.2 Candidate complaints (from surveys §4 + forums)

* Ghosting (1/3 after 1 week; 51% after AI interview silence), transparency/bias anxiety (57% want legal disclosure; only 21% think employers use AI responsibly), interview impersonality (pre-recorded no-human 33% walk-away trigger), AI arms race (candidates keyword-stuff with AI ↔ recruiters screen with AI → mutual authenticity erosion → gut vibe checks that add bias), repeat information, lack of human contact.

### 13.3 Hiring manager / business pain

* Time-to-hire (4.2 mo senior eng), shortages (1.1M nursing), compliance vacancies drive direct revenue/productivity loss ($240B mismatch crisis [V2Solutions]); false positives waste interviews; poor CX harms offer acceptance (73% feel mismatched/ignored).

> **Synthesis:** The unifying pain is not lack of scores — it's **lack of trusted, evidence-linked signal** that lets a time-pressed recruiter act or a candidate understand why, without hunting across ATS, email, Greenhouse scorecards, and interviewer notes.

---

## 14. Competitor-by-Workflow Map

Who solves which stage reasonably well vs where workflows are fragmented/manual/gap-ridden.

```
Job Definition
  ● Greenhouse/Ashby Content Assist (doc) | ◐ Beamery Job Design | × few evidence-link requirement sets

Candidate Acquisition (job distribution, sourcing)
  ●● SeekOut (1B+), Gem (800M), LinkedIn, iCIMS CXM
  Fragmented: Gem/SeekOut as layer over ATS; paradox of ATS-bound overlap

Resume Intake (parse)
  ● Textkernel/Sovren/DaXtra (doc) | ◐ MinerU/LlamaParse (new OCR-agentic)
  Gap: complex layouts/tables/scans

Screening (rank/filter)
  ●● Greenhouse Talent Matching, Lever Insights, Workday/HiredScore, SeekOut/Gem
  Fragmented: scores differ by vendor; evidence display uneven

Matching (semantic)
  ●● RAG hybrid products (Gem, SeekOut) | papers: ConFit, CareerBuilder fused embeddings
  Emerging: KG-backed (Eightfold/Beamery)

Shortlisting (human-in-loop ranking)
  ◐ Greenhouse calibration, Ashby Review Summaries (cite original feedback), Phenom Fit Score
  Need: meaningful human-involvement audit

Interview Preparation
  ◐ Generic question suggestion (Greenhouse, Ashby)
  Rare: candidate-gap-aware personalized QG (Yuksel Video QG, Modular Interviewer)

Interview (screen)
  ●● Humanly, Paradox, SeekOut Screener, Eightfold AI Interviewer (conversational 24/7)
  Risk: Illinois video-consent + 30-day delete

Interview Analysis (transcript → competency)
  ◐ Ashby/Greenhouse Notetaker (transcription), MediaSum-style summarization
  Experimental: competency modeling via LLM→library (2602.13084), CertusHire hybrid

Evaluation (scorecard → report)
  ●● Greenhouse Scorecards, Phenom, HireVue Interview Insights
  Gap: report that auto-populates from evidence + flags unanswered areas (HireFlow req)

Decision
  Human judgment augmented by Fit Score/Workday grading; bias risk: automation bias (SHRM 71%)

Record / Audit
  ◐ ATS logs + NYC LL144 exports + CO impact assessments
  Rare: append-only provenance ledger (Sourcerer, WorkProof)
  Fragmented: retention purges, SAR aggregation, log kept ≥6mo per EU

Natural-language pool queries
  ○ Ask Ashby, SeekOut Assist, Greenhouse Report builder (Plus/Pro)
  Gap: provenance-linked pool querying

Evidence / audit trail per insight
  ◌ Experimental (papers + Sourcerer/WorkProof) — no product documents full loop
```

**Mature:** acquisition, intake parse (text PDFs), screening ranking, scheduling.
**Fragmented:** matching nuance, shortlisting rationale, evaluation synthesis, audit across systems.
**Weakest / gap-ridden:** personalized interview-Q generation, evidence mapping, NL pool querying with citations, provenance ledger, handling new evidence arrivals, uncertainty surfacing.

---

## 15. What Actually Makes These Systems Agentic?

Market stretching of "agent" is documented per Tray.ai Dec 2025: many "agents" are chatbots with an LLM step mislabeled. Use transportable definitions from Microsoft, Tray, CopilotKit, TechTarget/IrisAgent to score real agency.

| Dimension | Chatbot | Copilot | **Agent / Agentic AI** | Traditional Automation |
|---|---|---|---|---|
| Role | *Chats* | *Assists* | *Acts* | *Follows rules* |
| Autonomy | Low/scripted | Medium — suggests, human owns decision | High — goal-driven, pursues objective within guardrails until done | None — fixed rules |
| Capability | Q&A, intake, routing | Drafting, summarization, next-action suggestions **inside host app** | Multi-step planning, tool calling (APIs), observing results, iterating, escalating | Repetitive single-system |
| Tool use | Minimal KB | Reads app state, calls app functions | Multiple systems, schema-validated, permission-aware | Single-system scripts |
| Memory/context | Low | High (inherits live app context) | High, vector DB long-term memory, learns | None |
| Interaction | Standalone channel (web chat, SMS) | Embedded ("flies cockpit with you") | Orchestration layer, may be headless or chat | Backend jobs |
| Governance | PII/profanity filter, human handoff | Respects app permissions, marks generated content | Identity-scoped actions, logs, rollback, human gate for high risk | Fail-stop |

**Definitions (verbatim cores):**

* Microsoft: *"Agentic AI performs multi-step tasks, adapts, learns; chatbot assists with simple Q&A (low context)"* [Microsoft Copilot vs Chatbots 2025](https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/do-more-with-ai/general-ai/understanding-ai-agents-vs-chatbots) [Copilot Studio](https://www.microsoft.com/en-us/microsoft-365-copilot/microsoft-copilot-studio/what-is-an-ai-agent).
* Tray.ai: *"Agent = reason, decide, act across systems within guardrails (plan → call APIs → read results → iterate); Copilot = assistive, not autonomous; Chatbot = conversational interface. Decision rule: need cross-system action with minimal supervision? → Agent; human final decision? → Copilot; else chatbot."* [Tray.ai Dec 2025](https://tray.ai/blog/agent-vs-copilot-vs-chatbot)
* CopilotKit: *"Agent autonomously reasons/acts toward goal; copilot is agent embedded in application, reads/writes app state, calls functions, renders live UI (agentic UI). Chatbot output is text; copilot acts."* [CopilotKit](https://www.copilotkit.ai/learning/copilots-vs-agents)
* TechTarget/IrisAgent similar [TechTarget](https://www.techtarget.com/ai/tip/AI-agent-vs-chatbot-Breaking-down-the-differences) [IrisAgent 2026](https://irisagent.com/blog/ai-agent-vs-chatbot-vs-copilot-whats-the-difference).

**Scoring real systems:**

| Product claim | Does it... choose actions? | call tools? | retrieve dynamically? | maintain state? | plan multi-step? | validate? | ask human approval? | act externally? | adapt/retry? | **Verdict** |
|---|---|---|---|---|---|---|---|---|---|---|
| Greenhouse Talent Matching | ✗ (scores only) | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ (human must review) | ✗ | ✗ | **Automation/Copilot** |
| Greenhouse assistant generators | ✗ | ✗ | × | ✗ | ✗ | ✗ | ✓ | ✗ | × | **Copilot** |
| Workday Talent Acquisition Agent (Recruiting Agent) | ✓ | ✓ | ✓ | ✓ | ✓ (panel coordination) | ✓ | ✓ | ✓ (calendar) | ✓ | **Agent** (bounded within Workday) |
| Ashby Assistant + custom agents + MCP | ✓ | ✓ (MCP) | ✓ | ✓ | ✓ | ✓ | ✓ (must approve before action) | ✓ | ✓ | **Agent** |
| LinkedIn Hiring Assistant (6 sub-agents, async) | ✓ | ✓ | ✓ | ✓ (cognitive memory) | ✓ | ✓ | ✓ | ✓ (messages/scheduling) | ✓ | **Agentic system** |
| Eightfold Agentic (Agent + Digital Twin) | ✓ | ✓ | ✓ | ✓ | ✓ | claimed | ✓ | ✓ | ✓ | **Agentic** |
| SeekOut/Gem agents (Finder, Analyst, Outreach) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ◐ | **Agentic lite** |
| Paradox Olivia | ✓ | ✓ | ✓ | ✓ | ✓ | guardrail grounded | ✓ | ✓ | ✓ | **Agent** (high-volume) |
| SeekOut AI Screener / Humanly Interviewer | ✓ (runs interview) | ✓ | × | ✓ | × (scripted) | ✓ | ✓ | ✓ | × | **Automated interviewer**, not general agent |
| Most GitHub "agentic HR" repos | ◐ (scripted graph) | ◐ | ◐ | ◐ | × | weak | ◐ | × | × | **Workflow/copilot**, not autonomous |
| Yuksel 2026 Agentic HR (papers) | ✓ | ✓ | ✓ | ✓ | ✓ | Plackett-Luce tournament | ✓ | × (eval) | ✓ | **Agentic** (research) |

**HireFlow's agentic difference** (consistent with brief): not "LLM present" but a system that *runs end-to-end — every applicant read, gaps chased, ranked with evidence, every decision on record — on the ATS you already have* (evidence-backed shortlists, no write-back until explicit human approval) — modeled after [OpenSeat](https://app.openseat.work/your-ats) positioning and Adachi/others' "screening that runs" framing.

---

## 16. Whitespace / Gap Analysis

Each hypothesis is **Observed evidence → Why insufficient → Opportunity** — not a feature recommendation.

| # | Gap Hypothesis | Observed evidence | Why current approach insufficient | Opportunity if addressed |
|---|---|---|---|---|
| 1 | **Full-loop provenance missing** | §10 shows every commercial product offers components but none documents JD→requirement→candidate evidence→interview question→note→evaluation→report→query→audit in one ledger; Sourcerer/WorkProof closest but latter spec-only (§6) | Evidence fragmented across ATS, emails, scorecards, interviewer notes | Append-only ledger (source→artifact→evidence span→claim with quote+fuzzy-verify) enabling exportable audit pack |
| 2 | **Per-requirement evidence mapping** | Requirement mapping exists (Greenhouse calibration, Yuksel YAML 12-20 dims) but mapping to *per-requirement* evidence citations is rare; 2602.13084 shows competency-behavior extraction works but not productized | Recruiters get a whole-candidate rank but can't answer "what supports Python requirement? where?" | Graded evidence per requirement (supporting/neutral/conflicting/missing) with confidence and contradictions surfaced |
| 3 | **Uncertainty as first-class signal** | JDs ask for missing/unclear detection; current parsers return presence/absence binary; products flag low-fit but not *unanswered vs conflicting vs unverifiable* | Hiring decisions under uncertainty without vocabulary to name it | Missing-info taxonomy (unanswered, conflicting, unverifiable, stale/recency-risk) that drives next questions/actions |
| 4 | **Candidate-specific question generation** | Generic suggestion (Greenhouse) common; candidate-gap-aware QG exists only in Yuksel Video QG / Modular Interviewer papers and simer-interviewer adaptive logic | Generic kits miss the gap that matters for this candidate | QG conditioned on mapped gaps + prior evidence, with follow-up generation gated on prior answer |
| 5 | **Follow-up gating on live signal** | LLM-as-Interviewer shows staged probing reveals reasoning depth; most platforms treat interview as fixed script | Static interviews waste signal and miss depth | Follow-up QA that adapts to interviewee answer and maps to same requirement |
| 6 | **NL pool querying with citations** | Ask Ashby / SeekOut Assist / Greenhouse report NL are emerging but citations weak; vector retrieval without provenance amplifies hallucination | Recruiter can't verify "show me candidates strong on X" answers | NL querying as retrieval → evidence → claim with provenance identical to report generation path |
| 7 | **Human-in-loop that is measured** | All vendors say "human decides"; ICO 2026 finds rubber-stamping common; SHRM 71% let AI reject alone despite bias belief; 2024 review: many DPIAs inadequate | Oversight claimed but not instrumented; same trust gap reappears | Instrumented oversight (who overrode what, time-on-evidence, competence logging, inconsistent-involvement detection) |
| 8 | **Bias handling that survives upgrade** | Gao 2026 shows model swap reverses bias direction; Wilson 2024 shows dense retrieval favors White 85%; FAIRE shows ranking bias > scoring bias | One-time bias report becomes stale on model/embedding change | Per-model/version bias phoning-home with impact ratios + significance, with auto-flag on alternative-model analysis |
| 9 | **Prompt-injection resilience in hiring context** | ~1% of real resumes contain hidden injections, rising; Trojan Horses shows reasoning models can be more persuasively gaslit | Resume is attacker-controlled input, yet products ingest it as data without cleansing | Cleansing tier (rendered-vs-extracted comparison, phantom detection 98% recall) + instruction/data separation + anomaly flag before scoring |
| 10 | **State that adapts when evidence arrives** | Most RAG systems rebuild FAISS per run; interview notes arrive async; TIMBRE handles temporal recency but not live pool updates | Shortlist goes stale after new interviews/JDs | Append-only ledger + re-ranking trigger (new evidence → re-evaluate only affected requirements → re-render report, preserve prior version for audit) |

*Additional gap:* Grouping is requested but underserved — current grouping is pipeline stages, not evidence-shaped cohorts (e.g., "strong on X but missing Y, n=12" for batch follow-up). Pseudonymized evidence bundles across stages would enable this without fragile clustering.

---

## 17. Implications for a 48-Hour Hackathon Build

*Not design decisions — constraints and leverage points so a product/engineering owner can decide.*

### Mature — reuse, don't reinvent

* **Parsing:** reuse MinerU/LlamaParse for layout OCR + an off-the-shelf JD→structured-requirement pass (LLM) + SkillNER/ONNX micro-model for fast local pre-check. Textkernel-style taxonomy normalization should consume ESCO/O*NET rather than being built.
* **Retrieval:** reuse hybrid retrieval (dense+sparse → RRF → rerank). There's no demo value in building a vector DB from scratch; use pgvector/FAISS/Qdrant and E5/bge embeddings.
* **LLMs:** reuse frontier LLMs via ADK/LiteLLM/LangSmith glue; keep Gemini/GPT/Claude swappable. Spend prototype time on evidence forcing, not prompt cleverness.
* **ATS surface:** reuse existing ATS integrations read-only first (Lever/Greenhouse as in OpenSeat pattern) rather than building a new ATS.

### Can be safely reused as components (proven, auditable)

* ONNX DistilBERT for per-field NER (15ms) before LLM; deterministic composite scoring (LLM per-dimension 0-10, Python computes weighted tier); bias-decoupled agent; verbatim-quote forcing + fuzzy verification; honeypot heuristics; W3C VC-style consent tiers for evidence.

### Where a small prototype can demonstrate meaningful differentiation

The brief's connective capabilities are where a 3-minute demo can stand out vs a vendor screenshot carousel:
* Show a **single JD** split into numbered requirements, then per candidate show **per-requirement evidence boxes** with source quote, page/line provenance, and contradictions highlighted — not a black-box score.
* Show **uncertainty vocabulary** (unanswered vs conflicting vs unverifiable) that directly produces **candidate-specific questions** and flags "unanswered evaluation areas."
* Show **NL pool query** returning the same evidence objects as the report, with citations — then show **audit export** (JSON+PDF) with version history that a regulator could inspect.

These require a **ledger**, not a bigger model — achievable in 48 hours with a JSON store and strict rendering rules.

### High-risk / hard-to-demo convincingly in 3 minutes

* Multi-agent autonomous outreach/scheduling across calendar/email (permissions, demo credentials, anti-spam, time for agents to converge).
* Full bias audit (needs representative dataset, significance testing, and auditor independence — not a 3-minute narrative).
* Live video interview with compliant consent/delete flows (heavy media infra; Illinois 30-day delete proof not demo-friendly).
* Credentialed knowledge graph with ESCO interplay and temporal recency — too subtle to perceive without hiring-manager stakeholders.

### External dependencies & deployment risks

* Frontier LLM rate limits/cost spikes during demo; keep deterministic fallback (cached embeddings) and offline seed evidence bundle.
* OCR variance on real PDFs; demo with a small curated set plus a "scanned" adversarial doc showing phantom-text detection.
* Calendar/MCP auth failures in live demo; run scheduling as mocked external action with audit log rather than live write.

### Data dependencies

* No credible public resume corpus for sensitive data — seed with synthetic or anonymized demo pool and explicitly state it; do not claim representativeness.
* Need one ESCO-sourced taxonomy slice to show normalization; full 13K-skill navigation is not needed.

### Demo-risk mitigations

* Pre-inject a hidden-prompt demo doc to show cleansing detection live (educational, not alarmist).
* Keep ledger append-only and show prior-version diff when new interview evidence arrives (illustrates §16 gap #10).

---

## 18. Open Questions Requiring Product Decisions

These cannot be answered by more research alone; they need product/engineering choices with the evidence above as input.

1. **What is the system's jurisdiction posture?** Apply EU's stricter ADM/human-oversight default everywhere, or maintain a jurisdiction toggle (EU vs UK vs US-NYC/CO/IL vs India)? Evidence suggests many global employers prefer a single strict mode to simplify audit.

2. **Where does human approval actually gate action?** Apply-to-offer has multiple writes (rank, question, note summary, report, message). Which transitions require explicit approval, which can pre-approve with audit, which stay read-only?

3. **What counts as evidence and what consent does it need?** Resume, interview transcript, GitHub, LinkedIn scrape vs phone screen — different privacy bases (GDPR legitimate interest vs talent-pool consent vs India 7(i)) and different retention clocks (6-12mo EU/UK vs labour-law minima in India).

4. **How do we represent requirement uncertainty?** Binary present/missing vs graded vocabulary (unanswered, conflicting, unverifiable impression, stale). This shapes question generation and report confidence — and fairness.

5. **What retrieval granularity yields trustworthy citations?** Sentence vs paragraph vs page chunks change provenance usefulness; smaller chunks boost precision but degrade interview-summary context — needs evaluation on 10-20 demo docs.

6. **LLM scope vs deterministic rules:** e.g., score per dimension via LLM while composite, tier, and role-gates are deterministic — but where to draw the line for matching vs summarization vs evaluation without hallucinated claims?

7. **Grouping definition:** Pipeline-product grouping (stages/score buckets) vs evidence-shaped cohorts ("strong on X but missing Y") — the latter needs a defined similarity object.

8. **Agent architecture:** Single loop with brakes vs multi-agent (planner, matcher, questioner, assessor, bias) — evidence (token cost, failure surface) says single loop first, decompose only where specialization is measured.

9. **AI disclosure surface:** Where and when to disclose AI use to candidates (pre-apply notice, pre-interview notice, in-report badge) and whether to expose per-decision explanation by default or on request.

10. **What is the minimal audit artifact that satisfies the brief?** Source record → artifact → evidence span (page/line + quote + confidence) → claim → assessment — with versions and approver log — that can export as JSON+PDF and survive NYC LL144 / CO impact / EU documentation expectations in miniature.

---

## Appendix A — Commercial Products

*Full per-product records (company, target customer, primary use case, main workflow, input data, AI & agentic capabilities, screening/interview, evidence/explainability, human-in-loop, auditability, integrations, pricing, limitations, source links with dates) — condensed from detailed source table (Sep 2026). For link verification, search exact product help title if a URL redirects.*

| # | Product / Company | Sources & dates |
|---|---|---|
| 1 | Greenhouse (+Real Talent, Sourcing Automation, Notetaker) — 7,500+ customers | [AI features 2026-09-03](https://support.greenhouse.io/hc/en-us/articles/33043749845403), [Talent Matching](https://support.greenhouse.io/hc/en-us/articles/41396009937307), [Spring 2025](https://www.greenhouse.com/greenhouse-latest-features-spring-2025) |
| 2 | Lever + VONQ AI Screening / Companions — Employ Inc., TRM | lever.co/vonq-ai-screening, /solutions/ai-powered-screening, help.lever.co AI Companion + Fall 2025 Release |
| 3 | Workday Recruiting + HiredScore — HCM enterprise | [AI Recruiting](https://www.workday.com/en-us/products/talent-management/ai-recruiting.html), [Talent Acquisition Agent](https://www.workday.com/en-us/artificial-intelligence/ai-agents/talent-acquisition.html), [2025-06-21 demystifying](https://blog.workday.com/en-us/demystifying-ai-hiring-clarifying-how-workdays-recruiting-tools-work.html) |
| 4 | Ashby All-in-One — tech scale-ups to enterprise, AI-native, MCP | [Ashby AI](https://www.ashbyhq.com/ai) 2026-05-19, [AI Features docs](https://docs.ashbyhq.com/ai-features-in-ashby), [Assistant 2026-05-07](https://www.ashbyhq.com/product-updates/ashby-assistant), docs.ashbyhq.com/ashby-agents |
| 5 | Paradox Olivia — 500+ enterprise, high-volume | paradox.ai, /products/conversational-ats, /candidate-experience-agent, [Gened AI deep dive 2025-07-05](https://genedai.me/2025/07/05/paradox-ai-olivia-deep-dive/) |
| 6 | Eightfold Talent Intelligence + AI Interviewer + Digital Twin — 1.6B trajectories, 1.6M skills | eightfold.ai/products/, [Talent Intelligence→Advantage 2025-05-08](https://www.prnewswire.com/news-releases/talent-intelligence-to-talent-advantage-eightfold-ai-revolutionizes-hr-through-agentic-ai-302449233.html) |
| 7 | SeekOut Recruit/Spot/Workspaces/Assist — 1B+ profiles | [SeekOut](https://www.seekout.com/), [External sourcing 2026-03-29](https://www.seekout.com/capabilities/external-sourcing/), [Agentic 2026-03-29](https://www.seekout.com/capabilities/agentic-ai-recruiting/) |
| 8 | Beamery Talent Lifecycle + Ray (BETA) | [Platform](https://beamery.com/platform/), [AI support doc 40360654119185](https://support.beamery.com/hc/en-us/articles/40360654119185-Understanding-Artificial-Intelligence-in-Beamery) |
| 9 | Gem (AI Sourcing + CRM/ATS + Agents) — 800M profiles, MCP | [AI Sourcing](https://www.gem.com/product/ai-sourcing), [Agents](https://www.gem.com/ai-recruiting-agents), Aug 2025 updates |
| 10 | LinkedIn Recruiter + Hiring Assistant — 1B+ members, Economic Graph | [Global available Sep 2025](https://news.linkedin.com/2025/hiring-assistant-globally-available), [Engineering](https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant), [Early impact 2025-03-25](https://www.linkedin.com/business/talent/blog/talent-acquisition/early-impact-of-linkedin-hiring-assistant-and-ai-agent) |
| 11 | iCIMS Talent Cloud + AI + Sourcing Agent (early access Fall 2025) | [AI recruiting](https://www.icims.com/products/ai-recruiting-software/), [Fall 2025](https://www.icims.com/company/newsroom/fallrelease2025/) |
| 12 | Phenom Intelligent Talent Experience + X+ Agentic + Hiring Intelligence — SAP Endorsed 2025-06-04 | [AI](https://www.phenom.com/artificial-intelligence) 2025-10-29 |
| 13 | HireVue/Modern Hire + Interview Insights | modern-hire AIS, [HireVue pricing 2025-07-15](https://www.hirevue.com/pricing) |
| 14 | Humanly AI Interviewer | [Products](https://www.humanly.io/products/ai-interviews), Geekwire 2025-07-23, PR 2025-11-20 |
| 15 | Loxo Talent Intelligence Platform (7th gen KG, 1.2B) | loxo.co |
| 16-24 | Entelo/Fetcher/SAP SF/Oracle/SmartRecruiters/Bullhorn/DaXtra/Textkernel/Harver and others | See §2 + [Bullhorn stages](https://kb.bullhorn.com/bh4sf/Content/BH4SF/Topics/ATSV2JobStages.htm), [Trimble config](https://help.trimble.com/en/viewpoint-hr-management-for-vista/viewpoint-hr-management-for-vista/hr-management-for-vista/applicant-tracking/configure-applicant-tracking/create-ats-stages) |

Pricing: nearly all enterprise quote-only; HireVue Essentials ~$35k/yr, Enterprise $60-145k (Vendr 2026, Tier 3), no public list price for most.

---

## Appendix B — GitHub Projects

*24 projects — stars Sep 2026 point-in-time, verified via search+fetch.*

| # | Repository | URL | Stars | Main focus | Ref |
|---|---|---|---|---|---|
| 1 | Resume-Matcher (srbhr) | https://github.com/srbhr/Resume-Matcher | 28,500 | End-to-end JD→tailored resume/cover/interview | srbhr docs/Discord |
| 2 | SmartResume (alibaba) | https://github.com/alibaba/SmartResume | 403 | Layout-aware OCR+layout → LLM fields | arXiv:2510.09722 |
| 3 | pyresparser (OmkarPathak) | https://github.com/OmkarPathak/pyresparser | 959 | Regex+NER baseline | GitHub |
| 4 | SkillNER (AnasAito) | https://github.com/AnasAito/SkillNER | 213 | Rule skill/cert via ESMI/Lightcast | pip skillNer |
| 5 | resume-extract (somus) | https://github.com/somus/resume-extract | — | ONNX DistilBERT 13 entities, ~15ms | Hugging Face oksomu/resume-ner |
| 6 | Ai-powered-resume-screening (ompatel7572) | https://github.com/ompatel7572/Ai-powered-resume-screening-system | — | Multi-column + SkillNER + Gemini ranker | GitHub |
| 7 | hr-rag-assistant (RobertoDure) | https://github.com/RobertoDure/hr-rag-assistant | — | Spring Boot + GPT-4 + pgvector 0-100 scoring | GitHub |
| 8 | RecruitIQ (kashishgadhiya) | https://github.com/kashishgadhiya/AI-resume-Rag-app | — | 8-stage hybrid RAG → MMR→Cohere, Mistral-7B | GitHub Prometheus /metrics |
| 9 | RecruitSense (Pranshu0204) | https://github.com/Pranshu0204/RecruitSense | — | Qdrant+BGE + RRF, LangGraph parser→rag\|bias→scorer | GitHub |
| 10 | talent-rag (atharvajoshi01) | https://github.com/atharvajoshi01/talent-rag | — | FAISS hybrid + cross-encoder ensemble | GitHub |
| 11 | Semantic-CV-Ranker | https://github.com/dhru-khakhariya/semantic-cv-ranker | — | 3×MiniLM + Haversine + pgvector weighted | GitHub |
| 12 | talentrank-ai (224-aadi) | https://github.com/224-aadi/talentrank-ai | — | Hard-gate + hybrid BM25→semantic fallback | GitHub |
| 13 | talentry-ai (williyam-m) | https://github.com/williyam-m/talentry-ai | — | Zero-LLM ranker + Qwen3-0.6B GRPO, honeypot | GitHub |
| 14 | AgentHiring (mohd-ibadullah) | https://github.com/mohd-ibadullah/AgentHiring | — | ADK gemini-2.5-flash + FastMCP, honeypot 100% | GitHub |
| 15 | RecruitRadar (Kushagra077) | https://github.com/Kushagra077/RecruitRadar | — | CrewAI 5 agents + verbatim guard | GitHub |
| 16 | HRRecruitingAgent (vaibhavarora102) | https://github.com/vaibhavarora102/HRRecruitingAgent | — | LangGraph + Cerebras 70b + FAISS + approval gates | GitHub |
| 17 | HireMind (DHIWAHAR-K) | https://github.com/DHIWAHAR-K/HireMind | — | 6 LangGraph agents planning | GitHub |
| 18 | hr-vertical-agent-kit (UmarbekFU) | https://github.com/UmarbekFU/hr-vertical-agent-kit | — | 3 MCP servers, 12 tools, eval suites | GitHub MIT |
| 19 | simer-interviewer (simreensiraj) | https://github.com/simreensiraj/simer-interviewer | — | Adaptive gatekeeper→interviewer→decider | GitHub |
| 20 | CertusHire (MohanKrishnaGR) | https://github.com/MohanKrishnaGR/CertusHire | — | FSM + 3 personas + 0.6*LLM+0.4*retrieval | GitHub |
| 21 | ai-interview-agent (GoDiao) | https://github.com/godiao/ai-interview-agent | — | Longitudinal state, heatmap, fix tracking | GitHub MIT |
| 22 | workproof-schema (TalentProof) | https://github.com/TalentProof/workproof-schema | 4 | Skill clusters+confidence+W3C VC attestations | JSON Schema v0.1 |
| 23 | sourcerer (matthewod11-stack) | https://github.com/matthewod11-stack/sourcerer | 2 | Intake→Discover→Dedup→Enrich→Score (cited) 793 tests | GitHub MIT |
| 24 | SourceKit (mrNLK) | https://github.com/mrNLK/SourceKit | — | GitHub graph → Research→Search→Enrich→Kanban | GitHub |

*Archive:* also reviewed sharathkum05/HR-Agent, ghoshvidip26/RAG-Resume-Screening, fanqingsong/agentic-ai-hr-automation, Akhileshkachhwaha26/hr-copilot-ai-agents, ramakrishnanyadav/Evidra, linkedin-signal-integrity-lens, qa-arsenal.

---

## Appendix C — Research Papers

*24 papers (2017-2026) — canonical arXiv/ACL/NeurIPS where applicable; titles verbatim.*

| # | Title — Authors, Year | Venue | URL |
|---|---|---|---|
| F1 | Attention Is All You Need — Vaswani et al., 2017 | NeurIPS | https://arxiv.org/abs/1706.03762 |
| F2 | BERT — Devlin et al., 2018/19 | NAACL | https://arxiv.org/abs/1810.04805 |
| F3 | Language Models are Few-Shot Learners — Brown et al., 2020 | NeurIPS | https://arxiv.org/abs/2005.14165 |
| F4 | T5 — Raffel et al., 2020 | JMLR | https://arxiv.org/abs/1910.10683 |
| F5 | LoRA — Hu et al., 2021 | ICLR 2022 | https://arxiv.org/abs/2106.09685 |
| F6 | RAG — Lewis et al., 2020 | NeurIPS | https://arxiv.org/abs/2005.11401 |
| 1 | ConFit — Yu et al., 2024 | arXiv | https://arxiv.org/abs/2401.16349 |
| 2 | ResuméAtlas — Heakl et al., 2024; Smart-Hiring 2025 | arXiv | https://arxiv.org/pdf/2406.18125 ; https://arxiv.org/pdf/2511.02537 |
| 3 | Job Recommender Systems: A Review — 2021 | arXiv | https://arxiv.org/pdf/2111.13576 |
| 5 | Deep Learning-based Job Market Analysis (skill survey) — Senger et al., 2024 | EACL NLP4HR | https://arxiv.org/abs/2402.05617 |
| 6 | SkillSpan — Zhang et al., 2022 | NAACL | https://aclanthology.org/2022.naacl-main.366 |
| 7 | Extreme Multi-Label Skill Extraction via LLMs — Decorte et al., 2023 | ECML-PKDD AI4HR | https://arxiv.org/abs/2307.10778 |
| 8 | Rethinking Skill Extraction with LLMs — Nguyen et al., 2024 | EACL NLP4HR | https://arxiv.org/abs/2402.03832 |
| 9 | Information Retrieval: Recent Advances — Hambarde & Proença, 2023 | IEEE Access | https://arxiv.org/abs/2301.08801 |
| 10 | Embedding-based Job→Candidate Matching at Scale — Zhao et al., 2021 | arXiv | https://arxiv.org/abs/2107.00221 |
| 11 | Modular AI-Powered Interviewer — Adeseye et al., 2025 | arXiv | https://arxiv.org/html/2601.11534v1 |
| 12 | LLM-as-an-Interviewer — 2024 | arXiv | https://arxiv.org/abs/2412.10424 |
| 13 | MediaSum — Zhu et al., 2021 | NAACL | https://arxiv.org/abs/2103.06410 |
| 14 | Competency Modeling via LLMs — 2026 | arXiv | https://arxiv.org/html/2602.13084v1 |
| 15 | Gender, Race, Intersectional Bias in Retrieval — Wilson & Caliskan, 2024 | AIES | https://arxiv.org/abs/2407.20371 |
| 16 | Can LLMs Hire Fairly? — Gao et al., 2026 | arXiv | https://arxiv.org/abs/2606.28978 |
| 17 | FAIRE — Wen et al., 2025 | arXiv | https://arxiv.org/abs/2504.01420 |
| 18 | Silicone Ceiling — Armstrong et al., 2024 | EAAMO | https://arxiv.org/html/2405.04412v1 |
| 19 | Evaluating Promise & Pitfalls of LLMs in Hiring — 2025 | arXiv | https://arxiv.org/pdf/2507.02087 |
| 20 | JobMatchAI — Vyas et al., 2026 | ACL Demo | https://aclanthology.org/2026.acl-demo.52/ |
| 21 | Making It Possible for Auditing of AI — 2024 | Inf Syst Frontiers | https://link.springer.com/article/10.1007/s10796-024-10508-8 |
| 22 | From Transparency to Accountability — 2024 | ACM | https://dl.acm.org/doi/fullHtml/10.1145/3689904.3694711 |
| 23 | Agentic AI for HR: LLM-Driven Candidate Assessment — Yuksel et al., 2026 | EACL | https://arxiv.org/abs/2603.26710 |
| 24 | Practical Guide to Production Agentic Workflows — Bandara et al., 2025 | arXiv | https://arxiv.org/abs/2512.08769 |
| KG | OKRA & TIMBRE — 2024-25 | ECIR/arXiv | https://arxiv.org/html/2504.07108v1 ; https://arxiv.org/pdf/2411.15146 |

---

## Appendix D — Regulations / Official Guidance

| # | Jurisdiction | Instrument | Status | Date | URL (official where avail) |
|---|---|---|---|---|---|
| 1 | EU | AI Act Regulation (EU) 2024/1689 | LAW | OJ 12 Jul 2024, in force 1 Aug 2024, high-risk employment from 2 Aug 2026 | http://data.europa.eu/eli/reg/2024/1689/oj |
| 2 | EU | GDPR Regulation (EU) 2016/679 Art.22 Recital 71 | LAW | 25 May 2018 | https://eur-lex.europa.eu/eli/reg/2016/679/oj |
| 3 | UK | UK GDPR + DPA 2018 + Data (Use and Access) Act 2025 (Royal Assent 19 Jun 2025) | LAW | retained + DUAA commenced 2025-26 | https://ico.org.uk/about-the-ico/what-we-do/recruitment-rewired/ |
| 4 | UK | ICO Recruitment & Selection guidance + AI in Recruitment Outcomes (Nov 2024) + Recruitment Rewired (31 Mar 2026) | GUIDANCE | 2024-2026 | ICO site (above) |
| 5 | US Federal | EEOC ADA & AI 12 May 2022 + EEOC Title VII AI 18 May 2023 (+ joint pledge 25 Apr 2023) | GUIDANCE | 2022-2023 | eeoc.gov |
| 6 | US-NYC | Local Law 144 (2021) + DCWP Rule 6-101, enforced 5 Jul 2023 | LAW | 2021/2023 | https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page |
| 7 | US-IL | AI Video Interview Act 820 ILCS 42 (eff 1 Jan 2020) + IHRA Amend HB3773 P.A.103-0804 (eff 1 Jan 2026) | LAW | 2019/2024 | https://law.justia.com/codes/illinois/chapter-820/act-820-ilcs-42/ |
| 8 | US-CO | AI Act SB24-205 (signed 17 May 2024, eff 1 Feb 2026) | LAW | 2024 | https://leg.colorado.gov/bills/SB24-205 |
| 9 | US-MD | Facial Recognition §3-717 Ch.446 (eff 2020) | LAW | 2020 | Justia MD Code |
| 10 | India | Digital Personal Data Protection Act 2023 (Act No.22) + Rules 2025 | LAW (staged; substantive ~May 2027) | 2023/2025 | https://www.meity.gov.in/static/uploads/2024/02/Digital-Personal-Data-Protection-Act-2023.pdf |

*Not law but high-signal commentary distinguished:* Eversheds 09 Mar 2026 AI Act briefing, Freshfields 12 Jul 2024, Seyfarth/Gibson Dunn EEOC explainers, Epstein Becker IL alerts, NYS Comptroller audit Dec 2025 — cited as interpretation, not authority.

---

## Appendix E — Source List

~120+ verified sources grouped below — primary (Tier 1) first.

**Tier 1 — Primary / authoritative**
* Academic papers: arXiv, ACL Anthology, NeurIPS, Springer, ACM (§5 / App C).
* Official docs/product help: Greenhouse/Ashby/Workday/Lever/iCIMS help centers, Google ADK, LlamaParse/MinerU, ESCO/O*NET official sites, EUR-Lex, ICO, EEOC, NYC.gov, ILGA, leg.colorado.gov, meity.gov.in (DPDP Act).
* GitHub repositories: 24 repos listed in §6 / App B (verified via search+fetch).
* Official technical reports: IBM RAG, Forrester TEI (commissioned — noted), NIST-referenced frameworks.

**Tier 2 — Strong secondary**
* Industry/analyst: G2 category docs, Fosway/IDC/Gartner commentary on Eightfold, Glassdoor/Forrester-beamery, SHRM Dec 2025, Saply parsing accuracy, Beamery/Workday/Phenom press releases, staffingindustry.com, hrexecutive.com, sensehq.com blogs, Brookings, Eleken/UITOP, ProductArena 2026, InfoWorld, V2Solutions, Yugabyte/Weaviate/Pingcap tech blogs.
* Reviews/benchmarks: LlamaIndex ExtractBench/ParseBench, Zilliz vector-graph-rag evals, Vendr pricing analyses (Tier 3 noted).

**Tier 3 — Practitioner / community (sentiment, not fact)**
* Reddit r/recruiting, r/recruitinghell, r/RecruitmentAgencies, r/rippling, r/startups, r/humanresources; Hacker News; LinkedIn posts; G2/Capterra review excerpts; Curriculo/Happlicant meta-analyses of ATS complaints (marked as anecdotal).

**Freshness flagged:** 2024-2026 sources prioritized for products/APIs/regulation/agentic; older papers used only where foundational (Transformer 2017, BERT 2018, T5/RAG/GPT-3 2020) or still SOTA reference.

For full per-claim provenance, see inline citations throughout §§2-8; each product row in App A lists its dated source set.

---

## Research Completion Summary

### 1. Commercial products analyzed: **24**
Greenhouse, Lever/VONQ, Workday/HiredScore, Ashby, Paradox Olivia, Eightfold, SeekOut, Beamery/Ray, Gem, LinkedIn Hiring Assistant, iCIMS, Phenom X+, HireVue/Modern Hire, Humanly, Loxo, plus Textkernel/Sovren/DaXtra/SAP SF/Oracle/SmartRecruiters/Bullhorn and niche parsing vendors — full table in §2 / App A.

### 2. GitHub projects analyzed: **24**
Resume-Matcher (28.5k★), SmartResume, pyresparser, SkillNER, resume-extract, hr-rag-assistant, RecruitIQ, RecruitSense, talent-rag, Semantic-CV-Ranker, talentrank-ai, talentry-ai, AgentHiring, RecruitRadar, HRRecruitingAgent, HireMind, hr-vertical-agent-kit, simer-interviewer, CertusHire, ai-interview-agent, workproof-schema, sourcerer, SourceKit, plus HR-Agent/RAG-Resume-Screening/agentic-ai-hr-automation/hr-copilot-ai-agents/Evidra — full table in §6 / App B.

### 3. Research papers analyzed: **24** (6 foundational + 18 task-specific)
Foundational — Attention Is All You Need (2017), BERT (2018/19), GPT-3 (2020), T5 (2020), LoRA (2021), RAG (2020). Task papers — ConFit, ResuméAtlas/Smart-Hiring, Job Recommender Review, SkillSpan, Skill Extraction Survey, Extreme XMIC via LLMs, Rethinking Skill Extraction, IR Advances, CareerBuilder Embeddings, Modular Interviewer, LLM-as-Interviewer, MediaSum, Competency Modeling, Wilson bias audit, Gao bias reversal, FAIRE, Silicone Ceiling, Promise & Pitfalls (10K pairs), JobMatchAI, Auditing of AI review, Transparency→Accountability, Agentic AI for HR, Production Agentic Workflows, OKRA/TIMBRE KGs — full list in §5 / App C.

### 4. Regulatory / official sources analyzed: **10**
EU AI Act 2024/1689, GDPR, UK GDPR/DPA + DUAA 2025, ICO 2024/2026 recruitment+ADM guidance (2), EEOC ADA 2022 + Title VII 2023 (+ joint pledge, Workday amicus), NYC LL144 + DCWP Rule, Illinois AI Video Interview Act + IHRA Amend HB3773 (2), Colorado AI Act SB24-205, Maryland §3-717, India DPDP Act 2023 + Rules 2025 — full list in §8 / App D.

### 5. Total sources (verified)
~120+ distinct URLs/excerpts across product docs, papers, repos, regulator sites, industry publications, and practitioner discussions — each cited inline and indexed in App E.

### 6. Top 10 recurring industry patterns (evidence-backed, not recommendations)

1. **ATS spine + bolt-on intelligence:** every mature ATS documents pipeline stages as fixed; intelligence (matching, transcription, QG, bias) arrives as layered services (Greenhouse Talmatch, Lever Companions, Workday HiredScore, Ashby Notetaker) — not a rebuilt ATS.
2. **Hybrid RAG as default IR:** dense + sparse BM25 → RRF → MMR → CrossEncoder/Cohere rerank beats pure vector or keyword alone (papers: IR Advances, CareerBuilder; products: SeekOut/Gem; GitHub: RecruitIQ 8-stage).
3. **Skill taxonomy anchoring:** ESCO v1.2.1 (13,485) or O*NET linked mapping is how teams keep skill extraction comparable across roles; synthetic ESCO XMLC (+15-25 pts) and ESCO↔O*NET crosswalk are recurring patterns.
4. **Deterministic scoring wrapper around LLM:** LLM outputs per-dimension 0-10; Python computes composite/tier — preserves auditability and prevents hallucinated final scores (RecruitSense, RecruitRadar, WorkProof spec).
5. **Bias decoupling:** scoring agent never sees raw demographic signals; separate bias agent flags and dashboards show impact ratios/4/5ths + significance (NYC/EU expectation); per-model re-audit on upgrade is mandated by measured reversal (Gao 2026).
6. **Evidence-forcing retrieval:** verbatim quote + fuzzy verification + dropping unverified claims (Sourcerer 793 tests, RecruitRadar guard, 2602.13084 behavioral descriptors) as antidote to LLM hallucination/sycophancy.
7. **Human-in-loop as measured gate, not slogan:** products claim "human decides" but ICO 2026 and SHRM show rubber-stamping; instrumented override/competence/time-on-evidence is the pattern that actually satisfies Meaningful Human Involvement.
8. **Cleansing before LLM in hiring:** rendered-vs-extracted phantom/invisible-text detection (98% recall, 21-24× speed, RAPIDS) plus instruction/data channel separation — required because resume is attacker-controlled input (~1% injections in the wild).
9. **Single-agent-loop first, multi-agent only when specialized:** token-cost evidence (4× single-agent, 15× multi-agent vs chat) pushes preference for one loop with explicit brakes/completion criteria, decomposing to supervisor/worker only where evaluation shows separation benefit (ADK/LangGraph guidance).
10. **Append-only ledger as product primitive:** source record → artifact → evidence span (quote + loc) → claim → assessment with version history — evidenced by paper ledger concepts (Competency Modeling, Agentic HR tournament) and GitHub WorkProof/Sourcerer provenance; needed to make NL pool queries and report generation share the same auditable path.

### 7. Top 10 evidence-backed gaps (observed → insufficiency, not feature pitch)

1. End-to-end provenance ledger connecting JD→requirement→candidate evidence→interview question→note→report→query in one exportable trail.
2. Per-requirement graded evidence (supporting/neutral/conflicting/missing) instead of whole-candidate opaque rank.
3. Uncertainty taxonomy (unanswered vs conflicting vs unverifiable vs stale) that is vocabulary for evaluators, not binary present/missing.
4. Candidate-gap-conditioned question generation and follow-ups gated on prior answers (vs generic kits).
5. NL pool querying with citations — same provenance path as reports, not a separate filter.
6. Measured human-in-loop (override logs, competence/time evidence) vs claimed.
7. Per-model/version bias monitoring that survives swaps/upgrades (bias reverses on model change).
8. Anti-gaming at screening time (honeypot/phantom detection + anomaly flag) against prompt-injection via resumes.
9. State that re-evaluates only affected requirements when new evidence arrives (append-only + selective re-rank with version diff).
10. Evidence-shaped grouping (e.g., "strong on X but missing Y, n=12") for batch follow-up vs mere pipeline stages.

### 8. Top 10 unresolved questions we should discuss before building

1. Jurisdiction posture — global strict mode vs EU/UK/US/India toggle; affects ADM defaults and retention.
2. Approval gating map — which writes (rank, question, summary, report, message) require explicit human approval vs audited pre-approve vs read-only.
3. Evidence consent scope — which sources are legitimate interest vs require granular consent, and how retention clocks differ by jurisdiction.
4. Requirement uncertainty representation — binary vs graded vocabulary and how it weights confidence.
5. Retrieval granularity for trustworthy citations — sentence vs paragraph chunks given provenance vs context trade-off.
6. LLM vs deterministic split — per-dimension LLM with Python composite vs LLM-ranking end-to-end.
7. Grouping definition — pipeline buckets vs evidence-shaped cohorts.
8. Agent topology — single loop vs small multi-agent (planner/matcher/questioner/assessor/bias) and cost/failure evidence per choice.
9. AI disclosure surface — pre-apply vs pre-interview vs report badge, and per-decision explanation default.
10. Minimal auditable artifact — exact fields and export (JSON+PDF with approver/version log) that satisfy the brief and regulator expectations in miniature.

> All counts, patterns, gaps, and questions above are **research findings**, not product recommendations. The decision of what to build — and what to deliberately not build in 48 hours — rests with the product/engineering owner using this evidence.

---

## Addendum 2026-09-19 — System One Models (Jev) & Sales-Conversion RL

*This addendum was added after the initial 2026-09-19 sweep in response to three new sources supplied for evaluation. It does not replace §§2-8; it extends them. All vendor claims flagged as **marketing claim** unless independently measured.*

### A. System One Model — Jev (TypeSafe AI)

**What it is:** Jev (`jev-latest`, reported `jev-1.13.0`) is *not* a generative LLM. It is the first public **System One model** from [TypeSafe AI — Introducing System One Models & Jev (15 Sep 2026)](https://typesafe.ai/blog/introducing-system-one-models-and-jev), trained with **RLCD (Reinforcement Learning for Calibrated Decisions)** vs RLHF/RLVR for LLMs. Training founder: Diogo Almeida (ex-OpenAI, ChatGPT RLHF). Inputs = unstructured `state` (text or structured `state` object / LangChain messages); outputs = **typed, parallel, calibrated decisions only** — `Noul` (yes/no → `p(yes)`), `Choice` (closed set → distribution + `choice` + `confidence`), `Score` (ordered levels → continuous `score` + distribution + `confidence`). Never generates strings, never type-errors by construction, output tokens are **FREE** (too cheap to meter).

**Why it is a harness primitive:** Documented in [LangChain — Building a Harness with Jev (17 Sep 2026)](https://www.langchain.com/blog/building-a-harness-with-jev) and [TypeSafe Quickstart](https://docs.typesafe.ai/introduction/quickstart): `state + {questions}` → one `POST https://api.typesafe.ai/v1/systemone` call. **All questions evaluated in parallel** — adding questions barely changes latency, costs only extra input tokens. This is how *one* `jev-latest` model can be reused across every HireFlow stage by changing the `questions` map, not weights.

**Measured claims (vendor, from TypeSafe evals site [evals.typesafe.ai](https://evals.typesafe.ai/)):**

* **193.6× faster, 444.6× cheaper** vs LLM baseline on 4 workflow evals (same workflow, reference = avg of GPT-6 Astra + Fable 5.1). Home page generalizes as `~200× faster, 400× cheaper on classification tasks`. Nuance disclosed: eval queries simplified/detailed dense paragraph, service hosted on West Coast, `System One LLM wrapper` used for LLM baselines (slower), input-only pricing at `$42 / 1B input tokens` (output free) vs `$0.20-10/MTok` + ~5× output for LLMs. Expect high end of real-world gains.
* **Latency:** `70-500ms` end-to-end vs `3-329s` for frontier reasoning models per vendor benchmarking.
* **No hallucinated type errors:** `0%` by construction vs measured LLM error rates via OpenRouter (bias noted).
* **Calibrated confidence:** higher confidence → higher accuracy; consistent across similar inputs — enables code-level `if 0.35 < p < 0.65 → needs review` instead of trusting prose (see concrete CV-screen threshold below).

**Concrete proof point — CV screening workbench:** Open-source repo [gtaras7/typesafe-jev — cv-screen](https://github.com/gtaras7/typesafe-jev/tree/main) / [cv-screen/README.md](https://github.com/gtaras7/typesafe-jev/blob/main/cv-screen/README.md) (MIT, Node 22 + SQLite, `127.0.0.1` only, key server-only, `CV_SCREEN_API_TOKEN` + `SCAN_ROOT` containment). Pattern:

1. One Jev call per CV, all questions batched (yes/no | Choice | Score) → distributions + confidence.
2. `src/compose.ts` does arithmetic (weighted match, gates/caps, verdicts `ready | maybe | pass` + `needs review` flag, strengths/gaps sentence) — prose never parsed.
3. **Policy as data** (`src/policy.ts`): weights, caps, thresholds, accepted degrees, age/military/sector rules, extra fields; `src/recompose.ts` re-scores all stored candidates **in ~20ms, 0 tokens** because judgments stay on disk; only a new question costs tokens, only for CVs missing it.

**Measured on 40 synthetic CVs (food-industry role, concurrency 8):** `3.1s` total, **783 CV/min**, median `338ms` (p95 `930ms`), `146,252` tokens, **$0.0061** folder → **$0.00015 / CV**, extrapolated 300 CVs `~23s, ~$0.046`; re-scoring after policy change `0 tokens`. Frontend 15-demo second run shows adding *one* sector question (`frontend with React`, weight 0.3) lifted bucket agreement `6/15 → 9/15` and correctly capped 3 backend candidates at `0.55` (`needs review`) — no weight tune could have done it without the question. Repo honest caveats: corpus synthetic, bucket names are author intent, thresholds never tuned on real hiring, eval = 4 CVs only. Repo tests: `npm test` 63 tests, no network, locking caps/gates/three-zone logic.

**Harness integration (LangChain):** `langchain-typesafe` → `TypeSafeClassifier.invoke(state, {question: Noul|Choice|Score})` → typed response. Two production middleware already shipped: `ModelRouterMiddleware` (Jev picks `fast` vs `powerful` LLM per request by criteria you define) and `AutoModeMiddleware` (Jev gates risky `tools=["bash"]` calls before execution) — patterns documented as trust layer for any agent.

**Where one Jev model slots across HireFlow (reusing `jev-latest`):** JD linting → resume skill/exp extraction (reuse `fields.ts` library: `hands_on 0-5`, `career progression 4 options`, etc.) → per-requirement mapping (missing/unclear is a `Noul 0.35-0.65` band → `needs review`) → candidate-specific interview QG (question only if unanswered + high weight) → interview-note contradiction flag → evaluation `unanswered areas` highlight → NL pool query filter (query text as `state`) → audit artifact (per-question distribution + confidence + policy hash + version). Demo differentiator: edit policy in UI → instant 0-token re-score vs re-paying LLM for every candidate.

### B. Sales-Conversion RL — `DeepMostInnovations/sales-conversion-model-reinf-learning` (HF)

Source: [Hugging Face — sales-conversion-model-reinf-learning](https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning) (142 dl/mo, MIT, `stable-baselines3` PPO), paper [arXiv:2503.23303 SalesRLAgent](https://arxiv.org/abs/2503.23303) (30 Mar 2025), dataset [saas-sales-conversations](https://huggingface.co/datasets/DeepMostInnovations/saas-sales-conversations). Model: `BAAI/bge-m3` 1024-dim embeddings + LLM dynamic metrics (`customer_engagement`, `sales_effectiveness` via `unsloth/Qwen3-4B-GGUF` / Llama) → continuous `0-1` conversion probability **turn-by-turn** (`status 🟢≥70 | 🟡≥50 | 🟠≥30 | 🔴<30`), `85ms` vs `3450ms` GPT-4, claimed `96.7%` accuracy / `+34.7%` over LLM-only / `+43.2%` conversion when used by reps — on **100k+ synthetic conversations** (not independently verified). Use cases are A/B script testing, `matplotlib` trajectory visualization, real-time coaching (`if engagement<0.5 → suggest open-ended question`).

**Relevance to HireFlow:** Not a drop-in hiring model — domain is *sales*, training is *synthetic* — but the **PPO turn-by-turn trajectory idea transfers** to interview intelligence: model interview dialogue evolution per turn (`interview_progression` delta) rather than only static screening score. Treat as architectural reference; if used, train a small HireFlow interview-trace variant on actual interview turns, don't reuse sales weights.

### C. Should HireFlow use Jev? — Decision frame for §§16-18

**Conditional YES as classifier/verification layer, NOT LLM replacement** (Jev cannot generate text). Recommended shape: **LLM for generation/reasoning/synthesis + Jev for judgment/routing/gating/verification inside the loop** — exactly the harness pattern LangChain documents.

| Decision | Rationale |
|---|---|
| **Adopt Jev for screening harness (§§2/11/14 agentic)** | Gives speed+cost envelope impossible with LLM-only: `~$0.00015/CV`, `~783 CV/min`, `20ms` free re-score — aligns with gap #1/#2/#3 (provenance, per-requirement evidence, uncertainty as `0.35-0.65` band). TypeSafe policy-code separation directly implements §§6 reusable idea #2/#4 (evidence-typed, deterministic wrapper). |
| **Keep LLM for §§7/11 RAG + reports** | Jev *gives up string generation* by design — cannot write interview questions prose, note summaries, or evaluation reports alone. Pair: Jev judgments → code composes score → LLM drafts narrative conditioned *only* on judged evidence (refuse if missing). |
| **Treat sales RL as reference, not dependency** | Conceptually strong for interview turn analysis, but synthetic sales domain creates bias risk (§12 prompt-injection / §5.6 per-model calibration lessons apply). Use pattern, not weights. |

**Risks to price into §§8/12/17 before committing (all flagged in sources themselves):**

* **Early-access vendor risk:** TypeSafe waitlist-gated 15 Sep 2026, pricing sustainability unproven (`we can’t prove it isn’t subsidized`), US West Coast hosting → GDPR Art.28 processor terms not yet independently reviewed → mitigate by isolating behind `Classifier` interface with fallback to LLM structured-output adapter (`System One LLM wrapper`).
* **Single-provider + limits:** `Choice` cardinality `≤255` (higher uses 2-stage score→choice, slower); for ESCO 13,485 require hierarchical scoring in policy code, not direct 13k choice.
* **Calibration domain shift:** Workflow eval reference = avg of Astra/Fable (bias toward OpenAI/Anthropic), CV thresholds `0.75/0.50` never tuned on real hiring, demo `6/15 → 9/15` buckets are author intent not accuracy — must run HireFlow-owned eval on synthetic folder and report `needs-review` rate, not accuracy.
* **Bias/fairness gap:** No published NYC LL144 / EU high-risk audit for Jev yet; `military rule / age rule` is in policy code (good) but no systematic disparate-impact test shown → run Wilson 2024 name-perturbation probe via Jev before any auto-reject.
* **Sales RL accuracy realism:** `96.7%` on synthetic does not transfer to hiring; do not quote for HireFlow without real interview-trajectory data.
* **Regulatory exposure:** Typed probabilities help explainability (EU AI Act Art.13/14 human oversight, §8 checklist) but RLCD training data provenance (`training data: where does it come from?` listed as open FAQ) still needed for Art.10 data governance.

**48h placement if you proceed:** Fork `typesafe-jev/cv-screen` policy patterns (`policy.ts → questions.ts → compose.ts → recompose.ts`) as a new `CapabilityExecutor` capability; add `langchain-typesafe` optional `SourceAdapter` feature-flagged on `TYPESAFE_API_KEY`; keep `RunStore` as append-only ledger but now judgments store `{question_id, distribution, confidence, policy_hash}`; add `ModelRouterMiddleware` + `AutoModeMiddleware` as safety/cost gates; demo with synthetic folder showing *instant* 0-token re-score after policy edit — the visible contrast to LLM-only.

### D. Updated source accounting (addendum)

*This addendum adds 5 Tier-1/2 sources to the 120+ in §8/App E (now ~125+). Tier-1: [TypeSafe blog 15 Sep 2026](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [TypeSafe Quickstart/docs](https://docs.typesafe.ai/introduction/quickstart), [TypeSafe evals](https://evals.typesafe.ai/), [typesafe-jev repo + cv-screen README](https://github.com/gtaras7/typesafe-jev/tree/main) + [cv-screen detail](https://github.com/gtaras7/typesafe-jev/blob/main/cv-screen/README.md). Tier-2: [LangChain harness 17 Sep 2026](https://www.langchain.com/blog/building-a-harness-with-jev), [HF sales-conversion-model](https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning) + [SalesRLAgent arXiv:2503.23303](https://arxiv.org/abs/2503.23303). Recency: all Sep 2025–Sep 2026 — current for §§7/11/14 tooling.*

*Research refresh:* 2026-09-19 • *Maintainer:* HireFlow research scouting — whitespace before direction. If a claim lacks a URL, use the App-indexed source: paper title → arXiv search; product title → official help/product page; repo name → GitHub exact match. Do not manufacture citations.
