# PRD: Pura Customer Support AI Agent  
**Product Name:** Pura Support Agent (in-app AI assistant)  
**Version:** 1.0 (MVP)  
**Date:** April 17, 2026  
**Author:** Suhail (Product Manager)  
**Status:** Draft – Ready for roadmap & phased delivery  

---

## 1. Problem Definition

### What’s the problem?
Pura customers currently rely on fragmented support channels (email, simple non semantic chatbot , Help Center articles, and phone) to get help with their smart fragrance diffusers. Common topics include product-specific questions (Pura 4™, Pura Plus™, Pura Mini™, Pura 3™, Pura Car Pro™, Pura Car™), Diffuser Setup, Fix a Problem, Account & Subscription Management, Order Status, Orders & Shipping, FAQ’s & Guides, and Contact Customer Care.  

Support volume is high and repetitive. Many queries are simple or transactional (order status, basic troubleshooting, subscription changes), but customers wait hours or days for answers. This leads to frustration, abandoned setups, higher return rates, and lower subscription retention. The current Help Center is static and requires customers to search themselves, while live agents are overwhelmed with repetitive tickets.

### Why are we solving this problem?
Customers expect instant, 24/7 help for hardware + subscription products in 2026. An AI agent can handle 60-80% of repetitive queries accurately, freeing human agents for complex or emotional issues. This directly addresses the biggest friction points identified in ticket data and user interviews.

### How does solving this benefit customers and the business?

**For Customers:**
- Instant answers 24/7 (no more waiting for business hours).
- Guided, conversational help (e.g., step-by-step setup for Pura Car Pro™ instead of reading a long article).
- Personalized support (order lookup, subscription management) without leaving the app.
- Higher satisfaction and faster “scent happiness” — fewer returns, stronger brand love.

**For the Business:**
- Significant ticket deflection (target: 50-70% reduction in support volume for the 13 core topics).
- Lower cost per interaction (AI is cheaper than human agents at scale).
- Improved key metrics: CSAT ≥4.5/5, subscription retention, repeat purchase rate.
- Data moat: conversation logs will reveal new product insights and feature gaps.
- Competitive edge: Pura becomes the premium fragrance brand with the smartest, most responsive support experience.

---

## 2. User

### Primary Persona: “Sarah the Busy Scent Lover”
- **Demographics:** 28–45 years old, female (70% of customer base), urban/suburban, tech-comfortable but not expert.  
- **Role/Behavior:** Busy professional or parent who owns 1–3 Pura diffusers (home + car). Heavy subscriber to fragrance pods. Shops via mobile app or website.  
- **Tech:** Uses iOS/Android app daily; expects Amazon-level convenience.

### Pain Points
- Can’t find quick answers in the Help Center (“Where is the setup video for Pura 4™?”).
- Waits 2–48 hours for order status or subscription change confirmation.
- Gets stuck during setup or troubleshooting (“My Pura Mini™ won’t connect — what now?”) and gives up.
- Frustrated when live chat is offline or agents repeat basic questions.
- Doesn’t want to call or email for simple things.

### Wants & Needs
- Natural conversation (“Hey, my Pura Car Pro isn’t working — help!”).
- Context-aware help (knows her order/subscription if logged in).
- Step-by-step guidance with images or links.
- Clear escalation path to a human when needed.
- Friendly, premium, scent-obsessed tone (“Let’s get that perfect scent flowing again!”).

### Current Journey
1. Buys diffuser or pods → receives order confirmation.  
2. Tries to set up → gets stuck → searches Help Center or emails support.  
3. Needs order/subscription change → logs into account → still confused → opens ticket.  
4. Problem occurs (device issue) → frustrated → contacts support or returns product.  
5. Rarely returns to buy more because experience felt slow/painful.

With the new Support Agent, the journey becomes: Open app → type or tap “Ask Pura” → get instant, accurate help in one conversation.

---

## 3. Solution

### High-Level Solution
An in-app conversational AI agent (chat widget) powered by LLM + RAG that covers all 13 core topics. It uses Pura’s existing Help Center content, product manuals, and backend APIs for real-time data (orders, subscriptions, account info).  

**Core Capabilities (MVP):**
- **Informational & Guided Flows** (full coverage): Product info (Pura 4™, Plus™, Mini™, 3™, Car Pro™, Car™), Diffuser Setup, FAQ’s & Guides, Fix a Problem (top 5 issues as decision-tree wizards).
- **Transactional Flows** (read-only + safe actions): Order Status, Orders & Shipping, basic Account & Subscription Management (view, skip shipment, update payment).
- **Smart Behaviors:** Topic detection at start, multi-turn conversation, user authentication (must be logged in for account/order flows), clear escalation to human agent or ticket creation.
- **Brand Experience:** Warm, premium, helpful tone. Mobile-first chat widget inside the Pura app.

### Key Features
- RAG knowledge base synced with Help Center (auto-updates when new articles are published).
- Secure API integrations (Shopify or existing backend) for order/subscription data.
- Guided troubleshooting with image links and step-by-step instructions.
- Handoff to live agent with full conversation transcript.
- Analytics dashboard for CS team (top queries, resolution rate, escalation points).

### Non-Goals (for MVP)
- Voice interface.
- Photo/video upload for troubleshooting.
- Proactive messages (e.g., “Your next shipment is in 3 days”).
- Multi-language support.
- Full write actions on subscriptions (e.g., cancel entirely — keep as human-only).

---

## 4. Goals

### Primary Goals (Success Metrics)
1. **Ticket Deflection** – 50–70% reduction in support tickets for the 13 covered topics within 90 days of launch.
2. **Resolution Rate** – ≥85% of conversations resolved without human escalation.
3. **Customer Satisfaction** – CSAT ≥4.5/5 (post-chat survey).
4. **Speed** – Average response time <2 seconds; full conversation resolution in <3 minutes.
5. **Adoption** – ≥40% of support-seeking users engage with the AI agent in first month.

### Secondary Goals
- Increase subscription retention by 5–10% (faster issue resolution = happier subscribers).
- Reduce average support cost per interaction by 60%.
- Gather actionable product insights from conversation logs (e.g., most common setup issues).

### Measuring Success
- Pre/post launch comparison of ticket volume, CSAT, and resolution time.
- Conversation analytics (resolution rate, drop-off points, escalation triggers).
- Weekly review of top failure modes to improve RAG and flows.
- Qualitative feedback from beta users and CS team.
