# Phase 1 — Know & Guide : Delivery Plan

**Type:**      Phase breakdown
**Roadmap:**   @docs/roadmap-pura-support-agent-2026-04-23.md
**PRD:**       @docs/pura-light-prd.md
**Status:**    Planning
**Last updated:** 2026-04-23

---

## Brief

```
Phase 1 — Know & Guide
Goal:     A first-time Pura customer types a setup or troubleshooting
          question into the chat widget and gets an accurate, guided
          answer in under 2 minutes — without opening a support ticket.
Gate:     ≥70% of conversations resolved without escalation in beta;
          zero critical accuracy failures in QA; P95 <2s
Duration: Not time-boxed (vibe coding pace)
Scope:    Full phase — informational + troubleshooting only, no auth
```

---

## Stack

See @docs/architecture.md for full rationale.

| Layer | Choice |
|---|---|
| Frontend | React + Vite |
| Styling | Tailwind CSS |
| Backend | FastAPI (Python) |
| LLM | Groq API — Llama 3.3 70B (free tier) |
| Embeddings | sentence-transformers / bge-small-en-v1.5 (local) |
| Vector Store | ChromaDB (local) |
| Database | SQLite (local) |
| RAG Framework | LlamaIndex |
| Testing | Pytest + Vitest |

---

## Capabilities and Stories

### Capability 1: RAG Knowledge Base

**[CAP-1.S-1] "Help Center content can be ingested into the vector store"**

As a content specialist,
I want to run a single script that loads Help Center articles, chunks them,
and stores embeddings in ChromaDB,
So that the agent has a searchable knowledge base.

Done when:
- [ ] Script accepts a folder of markdown/text files as input
- [ ] Documents are chunked (512 tokens, 50-token overlap)
- [ ] Each chunk is embedded using bge-small-en-v1.5 (local)
- [ ] Chunks stored in ChromaDB with metadata: article title + source filename
- [ ] Script prints summary on completion: X articles, Y chunks stored
- [ ] Re-running the script updates existing chunks without duplicating

Depends on: none
Effort: M (1–2d)
Priority: must-have

---

**[CAP-1.S-2] "Agent retrieves the most relevant Help Center chunks for a query"**

As Sarah (user),
I want the agent to find the right Help Center content when I ask a question,
So that its answers are grounded in Pura's actual documentation.

Done when:
- [ ] Given a natural language query, retrieval returns top-3 relevant chunks
- [ ] Tested against 10 sample queries across all 6 product lines
- [ ] ≥7/10 queries return a relevant chunk in top-3 results
- [ ] Retrieval latency <500ms on local hardware
- [ ] Returns empty result gracefully (no crash) when nothing relevant exists

Depends on: CAP-1.S-1
Effort: S (4–8h)
Priority: must-have

---

### Capability 2: Chat Widget UI

**[CAP-2.S-1] "User can open the chat widget and see the input interface"**

As Sarah (user),
I want to open a chat panel on the page,
So that I have a place to type my support question.

Done when:
- [ ] Chat panel renders on page load (no toggle needed for dummy UI)
- [ ] Panel shows: message history area, text input field, send button
- [ ] Input field is focused by default
- [ ] Empty state shows a welcome message: e.g. "Hi! Ask me anything about your Pura."
- [ ] UI is readable on a standard desktop browser window (1280px wide)

Depends on: none
Effort: S (4–8h)
Priority: must-have

---

**[CAP-2.S-2] "User can send a message and see the agent's response stream in real time"**

As Sarah (user),
I want to see the agent's reply appear word-by-word as it's generated,
So that the experience feels fast and responsive even before the answer is complete.

Done when:
- [ ] Pressing Enter or clicking Send submits the message
- [ ] User message appears immediately in the chat history
- [ ] Agent response streams token-by-token (not rendered all at once)
- [ ] Input is disabled while response is streaming; re-enabled on completion
- [ ] Conversation history scrolls to latest message automatically
- [ ] If backend returns an error, chat shows: "Something went wrong. Please try again."

Depends on: CAP-2.S-1
Effort: M (1–2d)
Priority: must-have

---

### Capability 3: LLM + RAG Pipeline

**[CAP-3.S-1] "User message reaches the backend and receives a streamed LLM response"**

As Sarah (user),
I want my typed question to be sent to the backend and get a response,
So that the chat widget is connected end-to-end.

Done when:
- [ ] FastAPI server runs locally with a POST /chat endpoint
- [ ] Frontend sends user message to /chat and receives a streaming response
- [ ] Response streams correctly from Groq (Llama 3.3 70B) to the UI
- [ ] Groq API key loaded from .env — never hardcoded
- [ ] Endpoint returns a clean error message if Groq API is unavailable

Depends on: CAP-2.S-2
Effort: M (1–2d)
Priority: must-have

---

**[CAP-3.S-2] "Agent answers Pura support questions using retrieved Help Center content"**

As Sarah (user),
I want the agent to answer using Pura's actual documentation,
So that responses are accurate and not hallucinated.

Done when:
- [ ] /chat endpoint retrieves top-3 relevant chunks from ChromaDB before calling Groq
- [ ] Retrieved chunks are injected into the system prompt as context
- [ ] Agent answers only using the provided context — falls back to "I don't have that
      information" when context is insufficient (no hallucination)
- [ ] Agent maintains Pura's warm, premium tone ("Let's get that sorted for you!")
- [ ] Agent refuses off-topic questions ("I'm here to help with Pura products only")
- [ ] Tested against 10 sample queries — ≥8/10 responses are accurate and grounded

Depends on: CAP-3.S-1, CAP-1.S-2
Effort: L (2–3d)
Priority: must-have

---

**[CAP-3.S-3] "Agent remembers earlier messages within the same conversation"**

As Sarah (user),
I want to ask follow-up questions without repeating myself,
So that the conversation feels natural and continuous.

Done when:
- [ ] Last N turns (configurable, default 6) included in Groq API call context
- [ ] Follow-up questions ("What about the Mini?") resolve correctly using prior context
- [ ] Conversation history does not exceed Groq's context window limit
- [ ] Tested with a 5-turn conversation covering a realistic support scenario

Depends on: CAP-3.S-1
Effort: S (4–8h)
Priority: must-have

---

### Capability 4: Troubleshooting Wizards

**[CAP-4.S-1] "Agent recognises a troubleshooting scenario and switches to guided mode"**

As Sarah (user),
I want the agent to detect when I have a device problem,
So that I get a structured guided flow instead of a flat text answer.

Done when:
- [ ] Agent detects troubleshooting intent from natural language
      (e.g. "won't connect", "not working", "blinking light")
- [ ] On detection, agent responds with a clarifying question to identify
      which of the top 5 issues applies before giving steps
- [ ] Covers all 6 product lines — agent asks "Which Pura model do you have?"
      if not already stated
- [ ] Tested with 5 different phrasings per issue — intent detected correctly ≥4/5

Depends on: CAP-3.S-2
Effort: M (1–2d)
Priority: must-have

---

**[CAP-4.S-3] "Troubleshooting steps include image links where relevant"**

As Sarah (user),
I want to see image links alongside the steps,
So that I can visually confirm I'm doing the right thing.

Done when:
- [ ] Help Center content includes image URLs in markdown (prerequisite: content prep)
- [ ] Agent surfaces image links inline with the relevant step — not as a separate message
- [ ] Links are validated before ingestion — no broken URLs in the knowledge base
- [ ] Tested on at least 3 setup/troubleshooting flows that have known image assets

Depends on: CAP-4.S-1
Effort: S (4–8h)
Priority: should-have

---

### Capability 5: Escalation Path

**[CAP-5.S-1] "Agent recognises when it cannot resolve a query and offers escalation"**

As Sarah (user),
I want the agent to tell me honestly when it can't help,
So that I'm not left stuck in a loop getting useless answers.

Done when:
- [ ] Agent detects "I don't know" situations: no relevant RAG chunks returned,
      or user explicitly says "that didn't help" / "I want to talk to a person"
- [ ] Agent responds with a clear message: "I wasn't able to resolve this —
      would you like me to connect you with the support team?"
- [ ] Escalation is offered after at most 2 failed attempts to answer the same query
- [ ] Tested against 5 out-of-scope or unanswerable queries

Depends on: CAP-3.S-2
Effort: S (4–8h)
Priority: must-have

---

**[CAP-5.S-2] "User can escalate with their conversation transcript pre-filled"**

As Sarah (user),
I want the support team to already know what I tried,
So that I don't have to repeat everything when I contact a human.

Done when:
- [ ] On escalation, agent displays a summary of the conversation so far
- [ ] Summary is formatted as plain text the user can copy into a support ticket
- [ ] Summary includes: user's original question, steps tried, point of failure
- [ ] Agent provides a link or instruction for reaching the support team
      (placeholder URL acceptable for Phase 1)

Depends on: CAP-5.S-1
Effort: S (4–8h)
Priority: must-have

---

### Capability 6: Conversation Logging

**[CAP-6.S-1] "Every conversation turn is saved to the local database"**

As a content specialist (QA reviewer),
I want every user message and agent response stored automatically,
So that I can review conversations to catch accuracy failures and feed
improvements into Phase 2.

Done when:
- [ ] SQLite DB created on first run if it doesn't exist (no manual setup)
- [ ] Each turn written as a row: session_id, timestamp, role (user/agent), message
- [ ] Session ID persists across turns in the same conversation
- [ ] Logging does not block or slow the streamed response to the user
- [ ] DB file location configurable via .env (default: ./data/conversations.db)

Depends on: CAP-3.S-1
Effort: S (4–8h)
Priority: must-have

---

## Delivery Sequence

```
Block 1 — Foundation (no dependencies, build in parallel if possible)
  [CAP-1.S-1] Help Center content ingested into ChromaDB          (M)
              unblocks: CAP-1.S-2, CAP-3.S-2

  [CAP-2.S-1] Chat widget UI shell renders with input interface    (S)
              unblocks: CAP-2.S-2

Block 2 — Core plumbing
  [CAP-1.S-2] RAG retrieval returns relevant chunks for a query    (S)
              depends on: CAP-1.S-1 | unblocks: CAP-3.S-2

  [CAP-2.S-2] User sends message, streamed response appears        (M)
              depends on: CAP-2.S-1 | unblocks: CAP-3.S-1

Block 3 — Connect everything together
  [CAP-3.S-1] FastAPI endpoint receives message, streams Groq LLM  (M)
              depends on: CAP-2.S-2 | unblocks: CAP-3.S-2, CAP-3.S-3, CAP-6.S-1

  [CAP-6.S-1] Conversation turns saved to SQLite                   (S)
              depends on: CAP-3.S-1 | can be done same session as CAP-3.S-1

  [CAP-3.S-3] Agent remembers earlier turns in conversation        (S)
              depends on: CAP-3.S-1

Block 4 — RAG integration (highest risk story in the phase)
  [CAP-3.S-2] Agent answers using retrieved Help Center content    (L)
              depends on: CAP-3.S-1 + CAP-1.S-2
              unblocks: CAP-4.S-1, CAP-5.S-1

Block 5 — Guided flows + escalation
  [CAP-4.S-1] Agent detects troubleshooting intent, enters         (M)
              guided mode
              depends on: CAP-3.S-2 | unblocks: CAP-4.S-3

  [CAP-5.S-1] Agent detects unresolvable query, offers escalation  (S)
              depends on: CAP-3.S-2 | unblocks: CAP-5.S-2

Block 6 — Polish
  [CAP-5.S-2] Escalation surfaces conversation transcript          (S)
              depends on: CAP-5.S-1

  [CAP-4.S-3] Troubleshooting steps include image links            (S)
              depends on: CAP-4.S-1
```

---

## Cut List (deferred)

No cuts required — scope fits vibe-coding pace comfortably.

**Optional defer if content isn't ready:**
- [CAP-4.S-3] Troubleshooting steps include image links — should-have; depends on Help Center content having image URLs. Phase gate still met without it.

---

## Open Questions

- [x] Content source: real Help Center content — Suhail will provide files directly
- [ ] Which are the exact top 5 troubleshooting issues to cover in CAP-4?
- [ ] Groq free tier rate limit: 6,000 tokens/min — acceptable for local QA testing?
