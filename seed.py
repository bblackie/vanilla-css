"""
seed.py — builds wireframe.db from scratch.

Run this ONCE before starting the app:

    python seed.py

Running it again wipes the database and rebuilds it, which is handy
while you are still changing the schema.
"""

import sqlite3
import os

DB_FILE = "wireframe.db"
SCHEMA_FILE = "schema.sql"

# --- The categories -------------------------------------------------------
# (name, slug)
CATEGORIES = [
    ("Lorem", "lorem"),
    ("Ipsum", "ipsum"),
    ("Dolor", "dolor"),
    ("Amet", "amet"),
]

# --- The 12 items ---------------------------------------------------------
# (title, summary, body, image_id, category_id)
# category_id refers to the ORDER of the list above: Lorem=1, Ipsum=2, etc.

LONG_BODY = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "
    "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
    "commodo consequat.\n\n"
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum "
    "dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non "
    "proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n\n"
    "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam "
    "varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus "
    "magna felis sollicitudin mauris. Integer in mauris eu nibh euismod "
    "gravida."
)

SHORT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor."

ITEMS = [
    ("Lorem Ipsum Dolor",        SHORT, LONG_BODY, 1011, 1),
    ("Consectetur Adipiscing",   SHORT, LONG_BODY, 1015, 2),
    ("Sed Do Eiusmod",           SHORT, LONG_BODY, 1016, 3),
    ("Tempor Incididunt",        SHORT, LONG_BODY, 1018, 4),
    ("Ut Labore Et Dolore",      SHORT, LONG_BODY, 1021, 1),
    ("Magna Aliqua Enim",        SHORT, LONG_BODY, 1024, 2),
    ("Ad Minim Veniam",          SHORT, LONG_BODY, 1025, 3),
    ("Quis Nostrud Exercit",     SHORT, LONG_BODY, 1027, 4),
    ("Ullamco Laboris Nisi",     SHORT, LONG_BODY, 1033, 1),
    ("Aliquip Ex Ea Commodo",    SHORT, LONG_BODY, 1039, 2),
    ("Duis Aute Irure",          SHORT, LONG_BODY, 1043, 3),
    ("Reprehenderit Voluptate",  SHORT, LONG_BODY, 1044, 4),
]


def main():
    # Start clean so re-running always gives the same result.
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed old {DB_FILE}")

    connection = sqlite3.connect(DB_FILE)

    # Build the tables by running everything in schema.sql
    with open(SCHEMA_FILE) as f:
        connection.executescript(f.read())
    print("Created tables from schema.sql")

    # Insert the categories first — items need their ids to exist.
    connection.executemany(
        "INSERT INTO categories (name, slug) VALUES (?, ?)",
        CATEGORIES,
    )
    print(f"Inserted {len(CATEGORIES)} categories")

    connection.executemany(
        """INSERT INTO items (title, summary, body, image_id, category_id)
           VALUES (?, ?, ?, ?, ?)""",
        ITEMS,
    )
    print(f"Inserted {len(ITEMS)} items")

    connection.commit()
    connection.close()
    print(f"\nDone. {DB_FILE} is ready. Now run: python app.py")


if __name__ == "__main__":
    main()
