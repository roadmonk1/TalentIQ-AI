# TalentIQ AI Beta Testing Guide

Welcome to the TalentIQ AI Beta Testing program! This guide outlines how to perform beta testing, what feedback to look for, and the known limitations of the current Alpha/Beta release.

---

## 1. How Users Test (E2E Journey)

Follow the complete user journey checklist to validate all core functionality:

1. **Sign Up & Login**:
   - Go to `/auth` and register a new test student/job-seeker account.
   - Log in using your registered credentials to confirm cookie-less session initialization.
2. **First Dashboard Visit**:
   - Verify you are greeted with the **Empty State Welcome Card**.
   - Review the explanation text and ensure no demo data or empty chart shapes are broken.
3. **Resume Upload**:
   - Click the resume upload button inside the empty state card or quick actions panel.
   - Choose a text/PDF resume file and submit.
   - Observe the parsing stages spinner animation to verify user feedback during computation.
4. **Dashboard Analysis**:
   - Ensure the page populates with your parsed scores (Career & Resume Scores).
   - Hover over the info icon `(i)` next to the card titles to read the score calculation breakdown tooltips.
   - Review your parsed details, skill gaps list, matches list, and activity timeline.
5. **AI Mentor Conversation (TalentCoach)**:
   - Click on the **TalentCoach** link in the navigation header.
   - Type career/resume coaching questions (e.g., "how can I improve my React score?") and send.
   - Verify the mentor updates context, generates follow-up hints, and records logs.
6. **Missions Tracking**:
   - Click to accept recommended growth missions.
   - Confirm that accepted missions are correctly synchronized back onto your Dashboard checklist.

---

## 2. What Feedback to Collect

We are collecting user experience reviews across three categories. Please use the floating **Beta Feedback** button at the bottom-right corner to report:

- **Bugs & Crashes**: Any request timeouts, infinite spinners, error overlays, or parsing crashes.
- **Layout & Mobile Responsiveness**: Broken flex grids, overlapping text blocks, unreadable contrasts, or scaling problems on mobile/tablet dimensions.
- **AI Utility**: Feedback regarding recommendations relevance, Career DNA skill correctness, or response formatting.

---

## 3. Known Limitations (Alpha Preview)

Be aware of the following architectural limits:
- **Cookie-less Session Storage**: Sessions utilize JWT access tokens cached in the browser's `localStorage`. Opening the application in multiple cross-origin private tabs will require logging in again.
- **SQLite Dev Database**: The default local environment uses a thread-safe single-file SQLite database. Multiple parallel read/writes could occasionally result in temporary locking delays.
- **LLM Context Sizes**: The Groq AI coaching adapter utilizes a structured conversation prompt context. Extremely long message histories may lead to conversation pruning or slight delay increases.
