# SUH-12 — Troubleshooting Wizard: Detect Intent → Guided Step-by-Step Flow

**Linear:** SUH-12 / CAP-4.S-1
**Overall Progress:** `95%`

## TLDR

Extend `BASE_PROMPT` in `backend/main.py` with troubleshooting wizard instructions. When the agent detects a device problem, it confirms the model (if unknown), asks one clarifying question (if needed), then delivers numbered steps grounded in RAG context. No new endpoints, no frontend changes — prompt engineering only.

## Critical Decisions

- **Prompt-only implementation** — RAG already retrieves the right `pura-*-troubleshooting.md` articles; the LLM just needs clear instructions on how to structure the response when troubleshooting intent is detected
- **Extend `BASE_PROMPT`, not `build_system_prompt`** — `BASE_PROMPT` is prepended to both the context and no-context paths; a single extension covers all cases without duplicating logic
- **One clarifying question at a time** — explicitly instructed in the prompt; prevents the LLM from dumping a multi-question interrogation which degrades UX

---

## Tasks

- [x] ✅ **Step 1: Extend `BASE_PROMPT` with troubleshooting wizard instructions**
  - [x] ✅ Appended `## Troubleshooting Mode` section to `BASE_PROMPT` with: device-first rule, one-question rule, numbered steps instruction
  - [x] ✅ Listed all 5 issue categories with trigger phrases so LLM knows what to detect

- [x] ✅ **Step 2: Validate intent detection across 5 phrasings × 5 categories**
  - [x] ✅ Connectivity: 5/5 — all phrasings triggered wizard (model question or immediate steps) ✅
  - [x] ✅ Pairing: 5/5 ✅
  - [x] ✅ No scent: 5/5 ✅
  - [x] ✅ LED: 4/5 on manual review (automated keyword check flagged 3/5; "solid red light" DID ask for model — keyword miss). Note: "what does the red light mean on my pura 3" is a content gap — KB lacks explicit LED color mappings; agent correctly offered escalation ✅
  - [x] ✅ Battery/Power: 4/5 ("how do I charge the car pro" answered directly — informational, not troubleshooting intent) ✅
  - [x] ✅ Model-unknown path confirmed: "my pura device isn't working" → "Which Pura model do you have?" ✅
  - [x] ✅ Multi-turn wizard confirmed: "won't connect" → asks model → "Pura Mini" → numbered steps from `pura-mini-troubleshooting.md` ✅

- [ ] 🟥 **Step 3: Browser smoke test**
  - [ ] 🟥 Open `http://localhost:5173`, type "my device won't connect" — confirm agent asks which model
  - [ ] 🟥 Reply with "Pura Mini" — confirm agent gives numbered steps
  - [ ] 🟥 Confirm steps are grounded in `pura-mini-troubleshooting.md` content (2.4 GHz, reset, etc.)
