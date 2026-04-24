# SUH-6 — Streaming Chat: Send Message + Stream Response

**Linear:** SUH-6 / CAP-2.S-2
**Overall Progress:** `95%`

## TLDR

Build the core chat interaction loop: user types a message, hits Enter or Send, their message appears instantly in history, and the agent's reply streams token-by-token from the backend. Includes frontend scaffold and widget shell (CAP-2.S-1 prerequisite — no frontend exists yet), plus a mock streaming backend stub so the frontend can be tested independently of Groq (CAP-3.S-1).

## Critical Decisions

- **Fetch ReadableStream over EventSource** — works with any chunked `text/plain` response; simpler to consume than SSE and aligns with how Groq streaming will be wired in CAP-3.S-1
- **`useChat` hook** — all message state and streaming logic lives in one hook; `ChatWidget` is pure presentation
- **Mock FastAPI streaming stub** — `POST /chat` returns a fake chunked response so frontend can be fully validated before real Groq is wired in CAP-3.S-1
- **TypeScript strict, no `any`** — per CLAUDE.md conventions throughout

---

## Tasks

- [x] ✅ **Step 1: Scaffold React + Vite + Tailwind frontend**
  - [x] ✅ Run `npm create vite@latest frontend -- --template react-ts` from project root
  - [x] ✅ Install Tailwind CSS and configure `vite.config.ts` + `index.css`
  - [x] ✅ Strip Vite boilerplate (`App.tsx`, `index.css`) down to a blank root
  - [ ] 🟥 Confirm `npm run dev` starts cleanly on `localhost:5173`

- [x] ✅ **Step 2: Build chat widget shell (CAP-2.S-1)**
  - [x] ✅ Create `frontend/src/components/ChatWidget.tsx` — full-height panel layout: message list area + input row at bottom
  - [x] ✅ Create `frontend/src/components/MessageBubble.tsx` — renders a single message; `role: "user" | "agent"` drives alignment and colour
  - [x] ✅ Empty state: welcome message `"Hi! Ask me anything about your Pura."` shown when history is empty
  - [x] ✅ Text input is focused by default on mount
  - [x] ✅ Layout is readable at 1280px wide (standard desktop)

- [x] ✅ **Step 3: Add mock streaming endpoint to backend**
  - [x] ✅ Create `backend/main.py` with FastAPI app; CORS open for `localhost:5173`
  - [x] ✅ `POST /chat` — accepts `{ message: string }`; returns a `StreamingResponse` that yields a mock sentence word-by-word with a small delay (~40ms between tokens) to simulate streaming
  - [x] ✅ Confirm endpoint reachable: `curl -N -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"test"}'`

- [x] ✅ **Step 4: Implement `useChat` hook — message state + streaming**
  - [x] ✅ Create `frontend/src/hooks/useChat.ts`
  - [x] ✅ State: `messages: Message[]`, `streaming: boolean`
  - [x] ✅ `sendMessage(text: string)` — appends user message immediately, then opens a `fetch` to `POST /chat` and reads the response body as a `ReadableStream`
  - [x] ✅ Streaming: append an empty agent message on stream start; update its `content` in-place as each chunk arrives (no new bubble per token)
  - [x] ✅ Set `streaming = false` when the stream closes or errors
  - [x] ✅ On network/backend error, append an agent message: `"Something went wrong. Please try again."`

- [x] ✅ **Step 5: Wire submission + streaming into `ChatWidget`**
  - [x] ✅ Send button click and Enter keypress both call `sendMessage`
  - [x] ✅ Guard: ignore submit if input is empty or `streaming === true`
  - [x] ✅ Input field and Send button are `disabled` while `streaming === true`; re-enabled on completion
  - [x] ✅ Message list auto-scrolls to the bottom after each state update (use a `ref` on the list container)

- [x] ✅ **Step 6: Smoke test end-to-end**
  - [x] ✅ Run backend (`uvicorn main:app --reload`) and frontend (`npm run dev`) together
  - [x] ✅ Confirm streaming response arrives word-by-word (2s end-to-end for mock sentence)
  - [x] ✅ CORS header `access-control-allow-origin: http://localhost:5173` confirmed
  - [x] ✅ TypeScript strict check passes with zero errors
  - [ ] 🟥 Visual browser test: user message appears instantly, agent streams token-by-token, input locks/unlocks, auto-scroll tracks latest message, error state on backend kill
