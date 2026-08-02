"""
app.py — a minimal Flask site showing the LISTING -> DETAIL pattern.

Four pages:
    /            the LISTING view — all 12 items, one wide row each
    /gallery     the GALLERY view — the same 12 items, tiled
    /item/<id>   the DETAIL page for one item
    /summary     a written article comparing the three CSS approaches

Run seed.py first to build the database, then:

    python app.py

and open http://127.0.0.1:5000
"""

import sqlite3
from flask import Flask, render_template, abort

app = Flask(__name__)

DB_FILE = "wireframe.db"

# --- Configuration -------------------------------------------------------
# The three demo sites run as three separate Flask apps, so they each need
# their own port. The summary page links between them, and those links have
# to be full URLs (http://127.0.0.1:5001/...) because Flask's url_for() only
# knows about routes inside THIS app.
#
# Keeping them in one dictionary here means there is exactly one place to
# edit if you change a port. Never scatter settings like this through your
# templates — you will miss one.
SITE_URLS = {
    "vanilla": "http://127.0.0.1:5000",
    "w3": "http://127.0.0.1:5001",
    "pico": "http://127.0.0.1:5002",
}

# Which of the three sites is THIS one? Used by the summary page to
# highlight the current site and skip linking to itself.
THIS_SITE = "vanilla"


def get_db():
    """Open a connection to the database.

    sqlite3.Row makes each result row behave like a dictionary, so in the
    templates we can write item.title instead of item[1]. Much easier to read.
    """
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def get_all_items():
    """Fetch every item, with its category name.

    The category NAME lives in the categories table, not the items table,
    so we JOIN the two tables together to get both in one query.

    This lives in its own function because BOTH the listing page and the
    gallery page need exactly the same data. Writing the query once means
    there is only one place to fix it if it is wrong.
    """
    connection = get_db()
    items = connection.execute(
        """
        SELECT  items.id,
                items.title,
                items.summary,
                items.image_id,
                categories.name AS category_name
        FROM    items
        JOIN    categories ON items.category_id = categories.id
        ORDER BY items.id
        """
    ).fetchall()
    connection.close()
    return items


@app.route("/")
def index():
    """Homepage: the LISTING view — one wide row per item."""
    return render_template("index.html", items=get_all_items())


@app.route("/gallery")
def gallery():
    """The GALLERY view — the same items, tiled in a grid.

    Note what is going on here: identical data, identical query, a different
    template. The listing and the gallery are two presentations of one set of
    records. Nothing about the database changes to support both.
    """
    return render_template("gallery.html", items=get_all_items())


@app.route("/summary")
def summary():
    """A written article comparing the three CSS approaches.

    This page uses NO database at all — it is hand-written content. Not every
    page on a site has to be driven by data, and it is worth noticing that
    this route is three lines long because of that.
    """
    return render_template(
        "summary.html",
        site_urls=SITE_URLS,
        this_site=THIS_SITE,
    )


@app.route("/item/<int:item_id>")
def detail(item_id):
    """Detail page: show ONE item, found by its id.

    The <int:item_id> part of the route captures the number from the URL
    and passes it into this function. So /item/5 gives item_id = 5.
    """
    connection = get_db()
    item = connection.execute(
        """
        SELECT  items.id,
                items.title,
                items.summary,
                items.body,
                items.image_id,
                categories.name AS category_name
        FROM    items
        JOIN    categories ON items.category_id = categories.id
        WHERE   items.id = ?
        """,
        (item_id,),          # the ? is filled in safely from this tuple
    ).fetchone()             # fetchone() because we expect a single row
    connection.close()

    # If someone types /item/999 there is no matching row, so item is None.
    if item is None:
        abort(404)

    return render_template("detail.html", item=item)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
