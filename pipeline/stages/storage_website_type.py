""" storage website type
Add information about storage website type.
Current types:
- GitHub: "github.com"
- Artifact service: "zenodo|figshare"
- Personal homepage: "sites.google.com|github.io"
- Temporary drive and others: "drive.google.com|*"
"""

from collections import defaultdict
import re
import os
from utils.file import *
import requests
from collections import defaultdict

OVERRIDE = False
unknown_cnt = 0

def get_directed_url(url):
    try:
        print("redirecting", url)
        response = requests.get(url)
        return response.url
    except Exception as e:
        print(e)
        return url

def get_real_url(url):
    if re.search(r"doi\.org|tinyurl|bit\.ly|goo\.gl|cutt\.ly", url):
        return get_directed_url(url)
    return url

counts = defaultdict(int)

def get_storage_website(url):
    if re.search(r"github.com", url):
        return "github"
    elif re.search(r"zenodo|figshare", url):
        return "artifact_service"
    elif re.search(r"sites.google.com|github.io", url):
        return "personal_homepage"
    # elif re.search(r"drive.google.com", url):
    else:
        return "temporary_drive_and_others"

def add_storage_website_type_paper(url):
    url = get_real_url(url)
    storage_website_type = get_storage_website(url)
    counts[storage_website_type] += 1
    return storage_website_type

def add_storage_website_type(input_file, output_file):
    papers = load_json(input_file)
    for paper in papers:
        if "storage_website_type" in paper and not OVERRIDE:
            continue
        if "artifact_url" in paper and paper["artifact_url"] != "":
            storage_website_types = []
            for url in paper["artifact_url"].split(";"):
                storage_website_type = add_storage_website_type_paper(url)
                storage_website_types.append(storage_website_type)
            paper["storage_website_type"] = ";".join(storage_website_types)

    dump_json(papers, output_file)
    print("counts:", counts)

if __name__ == "__main__":
    add_storage_website_type("data/papers.json", "data/papers.json")