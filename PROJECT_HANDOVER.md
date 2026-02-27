# 🚀 PROJET PPE - ROBO-ADVISOR (HANDOVER DOCUMENT)
**Date**: 07 Février 2026
**Status**: Phase 5/6 (Refinement & Expansion) Completed
**Stack**: Python (FastAPI), SQLite, Pandas, Vanilla JS/HTML/CSS

---

## 🎯 Project Goal & Philosophy
**Commercial Product**: A turnkey Robo-Advisor designed for **busy, non-expert users**.
**Core Pillars**:
1.  **Transparency**: Every decision (asset choice, weight) is explained in plain French (no jargon).
2.  **Simplicity**: Quick flow for users with little time.
3.  **REGULATORY COMPLIANCE (CRITICAL)**: Use strictly MiFID II compliant processes.
    - Safety-First logic (Capacity > Performance).
    - Hard locks on Expert features (Black-Litterman).
    - No "black box" optimizations.

Key components:
- **Questionnaire**: Collects goals, horizon, risk tolerance, capacity, knowledge.
- **Profiling**: Scores risk (0-1) and assigns a composite profile (Prudent/Equilibré/Dynamique).
- **Optimization**: Uses Markowitz Mean-Variance + Black-Litterman (for experts) to allocate assets.
- **Universes**: Wide range of ETFs and Stocks (US, EU, Global, Emerging, Bonds).

---

## ✅ Current State (What Works)

### 1. Asset Universe (Expanded & Dynamic)
- **Size**: **154 Assets** (Stocks & ETFs only).
- **Scope**: Major global indices (S&P 500, CAC 40, DAX), Thematic ETFs (Tech, Health), Bonds.
- **Exclusions**: Gold, Crypto, and Commodities were explicitly removed per user request.
- **Tech**: `src/data/data_loader.py` uses **Dynamic Classification** based on Yahoo Finance metadata (`quoteType`, `currency`, `exchange`) to automatically tag assets as US/EU/EM/Bonds.
- **Refresh**: Universe is cached in `data/universe.csv` and auto-refreshes if older than 7 days (or forced via `scripts/refresh_universe.py`).

### 2. Smart Questionnaire & Suggestion Engine
- **Unidirectional Logic**: Suggestions only flow forward (e.g., Horizon -> Risk), never backward, to prevent loops.
- **Safety-First**: Hard constraints (Capacity=None, Goal=Safety) **always override** performance suggestions.
    - *Example*: A user with "Long Horizon" but "No Loss Capacity" will be suggested "Low Risk", not "High Risk".
- **Expert Gating**: The **Black-Litterman** (Market Views) feature is strictily locked for "Expert" profiles. Switching to "Novice" auto-disables and clears it.
- **Visuals**: Real-time coherence indicators (✅ Excellent, ⚠️ Needs Reflection) and contextual tooltips.

### 3. Portfolio Generation
- **Optimization**: `src/portfolio/optimizer.py` handles the math.
- **Constraints**:
    - **Min/Max Assets**: 2 to 10 assets globally.
    - **Concentration**: Dynamic max weight/asset based on risk profile (Prudent=50%, Dynamic=30%).
    - **Small Amounts**: specific logic for <1000€ portfolios to avoid fragmentation.

### 4. Explanations (Pedagogy)
- **Transparency**: Every asset has a generated reason ("Core", "Diversification", "Reliability").
- **Tooltips**: Contextual interpretations for Sharpe Ratio, Volatility, and Returns (e.g., "Good balance for a prudent profile").

---

---

## 📜 Project History (Completed Phases)

### Phase 1: Core Engine (MVP)
- **Goal**: Create the mathematical backend.
- **Features**: Markowitz Mean-Variance Optimization, Basic Risk Profiling (0-1 score), Data Fetching from Yahoo Finance.

### Phase 2: Authentication & Web Platform
- **Goal**: Transform script into a web app.
- **Features**: User Accounts (Login/Register), Dashboard, Portfolio Saving (SQLite), FastAPI integration.

### Phase 3: Advanced Optimization
- **Goal**: Integrate professional models.
- **Features**: **Black-Litterman Model** implementation for expert views, Confidence-based optimization logic.

### Phase 4: UX Refinement
- **Goal**: Polish the user journey.
- **Features**: Improved Profile Page, better visual feedback, initial "Why this asset?" explanations.

### Phase 5: Commercial-Grade Refinement
- **Goal**: Make portfolios realistic and usable.
- **Features**: Realistic constraints (2-10 assets), dynamic concentration limits (30-50%), Small portfolio logic (<1000€).

### Phase 6: Portfolio Lifecycle Management
- **Goal**: Handle decision flows.
- **Features**: Accept/Reject workflows, ensuring only one "Active" portfolio per user, regeneration caching.

### Phase 7: Transparency & Education
- **Goal**: Explain the "Why".
- **Features**: Detailed asset role explanations (Core/Diversification), Contextual Tooltips (Sharpe, Volatility), French translations.

### Phase 8: Smart Suggestions Engine
- **Goal**: Guide users responsively.
- **Features**: Real-time suggestion engine in the questionnaire (e.g., "Long Horizon suggests Higher Risk"), Coherence Score UI.

### Phase 9: Pedagogical Logic (Safety-First)
- **Goal**: Enforce financial safety.
- **Features**: Unidirectional suggestion flow (no loops), **Safety-First Logic** (Capacity > Performance), Tone adaptation (Novice vs Expert).

### Phase 10: Asset Universe Expansion
- **Goal**: Scale for production.
- **Features**: Expansion to **154 Assets** (Stocks/ETFs), Dynamic Classification Engine (Auto-tagging based on metadata).

### Phase 11: Compliance & Gating (MiFID II)
- **Goal**: Regulatory compliance.
- **Features**: **Expert Feature Gating** (Locking Black-Litterman for non-experts), Auto-reset mechanisms for safety.

---

## 🏗️ Architecture & Key Files

### Backend (`src/`)
- `api/main.py`: Entry point.
- `api/endpoints.py`: All API routes.
- `data/data_loader.py`: **CRITICAL**. Handles Yahoo Finance fetching & classification.
- `portfolio/optimizer.py`: Markowitz/BL core logic.
- `profile/suggestion_rules.py`: **CRITICAL**. The logic engine for questionnaire hints (Field priority, Safety-First rules).
- `utils/config.py`: Ticker lists (`DEFAULT_ETF_TICKERS`), constants (`RISK_ALLOCATIONS`).

### Frontend (`templates/` & `static/`)
- `templates/nouvel_invest.html`: Main interface. Contains the JS logic for Black-Litterman gating (`toggleViewsSection`) and form handling.
- `static/js/smart-suggestions.js`: Client-side logic for real-time suggestions and coherence checks.

---

## 📝 Remaining Tasks (Next Steps)

Refer to `brain/.../task.md` for granular details. Main items left:

1.  **Portfolio Concentration Refinement** (Phase 5, Item 5)
    - [ ] Implement `EXPERT` concentration bonus (Experts can have more concentrated bets).
    - [ ] Verify high-conviction portfolios.

2.  **Questionnaire Wording & Order** (Phase 9)
    - [ ] Reorder fields (Knowledge first).
    - [ ] Simplify wording (remove jargon for novices).

3.  **Testing** (Phase 7)
    - [ ] Verify portfolio generation for different amounts (50€ vs 50k€).
    - [ ] "Garder" button integration test (ensure it appears in `suivi_invest.html`).

---

## 💡 Notes for Next AI
- **Strict Constraint**: The user wants **Stocks & ETFs ONLY**. Do not re-add Gold/Commodities.
- **Safety**: The "Safety-First" priority logic in `suggestion_rules.py` is complex (Tier 1 vs Tier 2 rules). Be careful when modifying priorities.
- **Classification**: If adding new assets, check `classify_asset()` in `data_loader.py` to ensure they are caught correctly (especially EU vs US).
