# Product Requirements Document: Viral Content Agent Team

## 1. Executive Summary
The Viral Content Agent Team is an autonomous squad designed to transform mundane or "boring" topics into highly engaging social media content (specifically Twitter Threads and LinkedIn Posts). It automates the creative process of angle discovery, drafting, and editorial refinement to maximize engagement and "virality."

## 2. System Identity & Architecture
**Identity:** A specialized creative agency in a box, consisting of three distinct agent personas working in a feedback loop.
**Architecture:** A sequential agentic workflow (Pipeline) where data flows from research to drafting to review.
The system ensures that no content is finalized until it passes a strict "Virality Score" threshold set by the Chief Editor.

## 3. Core Capabilities (The "Skills")

### 🕵️‍♂️ Trend Scout (Researcher)
*   **Role:** The Angle Hunter.
*   **Tooling:** Powered by Tavily API.
*   **Function:**
    *   Takes the user's input topic (e.g., "Supply Chain Logistics" or "Database Normalization").
    *   Searches for the latest news, trending discussions, or contrarian takes related to the topic.
    *   Identifies unique "angles" that make the topic relevant to a broader audience (e.g., connecting it to a current event, a celebrity, or a universal pain point).

### ✍️ Ghostwriter (The Creator)
*   **Role:** The Hook Master.
*   **Tooling:** Powered by Groq API (meta-llama/llama-4-maverick-17b-128e-instruct).
*   **Function:**
    *   Ingests the research and angles provided by the Trend Scout.
    *   Drafts the actual content (Twitter Thread or LinkedIn Post).
    *   **Key Focus:**
        *   **Hooks:** Writes stopping-power opening lines.
        *   **Readability:** Uses short sentences, white space, and punchy copy.
        *   **Formatting:** Optimizes for the specific platform (e.g., threads for Twitter, longer form for LinkedIn).

### ⚖️ Chief Editor (The Critic)
*   **Role:** The Virality Gatekeeper.
*   **Tooling:** Powered by Groq API.
*   **Function:**
    *   Reviews the Ghostwriter's draft.
    *   Scores the post on a "Virality Scale" (0-100) based on specific criteria:
        *   **Hook Strength:** Is it click-baity enough without being misleading?
        *   **Emoji Usage:** Is it tasteful or cringey?
        *   **Structure:** Are paragraphs too long? Is the rhythm right?
    *   **Feedback Loop:** If the score is below a threshold (e.g., 85/100), it rejects the draft and provides specific, actionable feedback (e.g., "The hook is weak, try using a statistic," "Too many emojis in paragraph 2").

## 4. Technical Stack
*   **Orchestration:** LangGraph (Python)
*   **LLM Engine:** Groq (Llama 4 for high-quality creative writing)
*   **Search/Scrape:** Tavily (for finding trending angles)
*   **Interface:** Streamlit

## 5. User Workflow
1.  **Input:** User provides a topic (e.g., "Accounting Software") and a target platform (Twitter or LinkedIn).
2.  **Research:** Trend Scout finds 3-5 unique angles/news items.
3.  **Drafting:** Ghostwriter selects the best angle and writes a draft.
4.  **Review:** Chief Editor scores the draft.
    *   *Pass:* Content is output to the user.
    *   *Fail:* Feedback is sent back to Ghostwriter for iteration.
5.  **Output:** User receives a ready-to-post thread or article.

## 6. Success Criteria
*   **Virality Score:** Consistently producing content that scores >80/100 by the Chief Editor.
*   **Transformation:** Successfully turning dry technical topics into accessible, engaging narratives.
*   **Efficiency:** Completing the research-write-review loop in under 2 minutes.