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
      font-family: 'Arial', sans-serif;
    }
    .container { max-width: 100%; }
    .date { text-align: center; margin: 0; font-size: 1em; }
    h1 {
      text-align: center;
      color: #4CAF50;
      margin: 5px 0;
      font-size: 2rem;
    }
    h2 {
      color: #4CAF50;
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
      color: #4CAF50;
      font-weight: 700;
      position: absolute;
      left: 10px;
    }
    .rating {
      color: #4CAF50;
      margin-left: 4px;
      font-weight: 700;
    }
    .rating-info-trigger {
      cursor: help;
      color: #4CAF50;
      text-align: center;
      user-select: none;
      border: 2px solid #4CAF50;
      border-radius: 50%;
      width: 1.1em;
      height: 1.1em;
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
      border: 2px solid #4CAF50;
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
      color: #4CAF50;
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
    .ytlink {
      display: inline-block;
      width: 1.3em;
      height: 1.3em;
      background-image: url(data:image/png;base64,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);
      background-size: contain;
      background-repeat: no-repeat;
      vertical-align: text-top;
    }   
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
            <p><strong>2/5</strong> – disappointing – won't listen again</p>
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
                        f'<a href="{row["Youtube"]}" target="_blank" rel="noopener" class="ytlink"></a>',
                        "<b>",
                        row["Artist"],
                        "</b> – <i>",
                        row["Album"],
                        '</i><span class="rating">(',
                        row["Rating"],
                        '/5)</span><span class="genre">',
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
