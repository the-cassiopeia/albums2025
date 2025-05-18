import csv
import datetime
import sys

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
      font-family: 'Segoe UI', sans-serif;
      background-color: #111;
      color: #e5e5e5;
      margin: 0 auto;
      padding: 0;
      width: 660px;
    }
 
    .container {
      max-width: 100%;
    }

    .date {
      font-size: 1em;
      text-align: center;
      margin: 0;
    }

    h1 {
      text-align: center;
      color: #538146;
      font-size: 2rem;
      margin-top: 5px;
      margin-bottom: 5px;
    }

    h2 {
      color: #538146;
      font-size: 1.2rem;
    }

    .album-list {
      counter-reset: album-counter;
      list-style: none;
      padding: 0;
      display: flex;
      flex-direction: column;
      gap: 0px;
    }

    .album-list li {
      counter-increment: album-counter;
      background-color: #1e1e1e;
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 1rem;
      display: flex;
      flex-wrap: nowrap;
      align-items: center;
      gap: 4px;
      position: relative;
      padding-left: 45px;
    }

    .album-list li::before {
      content: counter(album-counter) ".";
      position: absolute;
      left: 10px;
      font-weight: 700;
      color: #538146;
    }

    .rating {
      font-weight: 700;
      color: #538146;
      margin-left: 8px;
    }

    .rating-info-trigger {
      position: relative;
      display: inline-block;
      margin-left: 8px;
      cursor: help;
      color: #538146;
      font-weight: bold;
      border: 2px solid #538146;
      border-radius: 50%;
      width: 1.2em;
      height: 1.2em;
      text-align: center;
      line-height: 1.1em;
      font-size: 0.95em;
      user-select: none;
    }

    .rating-tooltip {
      display: none;
      position: absolute;
      top: 125%;
      left: 50%;
      transform: translateX(-50%);
      background-color: #2a2a2a;
      color: #e5e5e5;
      border: 2px solid #538146;
      border-radius: 8px;
      padding: 3px 10px;
      width: 320px;
      z-index: 100;
      font-size: 1.0rem;
      font-weight: normal;
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
      font-style: italic;
      font-size: 0.9rem;
      color: #888;
      margin-left: auto;
    }

    .icon-link {
      display: inline-block;
    }

    .icon {
      height: 1.3em;
      vertical-align: text-top;
    }

    .filter-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 15px 0;
    }

    .filter-container h2 {
      margin: 0;
    }

    .genre-search-input {
      text-align: center;
      box-sizing: border-box;
      font-style: italic;
      background-color: #1e1e1e;
      color: #e5e5e5;
      border: 0px solid #444;
      padding: 6px 10px;
      width: 150px;
      border-radius: 20px;
      font-size: 0.9rem;
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
    let albumData = [];

    function initializeAlbumData() {
      albumData = Array.from(document.querySelectorAll('.album-list li')).map(item => {
        const genre = item.querySelector('.genre')?.textContent.toLowerCase() || '';
        return { element: item, genreText: genre };
      });
    }

    function filterByGenre() {
      if (!albumData.length) initializeAlbumData();
      const searchTerm = genreSearchInput.value.toLowerCase();
      albumData.forEach(({ element, genreText }) => {
        element.style.display = genreText.includes(searchTerm) ? 'flex' : 'none';
      });
    }

    initializeAlbumData();
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

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_START)
        f.write(HTML_BODY)
        f.write("\n".join(HTML_ALBUMS))
        f.write(HTML_END)


if __name__ == "__main__":
    main()
