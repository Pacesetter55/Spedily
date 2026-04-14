import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'expense_tracker.db')


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    NOT NULL UNIQUE,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title      TEXT    NOT NULL,
            amount     REAL    NOT NULL,
            category   TEXT    NOT NULL,
            date       TEXT    NOT NULL,
            notes      TEXT,
            created_at TEXT    DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development (idempotent — skips if data exists)."""
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    conn.executescript("""
        INSERT INTO users (username, email, password_hash) VALUES
            ('alice', 'alice@example.com', 'hashed_password_1'),
            ('bob',   'bob@example.com',   'hashed_password_2');

        INSERT INTO expenses (user_id, title, amount, category, date, notes) VALUES
            (1, 'Grocery run',     45.50, 'Food',          '2026-04-01', 'Weekly groceries'),
            (1, 'Electric bill',  120.00, 'Utilities',     '2026-04-03', NULL),
            (1, 'Netflix',         15.99, 'Entertainment', '2026-04-05', 'Monthly subscription'),
            (2, 'Gym membership',  30.00, 'Health',        '2026-04-02', NULL),
            (2, 'Lunch',           12.75, 'Food',          '2026-04-06', 'Sandwich and coffee');
    """)
    conn.commit()
    conn.close()
