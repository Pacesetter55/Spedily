# Spec: Registration

## Overview
This step wires up the user registration form so that new accounts can actually be created and persisted in SQLite. The `register.html` template and the `GET /register` route already exist; this step adds the `POST /register` handler, a `create_user` database helper, input validation, duplicate detection, and password hashing. On success the user is redirected to `/login`. No session is started yet — that comes in Step 3.

## Depends on
- Step 01 — Database Setup (users table must exist via `init_db()`)

## Routes
- `GET  /register` — render registration form — public (already exists, no change needed)
- `POST /register` — process form submission, create account, redirect to login — public

## Database changes
No new tables or columns. The existing `users` table already has all required fields:
- `username TEXT NOT NULL UNIQUE`
- `email    TEXT NOT NULL UNIQUE`
- `password_hash TEXT NOT NULL`

Note: the register form field is named `name`; its value maps to the `username` column.

## Templates
- **Modify:** `templates/register.html`
  - The `{% if error %}` block is already present — no structural change needed.
  - Add `value="{{ form.name }}"`, `value="{{ form.email }}"` attributes so the form repopulates on validation error (prevents the user losing their input).

## Files to change
- `app.py` — add `POST /register` route; import `request`, `redirect`, `url_for`, `flash`; add `app.secret_key`
- `database/db.py` — add `create_user(username, email, password_hash)` helper and `get_user_by_email(email)` helper
- `templates/register.html` — add `value` attributes to name and email inputs for repopulation

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` (already installed via `werkzeug==3.1.6`) provides `generate_password_hash` and `check_password_hash`.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw SQLite via `get_db()` from `database/db.py`
- Parameterised queries only — never interpolate user input into SQL strings
- Hash passwords with `werkzeug.security.generate_password_hash` (default method `pbkdf2:sha256`)
- Use CSS variables — never hardcode hex values in any template or stylesheet
- All templates extend `base.html`
- Set `app.secret_key` using `os.environ.get('SECRET_KEY', 'dev-secret-change-me')` — never hardcode a production secret
- Validation order: (1) all fields present, (2) password >= 8 chars, (3) email not already registered, (4) username not already taken
- On any validation failure: re-render `register.html` with `error=<message>` and repopulate `form` dict so inputs retain their values
- On success: `redirect(url_for('login'))` — do NOT start a session yet

## Definition of done
- [ ] Submitting the form with valid data creates a new row in the `users` table
- [ ] The stored `password_hash` is NOT the plaintext password (verify in SQLite browser or `sqlite3` CLI)
- [ ] Submitting with a duplicate email shows an inline error and keeps the form populated
- [ ] Submitting with a duplicate username shows an inline error and keeps the form populated
- [ ] Submitting with a password shorter than 8 characters shows an inline error
- [ ] Submitting with any field empty shows an inline error
- [ ] Successful registration redirects to `/login`
- [ ] The `/register` GET route still works after the change (no regression)
