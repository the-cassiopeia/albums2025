import csv
import datetime

FORMATTED_DATE = datetime.datetime.now().strftime("%B %d, %Y")

HTML_START = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Album Ratings</title>
    <link rel="stylesheet" href="styles.css" />
</head>

<body>
    <div class="container">
        <h1>Albums 2025</h1>
        <p class="date">Last updated: {FORMATTED_DATE}</p>
        <h2>Rating Scheme</h2>
        <div class="rating-guide">
            <p><strong>5/5</strong> - amazing - AOTY contender</p>
            <p><strong>4/5</strong> - great - very memorable</p>
            <p><strong>3/5</strong> - pretty good - would listen again</p>
            <p><strong>2/5</strong> - average - won't listen again</p>
            <p><strong>1/5</strong> - bad - has major issues</p>
        </div>
        <h2>Album Ranking</h2>
        <ol class="album-list">
"""


HTML_END = """
        </ol>
    </div>
</body>

</html>
"""


def main():

    HTML_ALBUMS = []

    with open("albums.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            assert len(row) == 4
            assert row["Artist"] is not None
            assert row["Album"] is not None
            assert row["Rating"] is not None
            assert 1 <= float(row["Rating"]) <= 5
            assert row["Genre"] is not None

            HTML_ALBUMS.append(
                "".join(
                    [
                        "            <li><strong>",
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
        f.write("\n".join(HTML_ALBUMS))
        f.write(HTML_END)


if __name__ == "__main__":
    main()
