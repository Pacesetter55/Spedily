# Spec: Login and Logout

## Overview
This step implements session-based authentication so that registered users can sign in and sign out of Spendly. The `GET /login` route and `login.html` template already exist as stubs; this step adds the `POST /login` handler (credential verification, session creation, redirect to dashboard), the functional `GET /logout` route (session teardown, redirect to landing), and a `login_required` decorator to guard future protected routes. No protected routes are added here — that comes in later steps — but the decorator is introduced now so subsequent steps can use it immediately.

## Depends on
- Step 01 — Database Setup (`users` table must exist, `get_db()` must work)
- Step 02 — Registration (at least one user must exist to test login)

## Routes
- `GET  /login`  — render login form — public (already exists; update to redirect logged-in users)
- `POST /login`  — verify credentials, create session, redirect to dashboard placeholder — public
- `GET  /logout` — destroy session, redirect to `/` — logged-in only

## Database changes
No database changes. The existing `users` table already stores `email`, `username`, and `password_hash` — all that login needs. The `get_user_by_email` helper already exists in `database/db.py`.

## Templates
- **Modify:** `templates/login.html`
  - Add a `POST` form with `email` and `password` fields
  - Add an `{% if error %}` block to display inline validation errors
  - Add a link to `/register` for new users
  - All standard: extends `base.html`, uses CSS variables

## Files to change
- `app.py`
  - Import `session` from `flask` (alongside existing flask imports)
  - Import `check_password_hash` from `werkzeug.security` (alongside existing werkzeug import)
  - Replace the stub `GET /login` route with a combined `GET`/`POST` handler
  - Replace the stub `GET /logout` route with a working implementation
  - Add a `login_required` decorator (defined above the routes) that checks `session.get('user_id')` and redirects to `/login` if absent
- `templates/login.html` — add form, error block, and register link

## Files to create
None.

## New dependencies
No new dependencies. `flask` (already installed) provides `session`; `werkzeug` (already installed) provides `check_password_hash`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only `user_id` and `username` in the session — never store `password_hash`
- `GET /login` must redirect to `/profile` (or a suitable placeholder) if the user is already logged in — prevents re-login loops
- `POST /login` validation order: (1) both fields present, (2) email exists in DB, (3) password matches hash — always show the same generic error ("Invalid email or password") for steps 2 and 3 to avoid user enumeration
- `GET /logout` must work via a plain link (GET) — no CSRF token required at this stage
- `login_required` must preserve the originally requested URL via `next` query parameter so future steps can redirect back after login

## Definition of done
- [ ] Visiting `/login` renders a form with email and password fields
- [ ] Submitting valid credentials creates a session and redirects away from `/login`
- [ ] Submitting an unknown email shows "Invalid email or password" and keeps the form
- [ ] Submitting a wrong password shows "Invalid email or password" and keeps the form
- [ ] Submitting with any field empty shows a validation error
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, visiting `/logout` again redirects to `/login` (session is gone)
- [ ] A logged-in user visiting `/login` is redirected away (no re-login loop)
- [ ] The `login_required` decorator returns a redirect to `/login` for an unauthenticated request
