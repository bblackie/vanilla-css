---
title: CSS Layouts Demo — Flask Listing to Detail
tags:
  - flask
  - sqlite
  - y12dgt
  - wireframe
created: 2026-08-02
---

# CSS Layouts Demo — Flask Listing to Detail

A wireframe Flask site demonstrating the **listing page → detail page** pattern
with a two-table SQLite database joined on a foreign key.

## Environment setup


```
python -m venv .venv
```

This creates a .venv folder inside the project. That folder contains a separate Python environment for this project.

Next, you activate it.
## Activate virtual environment

On Windows PowerShell:
```
.venv\Scripts\Activate.ps1
```
If the prompt changes to include (.venv), that is evidence that the environment is active.

NB: You might get an error here regarding running PowerShell scripts.  To resolve that run:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then you upgrade pip:
```
python -m pip install --upgrade pip
```
This matters because pip is the tool that installs Python packages. Using python -m pip is clearer than just typing pip, because it makes sure the package installer belongs to the currently selected Python interpreter.


## Running it

```bash
pip install flask
```
```bash
python seed.py     # builds wireframe.db — run this first, and only once
```
```bash
flask run --port 5000     # starts the server
```

Then open <http://127.0.0.1:5000>.

Re-run `python seed.py` any time you want to wipe and rebuild the database.

## Files

| File | What it does |
|---|---|
| `schema.sql` | Defines the two tables and the foreign key between them |
| `seed.py` | Builds `wireframe.db` and fills it with 4 categories and 12 items |
| `app.py` | The Flask app — two routes, two SQL queries |
| `templates/base.html` | The shared page shell (header, nav, footer) |
| `templates/index.html` | The listing page |
| `templates/detail.html` | The item detail page |
| `templates/404.html` | Shown when an item id doesn't exist |
| `static/style.css` | All the CSS, heavily commented |
| `wireframe.db` | Created by `seed.py` — not in the repo |

## The database

Two tables. Category names are stored **once**, in `categories`. Each item
stores only the *id number* of its category:

```
categories                items
----------                -----
id                        id
name       <--------------  category_id
slug                      title, summary, body, image_id
```

Why not just put the text "Lorem" in every item row? Because if you later
rename that category you'd have to edit every single item. Storing it once and
pointing at it means one edit. This is the core idea behind splitting data
across tables.

## The join query

The homepage needs the item data *and* the category name, which live in
different tables. `JOIN` stitches them together:

```sql
SELECT  items.id, items.title, items.summary, items.image_id,
        categories.name AS category_name
FROM    items
JOIN    categories ON items.category_id = categories.id
ORDER BY items.id
```

The `ON` clause is the important line: *match each item to the category whose
id equals that item's `category_id`*. The `AS category_name` gives the column a
clean name so the template can write `item.category_name`.

## The listing → detail link

Three pieces have to line up:

1. **The route** — `@app.route("/item/<int:item_id>")`. The `<int:item_id>`
   captures the number from the URL and passes it to the function.
2. **The query** — `WHERE items.id = ?` with `fetchone()`, because we want one
   row, not a list. The `?` placeholder is filled in by SQLite, which is what
   stops SQL injection. Never build a query with an f-string.
3. **The link** — `url_for('detail', item_id=item.id)` in the template. This
   generates `/item/5`. Use `url_for` rather than typing `/item/5` by hand, so
   the links still work if you change the route later.

If someone visits `/item/999`, `fetchone()` returns `None` and `abort(404)`
sends them to `404.html`. Always handle this — it is a common marking point.

## Placeholder content

- **Text**: lorem ipsum, stored in the database like real content would be.
- **Images**: [Lorem Picsum](https://picsum.photos). The URL format is
  `https://picsum.photos/id/<photo>/<width>/<height>`. Using `/id/<photo>/`
  pins each item to the *same* photo every reload, instead of a random one.
  Note the listing requests `240/160` and the detail page requests `1200/600`
  from the same `image_id` — small thumbnail, large hero image.

## The gallery page — one query, two views

`/gallery` shows the **same 12 records** as the homepage. Same query, same
data, different template. This is the point worth labouring:

```python
def get_all_items():
    ...the JOIN query, written once...

@app.route("/")
def index():
    return render_template("index.html", items=get_all_items())

@app.route("/gallery")
def gallery():
    return render_template("gallery.html", items=get_all_items())
```

The query lives in its own function so it exists in **one** place. If you
copy-paste it into both routes and later find a bug, you have to remember to
fix it twice. You won't.

Your database does not need to know whether the user is looking at a listing
or a gallery. That is a presentation decision, made in the template.

### Flexbox or Grid?

The two pages use different layout tools on purpose:

- **Listing** uses **flexbox** — each row is one-dimensional: image, then text,
  side by side.
- **Gallery** uses **CSS Grid** — tiles are two-dimensional: they wrap into
  rows *and* columns.

Rough rule: flexbox for a *line* of things, grid for a *grid* of things.

The whole gallery layout is one line:

```css
grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
```

Read it as "as many equal columns as will fit, each at least 240px wide."
The browser works out the column count, so one column on a phone and four on
a laptop — with **no media query at all**. Resize the window and watch it
reflow.

### Tiles are one big link

The entire tile is wrapped in a single `<a>`, so the image and the caption are
both clickable. That's a far bigger target than a small "view details" button,
which matters a lot on a phone.

## Things to try

- Add a `/category/<slug>` route that lists only items in one category.
- Change `minmax(240px, 1fr)` to `minmax(160px, 1fr)` and resize the window.
- Swap `auto-fill` for `auto-fit` and resize with only 2–3 items showing.
  `auto-fill` keeps empty columns, `auto-fit` collapses them.
- Add a `price` or `date` column and sort the listing by it.
