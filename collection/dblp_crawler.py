""" Dblp Crawler

This script crawls paper links from dblp. It crawls all papers from the
conferences specified in data/config.py. It writes the result to
data/dblp.xlsx, data/dblp.json, and data/dblp.csv.

Currently, the conferences include:
    - Conferences: ICSE, ASE, ISSTA, FSE
""" 

import time
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import collection.config as cfg
from utils.file import *
from configs.model import *
from collection.dblp_dataset import DblpDataset


def calculate_page(page_range: str) -> int:
    result = re.match(r"(\d+)-(\d+)", page_range)
    if result is not None:
        start_page = int(result.group(1))
        end_page = int(result.group(2))
        return end_page - start_page + 1
    result = re.match(r"(\d+):(\d+)-(\d+):(\d+)", page_range)
    if result is not None:
        start_page = int(result.group(2))
        end_page = int(result.group(4))
        return end_page - start_page + 1
    result = re.match(r"(\d+)", page_range)
    if result is not None:
        return 1
    raise Exception("Invalid page range: %s" % page_range)


def parse_doi(url: str) -> str:
    result = re.match(r"https://doi.org/(.*)", url)
    if result is not None:
        return result.group(1)
    return None


def parse_paper_from_entry(entry, venue, issue, index) -> DblpPaperRecord:
    paper_id = "%s-%s-%s" % (venue, issue, index)
    title = entry.find("span", itemprop="name", class_="title").text
    year = int(entry.find("meta", itemprop="datePublished").get("content"))

    if (t := entry.find("span", itemprop="pagination")) is not None:
        page_range = t.text
        pages = calculate_page(page_range)
    else:
        pages = 0

    doi = ""

    # Extract URLs
    urls = []
    for link_li in entry.find_all("li", class_="ee"):
        url = link_li.find("a").get("href")
        urls.append(url)
        if (t := parse_doi(url)) is not None:
            doi = t

    return DblpPaperRecord(
        title=title,
        paper_id=paper_id,
        venue=venue,
        issue=issue,
        year=year,
        urls=urls,
        pages=pages,
        doi=doi,
    )


def get_paper_list(venue: str, issue: int) -> list[DblpPaperRecord]:
    url = cfg.url_template[venue] % issue
    page_content = requests.get(url).text
    bs = BeautifulSoup(page_content, "lxml")
    entry_class = cfg.entry_classes[venue]
    entries = bs.find_all("li", class_=entry_class)

    papers = []
    for index, entry in enumerate(entries):
        if venue == "ASE" and issue == 2022:
            if index > 116: break # ASE 2022 mixes the research track with other tracks in dblp
        try:
            paper = parse_paper_from_entry(entry, venue, issue, index)
            papers.append(paper)
        except Exception as e:
            print(e)
            print("Error: %s-%d-%d" % (venue, issue, index))
    return papers

def parse_all():
    dblp_dataset = DblpDataset()

    for conference in cfg.conferences:
        for year in tqdm(cfg.years, desc=conference):
            papers = get_paper_list(conference, year)
            dblp_dataset.add_papers(papers)
            time.sleep(1)
    
    # filtering
    dblp_dataset = dblp_dataset.get_subset(
        lambda p: p.pages >= 6
    )

    dblp_dataset.dump_xlsx("data/dblp.xlsx")
    dblp_dataset.dump_json("data/dblp.json")
    dblp_dataset.dump_csv("data/dblp.csv")


if __name__ == "__main__":
    parse_all()
