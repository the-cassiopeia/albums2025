import csv
import sys

import minify_html

HTML_START = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta content="width=device-width,initial-scale=1.0" name="viewport">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Source+Sans+3&display=swap">
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3&display=swap" rel="stylesheet">
  <title>Album Ratings</title>
  <style>
    body {
      color: #EDEDED;
      background: #161616;
      width: 590px;
      margin: 0 auto;
      padding: 0;
      font-family: 'Source Sans 3', sans-serif;
    }
    .container { max-width: 100%; }
    h2 {
      color: #5cb85c;
      font-size: 1.2rem;
      margin: 0;
    }
    .album-list {
      counter-reset: album-counter;
      display: flex;
      flex-direction: column;
      padding: 0;
      list-style: none;
    }
    .album-list li {
      counter-increment: album-counter;
      border-radius: 6px;
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 3px 10px 3px 42px;
      font-size: 1rem;
      position: relative;
    }
    .album-list li:hover {
      background: #2d2d2d;
      box-shadow: 0 0 12px rgba(45, 45, 45, 0.9);
    }
    .album-list li::before {
      content: counter(album-counter) ".";
      color: #5cb85c;
      font-weight: bold;
      position: absolute;
      left: 10px;
    }
    .rating {
      color: #5cb85c;
      margin-left: 6px;
      font-weight: bold;
    }
    .rating-info-trigger {
      cursor: help;
      color: #EDEDED;
      background: #5cb85c;
      user-select: none;
      border: none;
      border-radius: 50%;
      width: 1.1em;
      height: 1.1em;
      margin-left: 8px;
      font-size: .95em;
      font-weight: bold;
      line-height: 1.1em;
      display: inline-flex;
      justify-content: center;
      align-items: center;
      position: relative;
    }
    .rating-tooltip {
      color: #ededed;
      z-index: 100;
      text-align: left;
      background: #2d2d2d77;
      backdrop-filter: blur(15px);
      border: 1px solid rgba(85, 85, 85, 0.3);
      border-radius: 6px;
      width: 320px;
      padding: 5px 10px;
      display: none;
      position: absolute;
      top: 125%;
      left: 50%;
      transform: translate(-50%);
    }
    .rating-tooltip p {
      margin: 5px 0;
    }
    .rating-tooltip p strong {
      color: #5cb85c;
    }
    .rating-info-trigger:is(:hover, :focus, :focus-within) .rating-tooltip {
      display: block;
    }
    .genre {
      color: #888;
      margin-left: auto;
      font-size: .8rem;
      font-style: italic;
    }
    .YT {
      display: inline-block;
      width: 1.3em;
      height: 1.3em;
      background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+PGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzAiIGZpbGw9IiNjZDFjMWMiLz48cG9seWdvbiBwb2ludHM9IjIyLDE2IDQ4LDMyIDIyLDQ4IiBmaWxsPSIjZmZmIi8+PC9zdmc+) 0 0 / contain no-repeat;
      vertical-align: text-top;
    }
    .YT:hover {
      filter: brightness(1.2);
      transform: scale(1.2);
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
      color: #EDEDED;
      background: #2d2d2d;
      border: 0;
      border-radius: 6px;
      width: 125px;
      padding: 6px 10px;
      font-size: .85rem;
      font-style: italic;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="filter-container">
      <h2>
        2025 Album Ranking
        <span class="rating-info-trigger" id="ratingInfoTrigger" role="tooltip" tabindex="0">
          ?
          <div class="rating-tooltip" id="ratingTooltip">
            <p><strong>Rating Scheme</strong></p>
            <p><strong>5/5</strong> - amazing - AOTY contender</p>
            <p><strong>4/5</strong> - great - very memorable</p>
            <p><strong>3/5</strong> - pretty good - would listen again</p>
            <p><strong>2/5</strong> - not for me - won't listen again</p>
            <p><strong>1/5</strong> - bad - has major issues</p>
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
    document.querySelectorAll('a.YT').forEach(link => {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener');
    });

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
                assert row["Artist"].strip() is not None
                assert row["Album"].strip() is not None
                assert row["Rating"].strip() is not None
                assert 1 <= float(row["Rating"].strip()) <= 5
                assert row["Genre"].strip() is not None
                assert row["Youtube"].strip() is not None
                assert (
                    row["Youtube"].strip().startswith("https://www.youtube.com/watch?v=")
                )
                assert row["Youtube"] not in all_youtubes
            except (AssertionError, ValueError):
                print("Error while parsing the following row:")
                print(row)
                sys.exit(1)

            all_youtubes.add(row["Youtube"])
            ytb_shortened = "https://youtu.be/" + row["Youtube"].strip().removeprefix(
                "https://www.youtube.com/watch?v="
            )

            HTML_ALBUMS.append(
                "".join(
                    [
                        f'      <li><a href="{ytb_shortened}" class="YT"></a><b>',
                        row["Artist"].strip(),
                        "</b> - <i>",
                        row["Album"].strip(),
                        '</i><span class="rating">',
                        row["Rating"].strip(),
                        '/5</span><span class="genre">',
                        row["Genre"].strip(),
                        "</span></li>",
                    ]
                )
            )

    html_minified = minify_html.minify(
        HTML_START + "\n".join(HTML_ALBUMS) + HTML_END,
        minify_js=True,
        minify_css=True,
        minify_doctype=True,
        remove_processing_instructions=True,
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_minified)


if __name__ == "__main__":
    main()
