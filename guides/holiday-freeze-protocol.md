# Operational Protocol: The Holiday Code Freeze (2026 Edition)

> **Context**: Managing autonomous agents during low-staff periods.
> **Shift**: From "Stop All Work" to "Agentic Frost".

## 1. The Paradigm Shift
Traditionally, a "Code Freeze" meant no developers touched the code to prevent instability while staff was away. In 2026, agents don't take holidays. This led to the concept of **"Agentic Frost"**—a state where human deployment stops, but agentic development accelerates.

---

## 2. Definitions

### 🔴 Hard Freeze (Production)
*   **Status**: **LOCKED**.
*   **Action**: CI/CD pipelines to `production` are paused.
*   **Agent Permissions**: Revoked. Agents cannot push to `main` or trigger deployments.
*   **Goal**: Zero risk to live systems.

### 🔵 Agentic Frost (Development)
*   **Status**: **ACTIVE**.
*   **Action**: Agents work on `feature/*` branches.
*   **Workflow**:
    1.  Agents pick tickets from the backlog.
    2.  They write code, run tests, and self-heal until passing.
    3.  They open PRs with detailed summaries.
    4.  **Crucially**: No merges occur. The focus is "Backlog Elimination".
*   **Result**: When humans return, they find a queue of green, tested PRs ready for review.

---

## 3. The Feature Flag Requirement
To enable safe merging during "Soft Freeze" periods, agents are now instructed (via System Prompt) to wrap all new logic in Feature Flags.

**System Prompt Instruction:**
> "Any new functionality must be wrapped in a LaunchDarkly/PostHog feature flag. The flag default state must be 'FALSE'."

**Example (Agent Output):**
```typescript
if (features.get('new-checkout-flow', false)) {
  await renderNewCheckout();
} else {
  await renderLegacyCheckout();
}
```

This allows code to land in `main` without risking stability, as the code path is dormant by default.

---

## 4. Checklist for Freeze Preparation

1.  [ ] **Revoke Keys**: Ensure agents can't deploy to prod.
2.  [ ] **Sandboxing**: Verify agents are running in Docker/Firecracker containers.
3.  [ ] **Budget Caps**: Set API spend limits (prevent agents from looping infinitely on a bug).
4.  [ ] **Alerting**: Route critical failures to the on-call human (P1 only).
5.  [ ] **Task Queue**: Fill the backlog with "Low Priority / High Effort" tasks (e.g., test coverage, migration, refactoring) perfect for agents.
