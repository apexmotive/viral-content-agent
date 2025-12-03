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

### ⚖️ Chief Editor (The Active Editor)
*   **Role:** The Virality Gatekeeper & Final Polisher.
*   **Tooling:** Powered by Groq API.
*   **Function:**
    *   Reviews the Ghostwriter's draft.
    *   Scores the post on a "Virality Scale" (0-100) based on specific criteria:
        *   **Hook Strength:** Is it compelling enough to stop the scroll?
        *   **Emoji Usage:** Is it tasteful or excessive?
        *   **Structure:** Are lines short and punchy? Is the rhythm right?
        *   **Platform Optimization:** Does it fit the platform's best practices?
    *   **Active Editor Pattern:** 
        *   If score < threshold: Provides specific, actionable feedback and sends back to Ghostwriter
        *   If score ≥ threshold: Applies final polish directly instead of just approving
    *   **Transparency:** All scores and feedback are tracked for each draft iteration


## 4. Technical Stack
*   **Orchestration:** LangGraph (Python)
*   **LLM Engine:** Groq (Llama 4 for high-quality creative writing)
*   **Search/Scrape:** Tavily (for finding trending angles)
*   **Interface:** Streamlit

## 5. User Workflow
1.  **Input:** User provides a topic and selects platform (Twitter or LinkedIn). Can customize settings (model, iterations, threshold) in sidebar.
2.  **Research:** Trend Scout finds 3-5 unique angles/news items.
3.  **Drafting:** Ghostwriter creates content using the best angles with poetic, short-line structure.
4.  **Review:** Chief Editor scores the draft.
    *   **Score < Threshold:** Specific feedback sent back to Ghostwriter for revision (tracked in history).
    *   **Score ≥ Threshold:** Chief Editor applies final polish and approves.
5.  **Output:** User receives:
    *   Final polished content ready to post
    *   Complete draft history with scores
    *   All feedback and reviews from Chief Editor
    *   Research angles and sources from Trend Scout


## 6. Success Criteria
*   **Virality Score:** Consistently producing content that scores >80/100 by the Chief Editor.
*   **Transformation:** Successfully turning dry technical topics into accessible, engaging narratives.
*   **Efficiency:** Completing the research-write-review loop in under 2 minutes.