# SUH-11 — Conversation Memory: Pass History to Groq

**Linear:** SUH-11 / CAP-3.S-3
**Overall Progress:** `95%`

## TLDR

Send accumulated conversation turns with every `POST /chat` request so Groq has context to resolve follow-ups like "What about the Mini?" or "How do I fix that?". Frontend builds and sends history; backend inserts it between the system prompt and current user message. Backend stays stateless — no sessions, no DB needed.

## Critical Decisions

- **Frontend sends history, backend is stateless** — `useChat.ts` already holds `messages[]`; cheapest possible implementation is to send a slice of it with every request. No server-side session state needed in Phase 1
- **Role mapping in `useChat.ts`** — frontend uses `"agent"`, Groq requires `"assistant"`; map at the send site so backend just passes through and curl tests with `"assistant"` also work
- **Backend caps at `MAX_HISTORY_TURNS = 6`** — frontend sends all accumulated messages; backend takes only the last 6 as a safety net against unbounded token growth (Groq free tier: 6,000 tokens/min)
- **`history` optional in `ChatRequest`** — defaults to `None`; existing single-turn curl tests require no changes

---

## Tasks

- [x] ✅ **Step 1: Update `backend/main.py` to accept and inject history**
  - [x] ✅ Add `MAX_HISTORY_TURNS = 6` constant
  - [x] ✅ Add `HistoryItem` Pydantic model; extend `ChatRequest` with `history: list[HistoryItem] | None = None`
  - [x] ✅ In `stream_groq_response(message, history)`: build Groq `messages` list as `[system, *history[-MAX_HISTORY_TURNS:], user]`

- [x] ✅ **Step 2: Update `frontend/src/hooks/useChat.ts` to send history**
  - [x] ✅ Snapshot `messages` BEFORE appending new user message (avoids double-sending current turn)
  - [x] ✅ Map role `"agent"` → `"assistant"`, strip `id`, filter empty placeholders
  - [x] ✅ Include `history` in the `POST /chat` body alongside `message`

- [x] ✅ **Step 3: Validate multi-turn memory**
  - [x] ✅ 5-turn test: device context carried across all turns correctly
    - Turn 2: "What Wi-Fi band?" → remembered Pura 3 → "2.4 GHz" ✅
    - Turn 4: "How long does its battery last?" → remembered Car Pro → "15 hours" ✅
    - Turn 5: "How long does a cartridge last?" → still Car Pro → "30 days" ✅
  - [x] ✅ Single-turn curl without `history` field: works, no errors ✅
  - [ ] 🟥 Visual browser test: send a 3-turn conversation, confirm follow-ups resolve without repeating context
