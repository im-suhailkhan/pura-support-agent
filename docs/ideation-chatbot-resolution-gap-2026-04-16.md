# Ideation: Chatbot Resolution Gap
**Date:** 2026-04-16

---

## Inputs

**User persona:** 30-year-old Pura customer. Digitally native, buys perfume diffusers online, expects frictionless self-service. Has a question or issue (order status, scent compatibility, device troubleshooting, returns) and opens the chatbot expecting resolution — not a referral.

**Pain point:** When I need help with my Pura order or product, I want to get an instant, accurate answer without being redirected to links or told to call/email, so I can resolve my issue and get back to enjoying my purchase without interruption.

**Business context:** Pura is a perfume diffuser e-commerce company. Current chatbot is rule-based: it surfaces help document links and provides phone/email contact info. No conversational AI yet. Goal is to build an AI support agent. No constraints named beyond what the current chatbot does.

---

## Framework 1 — Matchmaking

### 1A. Live Order Context Pull
**Borrowed from:** Airline industry (self-service kiosks + booking lookups)

**How it works in this context:** Airlines let passengers look up bookings by email/name and see real-time status — gate, delay, seat — without talking to anyone. Apply this to Pura: when a customer opens chat, the agent silently authenticates via email (already on file from the order) and pulls their live order data. Answers about shipping, delivery, delays, or replacements are answered with their actual data — not generic "check your email" deflections.

**Why it fits:** The most common support queries for e-commerce are order-status related. Surfacing real data kills the deflection pattern at its root.

---

### 1B. Symptom-to-Solution Triage Engine
**Borrowed from:** Healthcare (symptom checkers like WebMD, NHS 111)

**How it works in this context:** Symptom checkers ask structured follow-up questions ("where does it hurt?", "how long?") to narrow to a diagnosis. Apply to Pura device troubleshooting: the AI asks "What's your diffuser doing? Lights blinking? No scent? App not connecting?" — then routes to a specific, confirmed fix for that exact symptom combination rather than a generic FAQ link.

**Why it fits:** Perfume diffuser issues have a finite symptom tree. The current chatbot sends everyone to the same page. This narrows to a precise answer without a human.

---

### 1C. Return/Exchange Self-Service Flow
**Borrowed from:** Retail (Zappos, Amazon self-service return portals)

**How it works in this context:** Zappos lets you initiate, label, and track a return entirely without human contact. Pura's AI agent could handle the full return/exchange conversation: confirm eligibility, capture the reason, generate a label, and confirm the replacement — all in chat. No "email us at support@pura" handoff.

**Why it fits:** Returns and exchanges are high-friction, high-volume. Deflecting to email adds 24–48hr delay. A self-completing flow removes that gap entirely.

---

### 1D. Scent Recommendation Concierge
**Borrowed from:** Luxury fragrance retail (in-store fragrance consultation at Sephora/Nordstrom)

**How it works in this context:** In-store fragrance staff ask lifestyle questions ("Do you prefer warm or fresh?", "Morning or evening?") to narrow to a recommendation. The AI chat agent does this conversationally — not as a quiz with a submit button, but as a dialogue — and ends with a specific scent recommendation with a direct add-to-cart link.

**Why it fits:** Customers buying refills or new scents are often uncertain. The current chatbot can't engage on preference — it just links to the catalog.

---

## Framework 2 — Reverse Assumptions

### 2A. The customer should initiate contact
**Assumption:** Support starts when the customer messages first.
**Reversal:** Pura reaches out before the customer has to ask.
**Idea: Proactive Order Anomaly Alerts** — When the system detects a shipping delay, failed delivery, or device activation not completed within 48hrs of delivery, the AI agent sends a proactive chat/SMS: "Hey, we noticed your diffuser hasn't been set up yet — need help?" This converts silent frustration into a handled moment.
**Why interesting:** Eliminates the entire category of "where is my order / why isn't this working" tickets because Pura acts before the customer reaches breaking point.

---

### 2B. The chatbot should answer questions
**Assumption:** The chatbot's job is to answer questions.
**Reversal:** The chatbot's job is to complete tasks, not answer questions.
**Idea: Action-First Agent** — Instead of answering "How do I return this?", the agent says "I've started your return. Confirm the item and I'll send the label." The framing shifts from information retrieval to task execution. The customer leaves the chat with something done, not something read.
**Why interesting:** Changes the entire UX contract. Most chatbots are encyclopedias; this one is an operator.

---

### 2C. Support is reactive — it handles problems
**Assumption:** The support channel exists to fix things that went wrong.
**Reversal:** Support is a proactive education channel that prevents problems.
**Idea: Post-Purchase Onboarding Sequence in Chat** — After order delivery, the AI agent initiates a 3-touch drip in chat: Day 1 "Here's how to set up your diffuser in 2 min", Day 3 "Try this scent pairing for your space", Day 7 "How's it going? Any questions?" This surfaces issues early and builds familiarity before frustration.
**Why interesting:** Turns a cost center into a retention driver. Customers who feel guided churn less.

---

### 2D. The chatbot should be always-on text
**Assumption:** Chat support is a text-only, always-available interface.
**Reversal:** Some problems are solved faster with a 60-second video, not text.
**Idea: Embedded Video Resolution Cards** — For troubleshooting steps that are hard to describe in text (device assembly, app pairing, scent pod insertion), the AI agent responds with an inline looping video clip — 15–30 seconds — specific to the exact issue described. Not a YouTube link. An embedded, contextual clip shown inside the chat window.
**Why interesting:** Bridges the gap between "link to a doc" (current state) and a human technician walking you through it. Video completion rate for how-to content is 3–5x higher than article reads.

---

## Framework 3 — Abstraction Laddering

### The Ladder

```
Feel confident and in control of my life and purchases
    ↓
Trust that the brand I chose will take care of me if something goes wrong
    ↓
Get my specific issue resolved quickly without effort or uncertainty
    ↓
Get a direct answer in chat without being redirected elsewhere
    ↓
Understand why my diffuser isn't working and fix it in under 5 minutes
```

---

### 3A. Brand Trust Signal — Rung: "Trust that the brand will take care of me"
The AI agent, after resolving any issue, sends a follow-up: "Done — and we've added a complimentary scent credit to your account for the hassle." No human needed to authorize this. The system auto-triggers a goodwill gesture for resolved complaints above a friction threshold. Customers feel cared for, not processed.

---

### 3B. Effort Elimination Engine — Rung: "Resolve quickly without effort or uncertainty"
Every response the AI gives ends with a binary: "Does this fix it? Yes / No." If No, the agent escalates its own response — tries a different solution path, then offers a live callback slot (scheduled, not a hold queue). The customer never has to re-explain. The conversation thread carries context into the human handoff.

---

### 3C. Intent Prediction Interface — Rung: "Get a direct answer without being redirected"
As the customer types their first message, the AI predicts the intent category in real time (order, troubleshoot, return, recommendation) and pre-loads the most likely resolution before they finish typing. By the time they send, the agent already has the answer ready. Sub-2-second perceived response time, no "let me look that up" delay.

---

### 3D. Guided Fix Wizard — Rung: "Understand why my diffuser isn't working and fix it in 5 minutes"
A structured, step-confirmed troubleshooting flow: the agent presents one action at a time ("Unplug the device. Done?"), waits for confirmation, then advances. Mirrors the UX of guided setup wizards in consumer tech. The customer is never given a wall of instructions — just the next single step. Completion rate for this format is dramatically higher than multi-step FAQ articles.

---

## Framework 4 — Systemic Change

### System Map
**People:** Customer, support agents, fulfillment team, product/QA team
**Processes:** Customer messages → chatbot shows links → customer calls/emails → human agent reads context-free message → researches → replies (24–48hr lag)
**Tools:** Current rule-based chatbot, email/ticketing system, Shopify or similar order management
**Environments:** Customer's home (device issue), mobile browser (chat interface), Pura's support back-office

---

### 4A. System tension: Knowledge is locked in documents, not embedded in the agent
**The current system treats knowledge as static pages the chatbot links to. The customer must read and self-apply — a broken assumption for a physical product with device variance.**

**Proposed shift:** Build a living knowledge graph — not a static FAQ. Every resolved ticket, every product QA note, every firmware update is structured and fed into the agent's retrieval layer. The agent cites current knowledge, not a page last updated in 2023.

**Who/what it affects:** Reduces support ticket volume (customers self-resolve), reduces repeat contacts (knowledge is accurate), feeds back into product team (patterns in unresolved queries surface product gaps).

**Why lasting:** Static docs rot. A knowledge graph that's continuously updated from resolution data compounds in value — the agent gets smarter as Pura's product line grows.

---

### 4B. System tension: The human escalation path destroys context
**When the chatbot fails and the customer emails or calls, all chat context is lost. The human agent starts from scratch. This doubles effort and signals to the customer they're starting over.**

**Proposed shift:** Unified context handoff — the AI agent packages the full conversation, detected intent, attempted resolutions, and customer order data into a structured brief that opens automatically when a human agent picks up the ticket. The human never asks "can you describe the issue again."

**Who/what it affects:** Human agents handle escalations faster (less time re-gathering context). Customer experience feels continuous. CSAT on escalated tickets rises because the human arrives informed.

**Why lasting:** This isn't a feature — it's an architecture decision. Once context flows end-to-end, every future improvement (AI or human) builds on a richer signal.

---

### 4C. System tension: Support is siloed from product feedback loops
**Issues resolved in support never reach the product or QA team in a structured way. The same device bug generates hundreds of tickets before anyone flags it as a pattern.**

**Proposed shift:** The AI agent tags every conversation with a structured taxonomy (device model, symptom, resolution type, resolved Y/N). A weekly digest surfaces to the product team: "347 contacts this week about pod insertion on the Pura 4 — 61% resolved without escalation, 39% needed human." Product acts on signal, not anecdote.

**Who/what it affects:** Reduces future ticket volume by fixing root causes. Creates a feedback flywheel — better products generate fewer support contacts.

**Why lasting:** Transforms support from a cost center into a product intelligence function. Structural, not cosmetic.

---

## Framework 5 — Creative Matrix

### Core User Needs (rows)
1. Get my specific issue resolved without effort
2. Feel like Pura cares about me as a customer
3. Know what to do next with my diffuser / scent

### Unexpected Attributes (columns)
- **Proactive** — acts before I ask
- **Trust-signaling** — builds brand confidence visibly
- **Ritualistic** — becomes part of how I use the product

|  | Proactive | Trust-signaling | Ritualistic |
|---|---|---|---|
| **Issue resolution without effort** | Agent detects failed setup and messages first | Agent confirms resolution and logs it — customer gets a "resolved" receipt | Agent checks in 7 days post-resolution: "Still working well?" |
| **Feel cared for** | Post-delivery "welcome" message with setup nudge | Auto goodwill gesture (credit, free scent) on any friction event | Monthly "Your Pura this month" recap — usage, top scent, next refill due |
| **Know what to do next** | Refill reminder before scent runs out, with order pre-loaded | Agent recommends next scent based on purchase history with confidence signal ("9/10 customers with your profile loved X") | Weekly scent rotation suggestion — turns diffuser use into a considered habit |

---

### Expanded Concepts

**5A. Friction-Triggered Goodwill (Issue resolution × Trust-signaling)**
Any conversation where the AI detects friction — escalation, repeated question, complaint language, unresolved troubleshoot — automatically triggers a goodwill credit to the customer's account. No human approval needed. The agent closes the chat with: "We've added a credit to your account — sorry for the hassle." Turns a bad experience into a brand moment.

**5B. Refill Before Empty (Know what's next × Proactive)**
Based on purchase date and typical scent duration (e.g., Pura pods last ~120hrs of use), the agent proactively messages: "Your [Scent Name] is likely running low — want to reorder? Your last address is saved." One-tap reorder from inside the chat. Removes the friction of the customer realizing mid-week they're out.

**5C. Monthly Ritual Recap (Feel cared for × Ritualistic)**
A monthly chat message: "Here's your Pura this month — you've been running [Scent] for 22 days. Based on what you love, you might enjoy [New Scent] this spring." Not a marketing email. A personal, data-grounded message inside the chat channel the customer already uses for support. Builds the habit of checking in with Pura.

**5D. Post-Resolution Check-In (Issue resolution × Ritualistic)**
Seven days after any resolved support issue, the agent sends a single message: "Hey — just checking the diffuser is still working well after we sorted that last week. Any issues?" This closes the loop, signals genuine care, and catches recurring problems before they become silent churn.

---

## Shortlist — Top 3 Ideas

### #1. Action-First Agent (Framework 2 — Reverse Assumptions)
**The idea:** Shift the chatbot's contract from answering questions to completing tasks. Instead of "here's how to return," the agent says "I've started your return — confirm and I'll send the label."

**What assumption it breaks:** That a chatbot's job is to provide information. This one executes.

**Fastest way to test:** Map the top 5 contact reasons from current support tickets. For each, design the "task completion" version of the response. A/B test against the current link-surfacing response. Measure: did the customer re-contact within 48hrs? (Recontact rate = resolution proxy.)

---

### #2. Symptom-to-Solution Triage Engine (Framework 1 — Matchmaking)
**The idea:** Structured follow-up questions narrow a device complaint to a specific, confirmed fix — not a generic FAQ link. Modeled on healthcare symptom checkers.

**What assumption it breaks:** That all customers with "diffuser issues" need the same support page. Symptom variance means resolution variance.

**Fastest way to test:** Build a decision tree for the top 3 device complaints (no scent, blinking light, app not connecting). Route these in the current chatbot as a structured question flow instead of a link. Measure: did the customer escalate to email/phone after the interaction? Escalation rate = resolution failure signal.

---

### #3. Friction-Triggered Goodwill (Framework 5 — Creative Matrix)
**The idea:** Any detected friction event (escalation, repeat contact, complaint language, unresolved troubleshoot) auto-triggers a small goodwill gesture — credit, free scent sample — visible to the customer before they leave the chat.

**What assumption it breaks:** That goodwill gestures require human judgment and approval. They can be rule-based and automated at the moment of friction.

**Fastest way to test:** Define a friction signal threshold (e.g., conversation > 3 turns with no resolution, or explicit complaint keywords). Manually apply the gesture to a cohort of tickets for 2 weeks. Compare 30-day repurchase rate and CSAT between friction-with-gesture vs friction-without-gesture cohorts.

---

*This file feeds into `/create-plan` to prioritize and sequence the build.*
