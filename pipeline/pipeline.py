"""
pipeline.py

this script scrape all needed paper informations from dblp, and github
"""

DEBUG_SUBSET = True

import os
from utils.file import *
from pipeline.stages import github
from pipeline.stages import code_smell
from pipeline.stages import storage_website_type
from pipeline.stages import dblp

if __name__ == "__main__":
    
    # dblp.add_dblp_info("data/papers.json", "data/processed_papers.json")

    github.add_github_info("data/processed_papers.json", "data/processed_papers.json")
    # storage_website_type.add_storage_website_type("data/processed_papers.json", "data/processed_papers.json")
    # code_smell.add_code_smell("data/processed_papers.json", "data/processed_papers.json")
