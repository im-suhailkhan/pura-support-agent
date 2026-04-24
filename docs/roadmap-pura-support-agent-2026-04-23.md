# Roadmap: Pura Customer Support AI Agent
**Solution:** In-app conversational AI agent (LLM + RAG) on pura.com covering all 13 core support topics
**PRD:** [docs/pura-light-prd.md](pura-light-prd.md)
**Date:** 2026-04-23
**Author:** Suhail (PM)
**Status:** Draft — pending approval

> **Scope clarification:** The PRD described a "mobile-first in-app widget." The MVP is scoped to the **pura.com website only**. Mobile (iOS/Android) is post-MVP.

---

## North Star Metric
**Ticket Deflection Rate — 50–70% reduction in support tickets for the 13 covered topics within 90 days of launch.**

---

## Step 1 — Outcome Decomposition

```
Core job:        A customer stuck on setup, troubleshooting, or an account question
                 visits pura.com, gets an instant accurate answer in one conversation,
                 and never opens a support ticket.

Table stakes:    Coverage of all 13 core topics · escalation path to a human with
                 full transcript · accurate RAG on existing Help Center content ·
                 brand-consistent tone · auth wall on all account/order flows

Differentiators: Context-aware (agent knows your order + subscription if logged in) ·
                 step-by-step troubleshooting wizards with image links ·
                 RAG auto-synced when Help Center is updated

Delighters:      CS analytics dashboard revealing failure modes + product insights ·
                 warm "scent-obsessed" premium voice that feels like a Pura brand
                 interaction, not a generic bot
```

Phases map to these layers in order. Core job ships in Phase 1. Delighters ship in Phase 3.

---

## Step 2 — Assumption Sequencing

**Already validated (per PRD — skip testing):**
- Support volume is high and dominated by repetitive queries (from ticket data)
- Customers expect instant 24/7 help (from user interviews)
- 60–80% of query volume is automatable (from CS team analysis)

**Open / unvalidated — assigned to phases:**

| # | Assumption | Phase to test | Evidence needed |
|---|---|---|---|
| A1 | Existing Help Center content is accurate + structured enough to power ≥80% RAG accuracy without major cleanup | Phase 1 | ≥70% of informational/troubleshooting convos resolved in beta without escalation |
| A2 | Website visitors will discover and engage with the chat widget at meaningful rate | Phase 1 | Widget engagement ≥20% of support-intent page visitors in beta |
| A3 | Shopify/backend API exposes order + subscription data in a form the agent can consume securely within scope | Phase 2 | All 5 transactional flows complete end-to-end in QA with ≥95% data accuracy |
| A4 | Combined resolution rate (informational + transactional) reaches ≥85% at full coverage | Phase 3 | ≥85% resolution rate over 2-week production window before Phase 3 closes |

**Gate rule:** No phase begins if its founding assumption is unvalidated by the previous phase gate.

---

## Step 3 — Phase Definitions

---

### Phase 1 — Know & Guide
*(Informational + Troubleshooting · No Auth)*

**Theme:** Prove the agent can answer product, setup, and troubleshooting questions accurately enough that real users trust it and don't escalate.

**Duration:** 4–6 weeks

**Team needed:**
- Backend / AI engineer: 80%
- Frontend engineer: 60%
- Content / knowledge specialist: 40% (RAG content QA)
- PM: 20%

**Outcome goal:**
A first-time Pura customer who gets stuck during setup visits pura.com, opens the chat widget, gets a step-by-step guided answer in under 2 minutes, and does not open a support ticket or call in.

**What's in:**
- [ ] User can open a chat widget on pura.com and type a question in natural language
- [ ] Agent covers all 6 product lines (Pura 4™, Plus™, Mini™, 3™, Car Pro™, Car™) — product info and specs
- [ ] Agent provides step-by-step Diffuser Setup guidance for all 6 models
- [ ] Agent answers top 20 FAQ & Guides articles via RAG
- [ ] Agent guides users through top 5 troubleshooting issues as decision-tree wizards (with image links)
- [ ] Agent detects when it cannot answer and offers to escalate — pre-filling a support ticket with conversation context
- [ ] RAG knowledge base ingested from Help Center export (first sync manual; subsequent syncs automatic on article publish)
- [ ] Basic conversation logging for QA and Phase 2 input (no dashboard yet)

**What's explicitly out:**
- Order status and shipping lookups (requires auth — Phase 2)
- Subscription management of any kind (Phase 2)
- Account information flows (Phase 2)
- Analytics / CS dashboard (Phase 3)
- Mobile app — iOS or Android (post-MVP)
- Multi-language support (post-MVP)

**Assumption being tested:**
A1 — Existing Help Center content is accurate and structured well enough to power ≥80% RAG accuracy on informational and troubleshooting queries without a content cleanup sprint.

**Phase gate (go/no-go):**
- ≥70% of informational and troubleshooting conversations in beta resolved without human escalation
- Widget engagement ≥20% of support-intent page visitors (proxy for ≥40% eventual adoption target)
- Zero critical accuracy failures (dangerous or wrong advice on setup steps) in QA sign-off
- Response time <2s at P95 in staging load test

**Risk:**
Help Center content is too thin, outdated, or poorly structured for RAG to perform accurately — requiring a content cleanup sprint that delays Phase 2. Mitigate by auditing the top 20 articles in Week 1 before committing to the 4-week estimate.

---

### Phase 2 — Serve & Transact
*(Authenticated Flows · Shopify Integration · Account + Order Actions)*

**Theme:** Add real-time order and account context so customers can resolve transactional questions — and take safe actions — without a human.

**Duration:** 5–7 weeks

**Team needed:**
- Backend / AI engineer: 80%
- Frontend engineer: 50%
- Integration engineer: 80% (API surface is the primary risk)
- PM: 20%

**Outcome goal:**
A logged-in Pura subscriber who wants to check their order status or skip a shipment can do it entirely within the chat widget on pura.com in under 3 minutes — without opening a ticket, emailing, or calling.

**What's in:**
- [ ] User can authenticate within (or alongside) the chat widget via Pura account login
- [ ] Agent reads and displays real-time order status and shipping info (Shopify integration)
- [ ] Agent reads and displays subscription details: current plan, next shipment date, pod selection
- [ ] Agent executes safe write actions: skip shipment, update payment method, update shipping address
- [ ] Agent hands off to live human agent with full conversation transcript attached (for out-of-scope actions)
- [ ] Conversation history persisted across sessions for logged-in users
- [ ] All Phase 1 capabilities remain live and stable throughout

**What's explicitly out:**
- Subscription cancellation — human-only (per PRD non-goals; too high-stakes for V1)
- Proactive / outbound messages (e.g., "your shipment is in 3 days") — requires event pipeline not in scope
- Photo or video upload for troubleshooting (post-MVP)
- Analytics / CS dashboard (Phase 3)
- Mobile app (post-MVP)

**Assumption being tested:**
A3 — Shopify (or the existing backend) exposes order and subscription data via API in a form the agent can consume securely, and users trust the agent enough to complete transactional actions through it rather than preferring to call or email.

**Phase gate (go/no-go):**
- All 5 transactional flows complete end-to-end with ≥95% data accuracy in QA (order status, skip shipment, update payment, update address, subscription view)
- ≥65% of transactional conversations in beta resolved without escalation
- CSAT for transactional flows ≥4.0/5 (users trust the agent with their account data)
- Security review passed — no data exposure or auth bypass issues
- Response time <2s at P95 under load including API calls

**Risk:**
API integration surface is larger than estimated — auth complexity, rate limits, schema mismatches, or missing endpoints are the most common cause of phase overruns on products like this. Spike Shopify API readiness in Week 1 of Phase 2 before locking the timeline.

---

### Phase 3 — Measure & Refine
*(Analytics · CS Dashboard · North Star Validation)*

**Theme:** Give the CS team full visibility into what the agent is doing and where it fails, then measure whether the north star has been hit.

**Duration:** 3–4 weeks

**Team needed:**
- Backend / AI engineer: 40%
- Frontend engineer: 30%
- PM: 30%
- CS team lead: 20% (calibration partner — required, not optional)

**Outcome goal:**
The CS team can see what the agent handles, where it drops, and why — and Pura can report ticket deflection rate vs. the 50–70% target with a defensible methodology.

**What's in:**
- [ ] CS analytics dashboard: top queries, resolution rate per topic, escalation triggers, CSAT by topic
- [ ] Weekly RAG refinement workflow: CS team flags bad answers → content updated → RAG re-synced
- [ ] Post-chat CSAT survey (1-click, in-widget, shown after resolution)
- [ ] Ticket deflection measurement: pre/post comparison integrated with support ticketing system (Zendesk / Gorgias)
- [ ] Escalation quality: agent produces a structured summary before handing off to live agent
- [ ] Load and latency validation at production traffic peak (P95 response <2s, full resolution <3 min)

**What's explicitly out:**
- New topic coverage beyond the 13 MVP topics (add post-launch based on dashboard data)
- Multi-language support (post-MVP)
- Voice interface (post-MVP)
- Mobile app (post-MVP)
- Proactive notifications (post-MVP)

**Assumption being tested:**
A4 — At full coverage (informational + transactional), the combined resolution rate hits ≥85% and ticket deflection reaches ≥50% within the 90-day window — validating the north star.

**Phase gate (go/no-go):**
- Ticket deflection ≥40% measured over a 2-week production window (leading indicator for 90-day ≥50% target)
- CSAT ≥4.3/5 across all topics in production
- CS team formally signs off on analytics dashboard as operationally useful
- P95 response time <2s under production peak load
- Deflection measurement methodology validated by CS lead (intent-to-contact users separated from browse traffic)

**Risk:**
Deflection numbers may be overstated if measurement counts low-intent visitors (people who typed a question but were never going to open a ticket). Deflection must be measured against users who reach a support-intent page (Help Center, Contact Us) — not all pura.com traffic.

---

## Step 4 — Dependency Map

| Phase | Depends on | External dependency | Decision needed before start |
|---|---|---|---|
| Phase 1 | — | Help Center content export / CMS API access | Widget placement on pura.com approved by web team; LLM provider selected |
| Phase 2 | Phase 1 RAG pipeline stable; Phase 1 gate passed | Shopify API credentials + docs; backend API documentation | Auth strategy decided (native SSO vs. dedicated widget login flow) |
| Phase 3 | Phase 2 API integrations live in production; Phase 2 gate passed | Ticketing system API (Zendesk / Gorgias) for deflection measurement | CS team lead committed to calibration sessions; measurement methodology agreed with CS leadership |

---

## Step 5 — Anti-Roadmap

- **Mobile app (iOS/Android):** Descoped from MVP per PM decision. Website widget must prove ticket deflection and CSAT before committing to native app development. Re-evaluate after Phase 3 gate.
- **Voice interface:** Out of scope per PRD Section 3. No architectural foundation for voice in this stack; adds ASR/TTS cost and latency complexity that isn't justified until text resolution is proven.
- **Subscription cancellation via agent:** Kept as human-only. Retention conversations require judgment, empathy, and potential offers — automating cancellation in V1 is high-risk and could accelerate churn.
- **Proactive / outbound messaging:** Requires an event-driven notification pipeline that doesn't exist. Risk of spam perception outweighs the benefit until the reactive experience is validated.
- **Multi-language support:** Deferred. English-first Help Center content is sufficient to validate the core concept. Adding languages multiplies RAG QA surface area and content maintenance cost before value is proven.

---

## Step 6 — Metrics Ladder

*All metrics sourced from PRD Section 4. No new metrics introduced.*

| Phase | Leading indicator | Lagging indicator | Phase-specific threshold |
|---|---|---|---|
| Phase 1 | Widget engagement rate (% of support-intent visitors sending ≥1 message) | Informational resolution rate (no escalation) | Engagement ≥20%; Resolution ≥70% on informational + troubleshooting topics |
| Phase 2 | Transactional completion rate (user executes action end-to-end) | CSAT for transactional flows | Completion ≥80% of attempted transactional actions; CSAT ≥4.0/5 |
| Phase 3 | Ticket deflection rate (2-week production window) | CSAT ≥4.5/5; 90-day deflection at or above target | Deflection ≥40% in 2-week window (on track for ≥50–70% at 90 days); adoption ≥40% of support-intent users |

**North star: Ticket Deflection Rate — 50–70% reduction in support tickets for the 13 covered topics within 90 days of launch.**

**Anti-metrics (must not worsen — inferred from PRD problem statement; not explicitly listed in PRD):**
- Subscription cancellation rate — agent friction must not drive churn
- Average resolution time for escalated tickets — handoff must not slow human agents down
- Product return rate — inaccurate troubleshooting advice must not increase returns

---

## CLAUDE.md Update Block
```
Active PRD:     @docs/pura-light-prd.md
Active roadmap: @docs/roadmap-pura-support-agent-2026-04-23.md
Current phase:  Phase 1 — Know & Guide
Phase gate:     ≥70% informational resolution in beta; widget engagement ≥20%; zero critical accuracy failures; P95 <2s
North star:     Ticket Deflection Rate — 50–70% reduction in support tickets (13 topics) within 90 days of launch
```
