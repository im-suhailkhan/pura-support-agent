# SUH-14 + SUH-15 + SUH-16 — Escalation Detection, Transcript & Conversation Logging

**Linear:** SUH-14 (CAP-5.S-1) · SUH-15 (CAP-5.S-2) · SUH-16 (CAP-6.S-1)
**Overall Progress:** `100% ✅`

## TLDR

Three finishing stories for Phase 1, done in one session:
- **SUH-14**: Agent offers escalation when it can't resolve a query (prompt engineering)
- **SUH-15**: On escalation, agent generates a structured conversation summary the user can copy to a support ticket (prompt engineering)
- **SUH-16**: Every turn logged to SQLite after the stream closes — non-blocking, session-aware

## Critical Decisions

- **SUH-14+15 prompt-only** — both escalation detection and transcript generation extend `BASE_PROMPT`; no new endpoints or frontend changes needed
- **SUH-16: write after stream closes** — full agent response is accumulated during streaming, then both turns (user + agent) are written to SQLite in `finally` after the generator exits; satisfies non-blocking requirement without async complexity
- **SUH-16: session ID from frontend** — `crypto.randomUUID()` called once per chat session via `useRef` in `useChat.ts`; sent with every request; backend stays stateless
- **SUH-16: `db.py` module** — isolates SQLite setup and `log_turn()` from `main.py`; consistent with `retrieval.py` pattern

---

## Tasks

- [x] ✅ **Step 1 (SUH-14): Extend `BASE_PROMPT` with escalation detection**
  - [x] ✅ Added `## Escalation` section with immediate triggers and 2-failed-attempt guard
  - [x] ✅ Escalation message defined: "I wasn't able to resolve this — would you like me to connect you with the Pura support team?"

- [x] ✅ **Step 2 (SUH-15): Add transcript summary to escalation path**
  - [x] ✅ Escalation section includes exact format for Support Summary block (Issue, Steps tried, Status, Contact)
  - [x] ✅ `support@pura.com` and `pura.com/help` included as contact placeholders

- [x] ✅ **Step 3 (SUH-16A): Create `backend/db.py` and update config**
  - [x] ✅ `backend/db.py`: `init_db()` + `log_turn()`; table created on import; parent dir created automatically
  - [x] ✅ `DB_PATH=./data/conversations.db` added to `backend/.env.example`
  - [x] ✅ `backend/data/conversations.db` added to `.gitignore`

- [x] ✅ **Step 4 (SUH-16B): Wire session ID and logging into backend + frontend**
  - [x] ✅ `backend/main.py`: `log_turn` imported from `db.py`; `session_id` added to `ChatRequest`; tokens accumulated in `response_tokens`; both turns logged in `finally` after stream
  - [x] ✅ `frontend/src/hooks/useChat.ts`: `sessionId = useRef(crypto.randomUUID())` on mount; sent as `session_id` in POST body
  - [x] ✅ TypeScript strict check: zero errors

- [x] ✅ **Step 5: Validate all three end-to-end**
  - [x] ✅ Escalation: "I want to talk to a person" → immediate escalation message ✅
  - [x] ✅ Transcript: 3-turn failure loop → `Support Summary` block with contact info ✅
  - [x] ✅ Logging: 4-turn conversation → 8 rows in SQLite with correct `session_id` and roles ✅
  - [x] ✅ Non-blocking: write happens in `finally` after stream; no delay observed
