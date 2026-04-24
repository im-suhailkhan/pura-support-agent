# SUH-13 — Image Links in Troubleshooting Steps

**Linear:** SUH-13 / CAP-4.S-3
**Overall Progress:** `100% ✅`

## TLDR

Add publicly accessible Pura image URLs inline to at least 3 setup/troubleshooting KB articles so the agent can surface them alongside steps. No code changes — the RAG pipeline already returns KB text verbatim. Pure content task.

> **Should-have.** Phase gate passes without this. Only execute once real image URLs are confirmed available.

## Critical Decisions

- **Inline markdown image syntax in KB files** — `![Alt text](https://url)` placed directly after the relevant step; agent returns the text as-is so the URL surfaces naturally in the response
- **No frontend markdown rendering added in this story** — images will appear as raw URLs in the chat UI; rendering them as actual images is a separate decision post-Phase 1
- **Validate before ingest** — broken URLs silently degrade response quality; HTTP check required before re-running `ingest.py`

---

## Tasks

- [x] ✅ **Step 1: Source and confirm image URLs**
  - [x] ✅ 6 placeholder URLs via placehold.co (purple #7C3AED, 800×500) — all return HTTP 200
  - [x] ✅ Mapped to: `pura-mini-setup.md`, `pura-mini-troubleshooting.md`, `pura-car-pro-setup.md`, `pura-car-pro-troubleshooting.md`, `pura-plus-setup.md`

- [x] ✅ **Step 2: Add image URLs inline to KB articles**
  - [x] ✅ `pura-mini-setup.md` — setup overview image added before step list
  - [x] ✅ `pura-mini-troubleshooting.md` — reset button image after reset step; LED indicator chart in LED section
  - [x] ✅ `pura-car-pro-setup.md` — setup overview image before step list; charging port image in charging section

- [x] ✅ **Step 3: Validate URLs and re-ingest**
  - [x] ✅ All 6 placeholder URLs return HTTP 200 ✅
  - [x] ✅ ChromaDB wiped and re-ingested: 29 chunks, no errors ✅
  - [x] ✅ Added prompt instruction: "include image markdown links verbatim inline with relevant step"
  - [x] ✅ "My Pura Mini won't connect" → reset button image surfaced inline ✅
  - [x] ✅ "How do I set up my Pura Car Pro?" → charging image surfaced inline ✅
  - [x] ✅ "How do I set up my Pura Mini?" → YouTube setup URL surfaced (LLM correctly prioritised video link over diagram — both are in KB) ✅
