import csv
import datetime
import sys

import minify_html

FORMATTED_DATE = datetime.datetime.now().strftime("%B %d, %Y")

HTML_START = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta content="width=device-width,initial-scale=1.0" name="viewport">
  <title>Album Ratings</title>
  <style>
    body {
      color: #e5e5e5;
      background-color: #111;
      width: 660px;
      margin: 0 auto;
      padding: 0;
      font-family: 'Segoe UI', sans-serif;
    }
    .container { max-width: 100%; }
    .date { text-align: center; margin: 0; font-size: 1em; }
    h1 {
      text-align: center;
      color: #538146;
      margin: 5px 0;
      font-size: 2rem;
    }
    h2 {
      color: #538146;
      font-size: 1.2rem;
      margin: 0;
    }
    .album-list {
      counter-reset: album-counter;
      display: flex;
      flex-direction: column;
      gap: 0;
      padding: 0;
      list-style: none;
    }
    .album-list li {
      counter-increment: album-counter;
      background: #1e1e1e;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 3px 10px 3px 45px;
      font-size: 1rem;
      position: relative;
    }
    .album-list li::before {
      content: counter(album-counter) ".";
      color: #538146;
      font-weight: 700;
      position: absolute;
      left: 10px;
    }
    .rating {
      color: #538146;
      margin-left: 8px;
      font-weight: 700;
    }
    .rating-info-trigger {
      cursor: help;
      color: #538146;
      text-align: center;
      user-select: none;
      border: 2px solid #538146;
      border-radius: 50%;
      width: 1.2em;
      height: 1.2em;
      margin-left: 8px;
      font-size: .95em;
      font-weight: 700;
      line-height: 1.1em;
      display: inline-block;
      position: relative;
    }
    .rating-tooltip {
      display: none;
      position: absolute;
      top: 125%;
      left: 50%;
      transform: translate(-50%);
      background: #2a2a2a;
      color: #e5e5e5;
      border: 2px solid #538146;
      border-radius: 8px;
      width: 320px;
      padding: 3px 10px;
      font-size: 1rem;
      font-weight: 400;
      z-index: 100;
      text-align: left;
    }
    .rating-tooltip p {
      margin: 5px 0;
    }
    .rating-tooltip p strong {
      color: #538146;
    }
    .rating-info-trigger:hover .rating-tooltip,
    .rating-info-trigger:focus .rating-tooltip,
    .rating-info-trigger:focus-within .rating-tooltip {
      display: block;
    }
    .genre {
      color: #888;
      margin-left: auto;
      font-size: .9rem;
      font-style: italic;
    }
    .icon-link { display: inline-block; }
    .icon { vertical-align: text-top; height: 1.3em; }
    .filter-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 15px 0;
    }
    .genre-search-input {
      text-align: center;
      box-sizing: border-box;
      color: #e5e5e5;
      background: #1e1e1e;
      border: 0 solid #444;
      border-radius: 20px;
      width: 150px;
      padding: 6px 10px;
      font-size: .9rem;
      font-style: italic;
    }
  </style>
</head>
"""

HTML_BODY = f"""
<body>
  <div class="container">
    <h1>Albums 2025</h1>
    <p class="date">Last updated: {FORMATTED_DATE}</p>
    <div class="filter-container">
      <h2>
        Personal Album Ranking
        <span class="rating-info-trigger" id="ratingInfoTrigger" role="tooltip" tabindex="0">
          ?
          <div class="rating-tooltip" id="ratingTooltip">
            <p><strong>Rating Scheme</strong></p>
            <p><strong>5/5</strong> – amazing – AOTY contender</p>
            <p><strong>4/5</strong> – great – very memorable</p>
            <p><strong>3/5</strong> – pretty good – would listen again</p>
            <p><strong>2/5</strong> – disappointing – won’t listen again</p>
            <p><strong>1/5</strong> – bad – has major issues</p>
          </div>
        </span>
      </h2>
      <input type="text" placeholder="filter by genre" class="genre-search-input" id="genreSearch" onkeyup="filterByGenre()" />
    </div>
    <ol class="album-list">
"""


HTML_END = """
    </ol>
  </div>
  <script defer>
    const genreSearchInput = document.getElementById('genreSearch');
    const ratingInfoTrigger = document.getElementById('ratingInfoTrigger');
    let albumData = [];

    function initializeAlbumData() {
      albumData = Array.from(document.querySelectorAll('.album-list li')).map(li => ({
        element: li,
        genreText: li.querySelector('.genre')?.textContent.toLowerCase() || ''
      }));
    }

    function filterByGenre() {
      if (!albumData.length) initializeAlbumData();
      const filter = genreSearchInput.value.toLowerCase();
      albumData.forEach(({ element, genreText }) => {
        element.style.display = genreText.includes(filter) ? 'flex' : 'none';
      });
    }

    initializeAlbumData();

    document.addEventListener('click', e => {
      if (!ratingInfoTrigger.contains(e.target)) ratingInfoTrigger.blur();
    });
  </script>
</body>
</html>
"""


def main():

    HTML_ALBUMS = []

    all_youtubes = set()

    with open("albums.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                assert len(row) == 5
                assert row["Artist"] is not None
                assert row["Album"] is not None
                assert row["Rating"] is not None
                assert 1 <= float(row["Rating"]) <= 5
                assert row["Genre"] is not None
                assert row["Youtube"] is not None
                assert row["Youtube"].startswith("https://www.youtube.com/watch?v=")
                assert row["Youtube"] not in all_youtubes
            except (AssertionError, ValueError):
                print("Error while parsing the following row:")
                print(row)
                sys.exit(1)

            all_youtubes.add(row["Youtube"])

            HTML_ALBUMS.append(
                "".join(
                    [
                        "      <li>",
                        f'<a href="{row["Youtube"]}" target="_blank" rel="noopener noreferrer" class="icon-link"><img class="icon" src="youtube.png"></a>',
                        "<strong>",
                        row["Artist"],
                        "</strong> – <em>",
                        row["Album"],
                        '</em> <span class="rating">(',
                        row["Rating"],
                        '/5)</span> <span class="genre">',
                        row["Genre"],
                        "</span></li>",
                    ]
                )
            )

    html_minified = minify_html.minify(
        HTML_START + HTML_BODY + "\n".join(HTML_ALBUMS) + HTML_END,
        minify_js=True,
        minify_css=True,
        minify_doctype=True,
        remove_processing_instructions=True,
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_minified)


if __name__ == "__main__":
    main()
