""" Augment Dblp info (Deprecated)

Given a paper's `conference`, `year`, and `title`, get its paper_url from dblp.

"""
from tqdm import tqdm
from collection.dblp_dataset import *
from utils.file import *
from utils.string import almost_identical

dblp_dataset = load_dblp_dataset_from_json("data/dblp.json")

def find_paper(title: str) -> DblpPaperRecord:
    for paper in dblp_dataset.get_paper_list():
        if almost_identical(paper.title, title):
            return paper
    return None

def has_all_dblp_info(paper):
    return "paper_id" in paper and \
        "venue" in paper and \
        "issue" in paper and \
        "year" in paper and \
        "paper_link" in paper and \
        "doi" in paper and \
        "pages" in paper

def add_dblp_info_paper(paper):
    if has_all_dblp_info(paper):
        return
    dblp_paper = find_paper(paper["title"])
    if dblp_paper is not None:
        paper["title"] = dblp_paper.title
        paper["paper_id"] = dblp_paper.paper_id
        paper["venue"] = dblp_paper.venue
        paper["issue"] = dblp_paper.issue
        paper["year"] = dblp_paper.year
        paper["paper_link"] = dblp_paper.urls[0] if len(dblp_paper.urls) > 0 else ""
        paper["doi"] = dblp_paper.doi
        paper["pages"] = dblp_paper.pages
    else:
        print("Cannot find paper: ", paper["title"])

def add_dblp_info(input_file, output_file):
    papers = load_json(input_file)
    for paper in tqdm(papers, "add dblp info"):
        add_dblp_info_paper(paper)
    dump_json(papers, output_file)