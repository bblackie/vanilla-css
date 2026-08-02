-- schema.sql
-- Defines the structure of the database. Run by seed.py.
-- Two tables, linked by a foreign key. This is the "one to many"
-- relationship: ONE category has MANY items.

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS categories;

-- The "lookup" table. Each category is stored ONCE, here.
CREATE TABLE categories (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL UNIQUE,
    slug  TEXT NOT NULL UNIQUE
);

-- The main table. Each item points at a category by its id number,
-- NOT by repeating the category name as text.
CREATE TABLE items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT    NOT NULL,
    summary       TEXT    NOT NULL,   -- short text, shown on the homepage
    body          TEXT    NOT NULL,   -- long text, shown on the detail page
    image_id      INTEGER NOT NULL,   -- which Lorem Picsum photo to use
    category_id   INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
