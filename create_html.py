import csv
import sys

import minify_html


def main():
    YT_PREFIX = "https://www.youtube.com/watch?v="

    LI_TEMPLATE = (
        '<li><a href="https://youtu.be/{youtube}" class="YT"></a>'
        '<b>{artist}</b> - <i>{album}</i><span class="rating">{rating}/5</span>'
        '<span class="genre">{genre}</span></li>'
    )

    html_albums = []
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
                assert row["Youtube"].startswith(YT_PREFIX)
                assert row["Youtube"] not in all_youtubes
            except (AssertionError, ValueError):
                print("Error while parsing the following row:")
                print(row)
                sys.exit(1)

            all_youtubes.add(row["Youtube"])

            html_albums.append(
                LI_TEMPLATE.format(
                    youtube=row["Youtube"].strip().removeprefix(YT_PREFIX),
                    artist=row["Artist"].strip(),
                    album=row["Album"].strip(),
                    rating=row["Rating"].strip(),
                    genre=row["Genre"].strip(),
                )
            )

    with open("template.html", "r", encoding="utf-8") as fin:
        html_template = fin.read()

    assert html_template.count("<!--PLACEHOLDER_ALBUM_LIST-->") == 1

    with open("index.html", "w", encoding="utf-8") as fout:
        fout.write(
            minify_html.minify(
                html_template.replace(
                    "<!--PLACEHOLDER_ALBUM_LIST-->", "\n".join(html_albums)
                ),
                minify_js=True,
                minify_css=True,
                minify_doctype=True,
                remove_processing_instructions=True,
            )
        )


if __name__ == "__main__":
    main()
