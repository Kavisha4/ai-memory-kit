"""
The Stale Polaroid demo: why "just add a vector DB" is not memory.

Zero dependencies, runs offline in under a second:
    python3 stale_polaroid.py

It stores a user's chat history as episodes, then answers "Where do I live?" with
four retrieval strategies:
  1. Semantic   - top-k by cosine similarity (toy bag-of-words embedding)
  2. Time-based - newest first
  3. Hybrid     - cosine + beta * 0.5^(age / half_life)
  4. Write-back - extract facts into a versioned table, supersede old values

Swap embed() for a real embedding model (OpenAI, Gemini, sentence-transformers) and
the stale fact still wins: the old message is longer and more similar to the question.
"""

import math
import re
import sqlite3
from collections import Counter
from datetime import date

TODAY = date(2026, 11, 20)

# (date, text) - what the user said over two years of chats
EPISODES = [
    ("2024-03-01", "I live in Delhi, near Connaught Place. I love where I live, the street food here is the best."),
    ("2024-06-11", "My son is allergic to peanuts, please never suggest peanut dishes."),
    ("2025-01-20", "Where I live in Delhi, winters are smoggy. I live with my family of four."),
    ("2025-08-02", "I'm vegetarian, I stopped eating meat this year."),
    ("2026-09-12", "We moved to Pune last week."),
    ("2026-11-19", "Can you book a team dinner for 6 tomorrow?"),
    ("2026-11-20", "I'm starving right now."),
]

QUESTION = "Where do I live?"

STOP = {"i", "a", "the", "to", "in", "is", "my", "me", "we", "of", "for", "do", "can", "you", "please", "this", "here", "with", "are", "last", "now", "right"}


# A real embedding model knows "moved to" is about where you live. Fake that here.
SYNONYMS = {"moved": "live", "relocated": "live", "stay": "live"}


def embed(text):
    """Toy embedding: bag of lowercase words plus synonyms. Enough to show the failure mode."""
    words = [w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP]
    return Counter(SYNONYMS.get(w, w) for w in words)


def cosine(a, b):
    dot = sum(a[w] * b[w] for w in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def age_days(d):
    return (TODAY - date.fromisoformat(d)).days


def show(title, rows, note):
    print(f"\n\033[1m{title}\033[0m")
    for score, d, text in rows:
        print(f"  {score:6.3f}  {d}  {text[:70]}")
    print(f"  \033[33m→ {note}\033[0m")


def semantic(k=3):
    q = embed(QUESTION)
    scored = sorted(((cosine(q, embed(t)), d, t) for d, t in EPISODES), reverse=True)
    return scored[:k]


def time_based(k=3):
    rows = sorted(EPISODES, key=lambda e: e[0], reverse=True)
    return [(0.0, d, t) for d, t in rows[:k]]


def hybrid(k=3, beta=0.5, half_life_days=180):
    q = embed(QUESTION)
    scored = []
    for d, t in EPISODES:
        score = cosine(q, embed(t)) + beta * 0.5 ** (age_days(d) / half_life_days)
        scored.append((score, d, t))
    return sorted(scored, reverse=True)[:k]


def write_back():
    """Extract facts with since/until, superseding instead of overwriting."""
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE facts (key TEXT, value TEXT, since TEXT, until TEXT, source TEXT)")

    def upsert(key, value, when, source):
        cur = db.execute("SELECT value FROM facts WHERE key=? AND until IS NULL", (key,)).fetchone()
        if cur and cur[0] == value:
            return
        db.execute("UPDATE facts SET until=? WHERE key=? AND until IS NULL", (when, key))
        db.execute("INSERT INTO facts VALUES (?,?,?,NULL,?)", (key, value, when, source))

    # In production a cheaper LLM does this extraction with structured output.
    # Here, a few regex rules stand in for it.
    for d, t in EPISODES:
        if m := re.search(r"(?:live in|moved to) (\w+)", t):
            upsert("city", m.group(1), d, t)
        if "vegetarian" in t:
            upsert("diet", "vegetarian", d, t)
        if "allergic to peanuts" in t:
            upsert("allergy (son)", "peanuts", d, t)

    print("\n\033[1m4. WRITE-BACK  facts table, superseded not deleted\033[0m")
    for key, value, since, until, _ in db.execute("SELECT * FROM facts ORDER BY key, since"):
        state = "current" if until is None else f"until {until}"
        print(f"  {key:15} {value:12} since {since}  {state}")
    city = db.execute("SELECT value FROM facts WHERE key='city' AND until IS NULL").fetchone()[0]
    print(f"  \033[32m→ Read path: SELECT value WHERE until IS NULL  ⇒  {city}\033[0m")
    print("  \033[32m→ History still answers 'Where did I live last year?' ⇒ Delhi\033[0m")


if __name__ == "__main__":
    print(f"Question: \033[1m{QUESTION}\033[0m   (truth: Pune)")
    show("1. SEMANTIC  top-k by cosine", semantic(),
         "Finds the Pune message, but ranks two stale Delhi messages above it.")
    show("2. TIME-BASED  newest first", time_based(),
         "Recent, but 'I'm starving' and the dinner booking crowd out the answer.")
    show("3. HYBRID  cosine + 0.5 * 0.5^(age/180d)", hybrid(),
         "Pune is now first, but both stale Delhi messages still go into the prompt.")
    write_back()
