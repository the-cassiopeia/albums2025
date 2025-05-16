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
      width: 695px;
    }
 
    .container {
      max-width: 100%;
    }

    .date {
      font-size: 1em;
      text-align: center;
    }

    h1 {
      text-align: center;
      color: #538146;
      font-size: 2rem;
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
      gap: 8px;
    }

    .album-list li {
      counter-increment: album-counter;
      background-color: #1e1e1e;
      padding: 6px 20px;
      border-left: 5px solid #538146;
      border-radius: 10px;
      font-size: 1rem;
      display: flex;
      flex-wrap: nowrap;
      align-items: center;
      gap: 5px;
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

    .genre {
      font-style: italic;
      color: #888;
      margin-left: auto;
    }

    .rating-guide {
      background-color: #1e1e1e;
      border-left: 5px solid #538146;
      padding: 6px 20px;
      border-radius: 10px;
      margin-bottom: 10px;
      color: #f0f0f0;
    }

    .rating-guide p {
      margin: 4px 0;
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
      border-radius: 6px;
      font-size: 0.95rem;
    }
  </style>
</head>
"""

HTML_BODY = f"""
<body>
  <div class="container">
    <h1>Albums 2025</h1>
    <p class="date">Last updated: {FORMATTED_DATE}</p>
    <h2>Rating Scheme</h2>
    <div class="rating-guide">
      <p><strong>5/5</strong> - amazing - AOTY contender</p>
      <p><strong>4/5</strong> - great - very memorable</p>
      <p><strong>3/5</strong> - pretty good - would listen again</p>
      <p><strong>2/5</strong> - disappointing - won't listen again</p>
      <p><strong>1/5</strong> - bad - has major issues</p>
    </div>
    <div class="filter-container">
      <h2>Album Ranking</h2>
      <input placeholder="filter by genre" class="genre-search-input" id="genreSearch" onkeyup="filterByGenre()">
    </div>
    <ol class="album-list">
"""


HTML_END = """
    </ol>
  </div>
  <script defer>
    const genreSearchInput = document.getElementById('genreSearch');

    const albumData = Array.from(document.querySelectorAll('.album-list li')).map(listItem => {
      const genreElement = listItem.querySelector('.genre');
      return {
        element: listItem,
        genreText: genreElement ? genreElement.textContent.toLowerCase() : ''
      };
    });

    function filterByGenre() {
      const searchTerm = genreSearchInput.value.toLowerCase();

      albumData.forEach(album => {
        if (album.genreText.includes(searchTerm)) {
          album.element.style.display = 'flex';
        } else {
          album.element.style.display = 'none';
        }
      });
    }
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
