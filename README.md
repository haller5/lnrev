# Untitled — reading log

A static site. No build tools, no server, no database — just HTML, CSS,
and one Python script that generates the HTML from a single data file.

## How to add a new review

1. Open **`reviews.json`**.
2. Copy one of the existing entries in the `"reviews"` array and fill in
   your own fields:

   ```json
   {
     "slug": "some-short-id",       // used in the URL, no spaces
     "featured": false,             // true = the big "currently reading" post
     "type": "ln",                  // "ln", "anime", or "book"
     "title": "Series Title",
     "jp_sub": "Romanized title",   // optional, leave "" to skip
     "meta": "vol. 2",              // shows next to the category tag
     "date": "oct 2026",
     "cover": "images/some-short-id.jpg",  // optional, see below
     "quote": "One-line verdict.",
     "review_notes": ["spoilers — mild"],  // optional, [] to skip
     "para1": "Opening paragraph.",
     "thoughts": "The rest of the review, under a 'Thoughts' heading.",
     "rating": "4/5",
     "like": ["thing one", "thing two"],
     "dislike": ["thing you didn't like"]
   }
   ```

3. If you have cover art, drop the image file into the **`images/`**
   folder and point `"cover"` at it (e.g. `"images/some-short-id.jpg"`).
   If you leave `"cover"` as `""`, the page falls back to the usual
   colored gradient for that category — nothing breaks either way.
4. Run the generator from a terminal in this folder:

   ```
   python3 build.py
   ```

   This rewrites `index.html` and every page in `articles/` from
   scratch based on `reviews.json`. It's safe to run as many times as
   you want.
5. Open `index.html` in a browser to check it, then commit and push
   (see below).

To change what's "currently reading," move `"featured": true` to a
different entry (only one entry should have it at a time) and re-run
`build.py`.

To edit the **Upcoming Reads** / **In the Future** sidebar lists, or
the site title/tagline/footer/author name, edit the `"reading_list"`
and `"site"` sections near the top of `reviews.json`.

## Everything image-related is driven by reviews.json / the site block

- Each review's `"cover"` field controls **three** things at once: the
  big cover on its article page, the small stacked thumbnail next to
  its title in the shelf list, and the image shown in the hover-preview
  pane on the right of the homepage. Set it once, it shows up
  everywhere that review appears.
- `site.banner` is the homepage header image.
- `site.avatar` is the byline photo shown on every review.
- `site.author` is the name shown next to that avatar.

Any of these left blank (or pointing at a file that doesn't exist)
falls back automatically to the plain color/gradient look — nothing
breaks, it just looks like it does today until you add real images.

## What NOT to hand-edit

`index.html` and everything inside `articles/` are generated —
editing them directly works until the next time you run `build.py`,
which overwrites them. Put content changes in `reviews.json` instead.
`style.css` and `script.js` are hand-written and safe to edit directly;
`build.py` never touches them.

## Adding cover images

Just drop `.jpg`/`.png` files into `images/` and reference them from
`reviews.json`. There's no resizing step, so images somewhere around
600–900px on the long edge will keep the site loading quickly — bigger
files still work, just slower to load.

## Hosting it on GitHub Pages

One-time setup:

1. Create a new repository on GitHub (public — Pages needs that on a
   free account).
2. From inside this folder:

   ```
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

3. On GitHub, go to the repo's **Settings → Pages**.
4. Under "Build and deployment," set **Source** to "Deploy from a
   branch," pick the **main** branch and the **/ (root)** folder, then
   save.
5. GitHub gives you a URL — usually
   `https://<your-username>.github.io/<repo-name>/` — live within a
   minute or two.

From then on, publishing an update is just:

```
python3 build.py
git add .
git commit -m "Add review: <title>"
git push
```

GitHub Pages picks up the new commit automatically and redeploys.
