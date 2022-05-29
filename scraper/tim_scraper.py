import logging
import re
import json
import os
import sys
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def get_past_episodes_urls():
    """_summary_"""
    directory_url = (
        "https://tim.blog/2018/09/20/all-transcripts-from-the-tim-ferriss-show/"
    )

    dir_site = requests.get(directory_url)
    dir_site.raise_for_status()

    soup = BeautifulSoup(dir_site.content, "html.parser")
    site_content = str(soup.find(class_="entry-content"))

    # Grab everything in the regex format
    regex = r'^<p><a href="([^"]*)"([^>]*)>(#\d*:[^<]*)</a></p>'
    matches = re.finditer(regex, site_content, re.MULTILINE)

    # store in json structure [{index, title, url},]
    bulk_transcript_urls = dict()
    for match_num, match in enumerate(matches, start=1):
        bulk_transcript_urls[match_num] = {
            "title": match.group(3),
            "url": match.group(1),
        }

    if len(bulk_transcript_urls) == 0:
        logging.warning("No matches found. Exiting system to avoid file overwrite.")
        sys.exit(0)

    output_path = os.sep.join(["output", "transcript_urls.json"])
    with open(output_path, "w", encoding="utf-8") as final:
        json.dump(bulk_transcript_urls, final, indent=2)
        logging.info(f"SUCCESS: Wrote URL list to {output_path}")


if __name__ == "__main__":
    get_past_episodes_urls()
