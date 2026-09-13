#!/usr/bin/env python3
"""
Site generator for the Untitled review site.

Usage:
    python3 build.py

Reads everything from reviews.json and (re)writes index.html and every
page in articles/. style.css and script.js are hand-maintained, not
generated. Add a new review by editing reviews.json (and optionally
dropping a cover image in images/), then re-run this script.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(ROOT, "articles")

TYPE_LABELS = {
    "ln": {"tag": "LN", "label": "light novel"},
    "anime": {"tag": "ANIME", "label": "anime"},
    "book": {"tag": "BOOK", "label": "english novel"},
}

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700'
    '&family=Noto+Sans+JP:wght@400;500;700&family=Inter:wght@400;500;600'
    '&display=swap" rel="stylesheet">'
)


def li_list(items):
    return "".join(f"<li>{x}</li>" for x in items)


def review_notes_html(items):
    if not items:
        return ""
    return f'<ul class="review-notes">{li_list(items)}</ul>'


def jp_sub_html(text):
    if not text:
        return ""
    return f'<p class="jp-sub">{text}</p>'


def _resolved_url(path, prefix):
    """Returns prefix+path if path is set and the file exists on disk,
    otherwise None. Every image-driving helper below goes through this
    so a missing/blank field always falls back cleanly to the CSS
    default (gradient or solid fill) instead of a broken image."""
    if not path:
        return None
    if not os.path.isfile(os.path.join(ROOT, path)):
        return None
    return prefix + path


def bg_image_attr(path, prefix, extra_css=""):
    """Inline style="background-image:url(...)" attribute, or "" if the
    image is missing (CSS fallback takes over)."""
    url = _resolved_url(path, prefix)
    if not url:
        return ""
    return f" style=\"background-image:url('{url}');{extra_css}\""


def cover_attr(entry, image_prefix):
    return bg_image_attr(
        entry.get("cover"), image_prefix,
        " background-size:cover; background-position:center;"
    )


def stack_card_style(entry, image_prefix):
    """Same helper as cover_attr, used for the three thumb-stack /
    preview-stack cards — same cover image on all three."""
    return cover_attr(entry, image_prefix)


def cover_url_or_empty(entry, image_prefix):
    """Resolved cover URL (or '') for the data-cover attribute that
    script.js reads to fill the hover-preview pane."""
    return _resolved_url(entry.get("cover"), image_prefix) or ""


def render_avatar(site, image_prefix):
    attr = bg_image_attr(site.get("avatar"), image_prefix)
    return f'<div class="avatar"{attr}></div>'


def render_banner(site, image_prefix):
    attr = bg_image_attr(site.get("banner"), image_prefix)
    return f'<div class="banner"{attr}></div>'


def render_sidebar(data, index_href):
    featured = next(r for r in data["reviews"] if r.get("featured"))
    rl = data["reading_list"]
    upcoming = li_list(rl.get("upcoming", []))
    future = li_list(rl.get("future", []))
    return f"""    <aside class="sidebar">
      <div class="widget highlight">
        <h3>Currently Reading</h3>
        <ul><li>{featured['title']} — {featured['meta']}</li></ul>
      </div>
      <div class="widget">
        <h3>Upcoming Reads</h3>
        <ul>{upcoming}</ul>
      </div>
      <div class="widget">
        <h3>In the Future</h3>
        <ul>{future}</ul>
      </div>
      <div class="widget">
        <h3>Categories</h3>
        <ul>
          <li><a href="{index_href}">[LIGHT NOVEL]</a></li>
          <li><a href="{index_href}">[ANIME]</a></li>
          <li><a href="{index_href}">[BOOK]</a></li>
          <li><a href="{index_href}">[REVIEW]</a></li>
        </ul>
      </div>
    </aside>"""


def render_article_body(entry, site, image_prefix, link_prefix, css_class, eyebrow, show_read_more):
    t = TYPE_LABELS[entry["type"]]
    read_more = (
        f'\n            <a class="read-more" href="{link_prefix}articles/{entry["slug"]}.html">read more</a>'
        if show_read_more else ""
    )
    return f"""      <article class="{css_class}">
        <div class="topline">
          <span>{eyebrow}</span>
          <span class="tag">[{t['tag']}]</span>
        </div>
        <h2>{entry['title']}</h2>
        {jp_sub_html(entry.get('jp_sub'))}
        <p class="quote">{entry['quote']}</p>
        <div class="cover" data-type="{entry['type']}"{cover_attr(entry, image_prefix)}></div>
        <div class="post-body">
          <div class="byline" data-type="{entry['type']}">
            {render_avatar(site, image_prefix)}
            <p class="author">{site['author']}</p>
            <p class="date">{entry['date']}</p>
            <span class="tag">[{t['tag']}]</span>
            <span class="tag">[REVIEW]</span>
          </div>
          <div class="body-text">
            {review_notes_html(entry.get('review_notes'))}
            <p>{entry['para1']}</p>
            <h4>Thoughts</h4>
            <p>{entry['thoughts']}</p>
            <p class="rating">final rating: {entry['rating']}</p>
            <div class="like-lists">
              <p>what I like</p>
              <ul>{li_list(entry['like'])}</ul>
              <p>what I don't like</p>
              <ul>{li_list(entry['dislike'])}</ul>
            </div>{read_more}
          </div>
        </div>
      </article>"""


def render_shelf_row(entry, image_prefix):
    t = TYPE_LABELS[entry["type"]]
    card_style = stack_card_style(entry, image_prefix)
    data_cover = cover_url_or_empty(entry, image_prefix)
    return f"""      <details class="shelf-row-wrap">
        <summary class="shelf-row" data-type="{entry['type']}" data-cover="{data_cover}">
          <div class="thumb-stack" data-type="{entry['type']}">
            <div class="tcard t3"{card_style}></div>
            <div class="tcard t2"{card_style}></div>
            <div class="tcard t1"{card_style}></div>
          </div>
          <span class="title">{entry['title']}</span>
          <span class="dots"></span>
          <span class="tag">[{t['tag']}] {entry['meta']}</span>
        </summary>
        <div class="shelf-detail">
          <p class="rating">final rating: {entry['rating']}</p>
          <p>{entry['para1']}</p>
          <a class="read-more" href="articles/{entry['slug']}.html">read more</a>
        </div>
      </details>"""


def build_index(data):
    site = data["site"]
    featured = next(r for r in data["reviews"] if r.get("featured"))
    shelf = [r for r in data["reviews"] if not r.get("featured")]

    shelf_rows = "\n".join(render_shelf_row(r, image_prefix="") for r in shelf)
    featured_html = render_article_body(
        featured, site, image_prefix="", link_prefix="",
        css_class="featured", eyebrow=f"currently reading / {featured['meta']}",
        show_read_more=True,
    )
    sidebar_html = render_sidebar(data, index_href="#")
    banner_html = render_banner(site, image_prefix="")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{site['title']}</title>
{FONT_LINK}
<link rel="stylesheet" href="style.css">
</head>
<body>

  <header class="site-header">
    <h1><a href="index.html">{site['title'].upper()}</a></h1>
    <p class="tagline">{site['tagline']}</p>
    <nav>
      <a href="index.html" class="active">[HOME]</a>
      <a href="#">[ABOUT]</a>
    </nav>
  </header>

  {banner_html}

  <div class="layout">
    <div class="main-col">

{featured_html}

      <p class="shelf-label">the shelf</p>
      <div class="shelf-wrap">
        <div class="shelf-index" id="shelf-index">
{shelf_rows}
        </div>
        <div class="shelf-preview">
          <div class="preview-stack" id="preview-stack">
            <div class="pcard p3"></div>
            <div class="pcard p2"></div>
            <div class="pcard p1"></div>
          </div>
          <p class="preview-title" id="preview-title"></p>
          <p class="preview-meta" id="preview-meta"></p>
          <p class="hint" id="preview-hint">hover a title</p>
        </div>
      </div>

    </div>

{sidebar_html}
  </div>

  <footer class="site-footer">{site['footer']}</footer>

<script src="script.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote index.html")


def build_article(entry, data):
    site = data["site"]
    is_featured = entry.get("featured", False)

    eyebrow = (
        f"currently reading / {entry['meta']}" if is_featured
        else f"{TYPE_LABELS[entry['type']]['label']} / {entry['meta']}"
    )
    article_html = render_article_body(
        entry, site, image_prefix="../", link_prefix="../",
        css_class="post", eyebrow=eyebrow,
        show_read_more=False,  # already on this review's own page
    )

    sidebar_html = render_sidebar(data, index_href="../index.html")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{entry['title']} — {site['title']}</title>
{FONT_LINK}
<link rel="stylesheet" href="../style.css">
</head>
<body>

  <header class="site-header">
    <h1><a href="../index.html">{site['title'].upper()}</a></h1>
    <p class="tagline">{site['tagline']}</p>
    <nav>
      <a href="../index.html">[HOME]</a>
      <a href="#">[ABOUT]</a>
    </nav>
  </header>

  <div class="layout article-layout">
    <div class="main-col">
      <a class="back-link" href="../index.html">← back to the shelf</a>

{article_html}
    </div>

{sidebar_html}
  </div>

  <footer class="site-footer">{site['footer']}</footer>

</body>
</html>
"""
    path = os.path.join(ARTICLES_DIR, f"{entry['slug']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote articles/" + entry["slug"] + ".html")


def main():
    with open(os.path.join(ROOT, "reviews.json"), encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(ARTICLES_DIR, exist_ok=True)
    build_index(data)
    for entry in data["reviews"]:
        build_article(entry, data)

    print(f"\nDone — {len(data['reviews'])} article page(s) + index.html")


if __name__ == "__main__":
    main()
