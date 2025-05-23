import csv
import sys

import minify_html

HTML_START = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta content="width=device-width,initial-scale=1.0" name="viewport">
  <title>Album Ratings</title>
  <style>
    body {
      color: #EDEDED;
      background: #111;
      width: 660px;
      margin: 0 auto;
      padding: 0;
      font-family: 'Arial', sans-serif;
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
      gap: 3px;
      padding: 0;
      list-style: none;
    }
    .album-list li {
      counter-increment: album-counter;
      background: #1d1d1d;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 3px 10px 3px 45px;
      font-size: 1rem;
      position: relative;
    }
    .album-list li:hover {
      background: #2a2a2a;
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
      background: rgba(42, 42, 42, 0.65);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(85, 85, 85, 0.3);
      border-radius: 12px;
      width: 320px;
      padding: 5px 10px;
      font-size: 1rem;
      font-weight: 400;
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
      font-size: .9rem;
      font-style: italic;
    }
    .ytl {
      display: inline-block;
      width: 1.3em;
      height: 1.3em;
      background: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgd2lkdGg9IjY0IgogICBoZWlnaHQ9IjY0IgogICB2aWV3Qm94PSIwIDAgNjQgNjQiCiAgIHZlcnNpb249IjEuMSIKICAgaWQ9InN2ZzEiCiAgIHNvZGlwb2RpOmRvY25hbWU9InlvdXR1YmUtcm91bmQtaWNvbi1vcmlnaW5hbC5zdmciCiAgIGlua3NjYXBlOnZlcnNpb249IjEuNC4yIChmNDMyN2Y0LCAyMDI1LTA1LTEzKSIKICAgeG1sbnM6aW5rc2NhcGU9Imh0dHA6Ly93d3cuaW5rc2NhcGUub3JnL25hbWVzcGFjZXMvaW5rc2NhcGUiCiAgIHhtbG5zOnNvZGlwb2RpPSJodHRwOi8vc29kaXBvZGkuc291cmNlZm9yZ2UubmV0L0RURC9zb2RpcG9kaS0wLmR0ZCIKICAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogICB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8ZGVmcwogICAgIGlkPSJkZWZzMSIgLz4KICA8c29kaXBvZGk6bmFtZWR2aWV3CiAgICAgaWQ9Im5hbWVkdmlldzEiCiAgICAgcGFnZWNvbG9yPSIjZmZmZmZmIgogICAgIGJvcmRlcmNvbG9yPSIjMDAwMDAwIgogICAgIGJvcmRlcm9wYWNpdHk9IjAuMjUiCiAgICAgaW5rc2NhcGU6c2hvd3BhZ2VzaGFkb3c9IjIiCiAgICAgaW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAuMCIKICAgICBpbmtzY2FwZTpwYWdlY2hlY2tlcmJvYXJkPSIwIgogICAgIGlua3NjYXBlOmRlc2tjb2xvcj0iI2QxZDFkMSIKICAgICBpbmtzY2FwZTp6b29tPSI5LjQzNzUiCiAgICAgaW5rc2NhcGU6Y3g9IjExLjYwMjY0OSIKICAgICBpbmtzY2FwZTpjeT0iOS41MzY0MjM4IgogICAgIGlua3NjYXBlOndpbmRvdy13aWR0aD0iMjU2MCIKICAgICBpbmtzY2FwZTp3aW5kb3ctaGVpZ2h0PSIxNDE3IgogICAgIGlua3NjYXBlOndpbmRvdy14PSIyNTUyIgogICAgIGlua3NjYXBlOndpbmRvdy15PSItOCIKICAgICBpbmtzY2FwZTp3aW5kb3ctbWF4aW1pemVkPSIxIgogICAgIGlua3NjYXBlOmN1cnJlbnQtbGF5ZXI9InN2ZzEiIC8+CiAgPGNpcmNsZQogICAgIGN4PSIzMiIKICAgICBjeT0iMzIiCiAgICAgcj0iMzAiCiAgICAgZmlsbD0iI2U0MzUzNSIKICAgICBpZD0iY2lyY2xlMSIKICAgICBzdHlsZT0iZmlsbC1ydWxlOmV2ZW5vZGQ7ZmlsbDojY2QxYzFjO2ZpbGwtb3BhY2l0eToxIiAvPgogIDxwb2x5Z29uCiAgICAgZmlsbD0iI2ZmZmZmZiIKICAgICBwb2ludHM9IjI0LDIwIDQ1LDMxLjc5OCAyNCw0NCAiCiAgICAgaWQ9InBvbHlnb24xIgogICAgIHN0eWxlPSJmaWxsLXJ1bGU6ZXZlbm9kZCIKICAgICB0cmFuc2Zvcm09Im1hdHJpeCgxLjE5MTczNzYsMCwwLDEuMTY5ODA0LC02LjYwMTcwMjksLTUuNDg0NjIwMSkiIC8+Cjwvc3ZnPgo=) 0 0 / contain no-repeat;
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
      color: #EDEDED;
      background: #1d1d1d;
      border: 0;
      border-radius: 20px;
      width: 150px;
      padding: 6px 10px;
      font-size: .9rem;
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
                        f'<a href="{row["Youtube"]}" target="_blank" rel="noopener" class="ytl"></a>',
                        "<b>",
                        row["Artist"],
                        "</b> – <i>",
                        row["Album"],
                        '</i><span class="rating">',
                        row["Rating"],
                        '/5</span><span class="genre">',
                        row["Genre"],
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
