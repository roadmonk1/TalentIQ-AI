# Phase 7 — Database Persistence Design (PostgreSQL + SQLAlchemy)

This document describes the proposed database schema and persistence strategy for Phase 7. It is a design-only artifact; no models or migrations are implemented yet.

## Goals
- Persist user resume profiles, TalentCore scores, Mentor sessions and messages, memory objects, missions, and timeline events.
- Use PostgreSQL for reliable storage and SQLAlchemy ORM for Python models.
- Use Alembic for migrations.

## High-level entities

1. `users`
   - Existing `User` model remains; store reference `user_id` in all user-owned entities.

2. `resume_profiles`
   - id (UUID PK)
   - user_id (FK -> users.id)
   - source (enum: upload|demo|import)
   - filename
   - raw_text (text)
   - parsed_profile (JSONB)
   - created_at, updated_at
   - metadata (JSONB) — word counts, parsing stages

3. `talentcore_scores`
   - id (UUID PK)
   - profile_id (FK -> resume_profiles.id)
   - career_score (numeric)
   - resume_score (numeric)
   - ats_score (numeric)
   - breakdown (JSONB)
   - generated_at

4. `mentor_sessions`
   - id (UUID PK)
   - user_id (FK -> users.id)
   - target_career (string)
   - mode (string)
   - summary (text)
   - metadata (JSONB)
   - created_at, updated_at

5. `mentor_messages`
   - id (UUID PK)
   - session_id (FK -> mentor_sessions.id)
   - role (enum: user|assistant|system)
   - text (text)
   - metadata (JSONB)
   - created_at
   - indexed columns: session_id, role, created_at

6. `mentor_memory`
   - id (UUID PK)
   - session_id (FK -> mentor_sessions.id)
   - key (string) — memory type (conversation_summary, profile_snapshot, embeddings_ref)
   - value (JSONB)
   - ttl/expires_at (optional)
   - created_at, updated_at

7. `missions`
   - id (UUID PK)
   - user_id (FK -> users.id)
   - session_id (FK -> mentor_sessions.id) nullable
   - title
   - description
   - status (enum: pending|accepted|completed|skipped)
   - schedule (JSONB) — daily/weekly plan
   - created_at, due_date, completed_at

8. `timeline_events`
   - id (UUID PK)
   - user_id (FK -> users.id)
   - type (string)
   - payload (JSONB)
   - occurred_at

## Relationships
- `users` 1—* `resume_profiles`
- `resume_profiles` 1—1 `talentcore_scores` (or 1—* for multiple snapshots)
- `mentor_sessions` 1—* `mentor_messages`
- `mentor_sessions` 1—* `mentor_memory`
- `users` 1—* `missions`

## Indexing & Performance
- Index `mentor_messages(session_id, created_at)` for fast conversation retrieval.
- GIN index on JSONB columns (`parsed_profile`, `breakdown`, `metadata`) for querying.
- Consider full-text index (tsvector) on `resume_profiles.raw_text` for search.

## SQLAlchemy + Alembic Plan
1. Add SQLAlchemy models in `backend/app/models` or `backend/app/db_models.py` with declarative base.
2. Configure `SQLALCHEMY_DATABASE_URI` via `DATABASE_URL` env var.
3. Initialize Alembic configuration, set `env.py` to use Flask app context and SQLAlchemy metadata.
4. Create initial migration: users (existing), resume_profiles, talentcore_scores, mentor_sessions, mentor_messages, mentor_memory, missions, timeline_events.
5. Add migrations to maintain schema as features evolve (e.g., add indexes, partition large tables).

## Consistency and Backups
- Use transactional writes when writing session + messages.
- Consider periodic backups (pg_dump) and retention policy for alpha.

## Embeddings and Vector Stores (optional)
- If storing embeddings for memory, keep embeddings in a dedicated table or external vector DB (Pinecone/PGVector) and store references in `mentor_memory`.

## Notes
- This is a design doc only. Implementation will follow after architecture approval.
