# SUH-10 — RAG Grounding: Inject Help Center Context into LLM Prompt

**Linear:** SUH-10 / CAP-3.S-2
**Overall Progress:** `95%`

## TLDR

Wire `retrieval.py` into `main.py`: call `retrieve()` before every Groq request, format the top chunks into a `### CONTEXT ###` block, and instruct the LLM to answer only from that context. Chunks with distance ≥ 1.0 are too dissimilar to be useful and trigger a graceful fallback instead. This is what turns the generic Groq LLM into a Pura-specific support agent.

## Critical Decisions

- **Distance threshold of 1.0 to filter irrelevant results** — SUH-7 showed on-topic queries return distances ~0.5–0.8; off-topic returns ~1.17. Filtering at ≥ 1.0 prevents injecting noise for unrelated queries without requiring a separate relevance classifier
- **Context embedded in the system message** — cleaner than a separate context message; keeps the conversation structure as `[system, user]`, consistent with the current `main.py` shape
- **`build_system_prompt(chunks)` helper** — isolates prompt construction so it's easy to extend when CAP-3.S-3 adds conversation memory to the same messages list

---

## Tasks

- [x] ✅ **Step 1: Update `backend/main.py` to retrieve and inject context**
  - [x] ✅ Import `retrieve` from `retrieval.py` at the top of `main.py`
  - [x] ✅ Add `build_system_prompt(chunks: list[dict]) -> str` helper with context block and fallback
  - [x] ✅ In `stream_groq_response(message)`: call `retrieve()`, filter by `distance < 1.0`, build prompt
  - [x] ✅ Remove the now-unused static `SYSTEM_PROMPT` constant

- [x] ✅ **Step 2: Validate grounding against 10 test queries**
  - [x] ✅ All 10 queries return answers grounded in KB content — **10/10** (gate: ≥8/10) ✅
  - [x] ✅ Spot-check: "What is the battery life of the Pura Car Pro?" → `"approximately 15 hours per full charge"` (exact `pura-car-pro-faq.md` value) ✅
  - [x] ✅ All responses cite product-specific steps, specs, and procedures — no generic hallucination observed

- [x] ✅ **Step 3: Verify fallback and off-topic behaviour**
  - [x] ✅ "How do I cancel my Pura subscription?" → RAG found `fragrance-subscription.md` and answered correctly (cancellation steps cited accurately — KB coverage better than expected)
  - [x] ✅ "What is the capital of France?" → `"I'm here to help with Pura products only."` ✅
  - [ ] 🟥 Visual browser test: open `http://localhost:5173`, send a Pura question, confirm grounded streaming response
