import os
import json
import re
import ssl
import logging
import urllib.request
from PyPDF2 import PdfReader

ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join("logs", "pdf_downloader.log")),
        logging.StreamHandler(),
    ],
)


def collect_pdfs(input_json):
    # Read json content
    with open(input_json, "r") as f:
        json_content = json.load(f)

    # Get URLs that end with ".pdf"
    for i in json_content:
        url = json_content[i]["url"]
        # If URL ends with ".pdf", download it
        if re.match(r".*\.pdf\/?$", url):
            formatted_title = url.rsplit("/", 1)[-1]
            base_path = os.path.join("Transcripts", "PDFs")
            download_pdf_from_url(url, os.path.join(base_path, formatted_title))


def download_pdf_from_url(url, pdf_path):
    urllib.request.urlretrieve(url, pdf_path)
    logging.info(f"Downloaded PDF from '{url}' to '{pdf_path}'.")


def scrape_pdf(pdf):
    """Converts PDF to TXT.

    Args:
        pdf (str): PDF to be scraped.
    """
    reader = PdfReader(pdf)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    print(text)


if __name__ == "__main__":
    collect_pdfs("output/transcript_urls.json")
