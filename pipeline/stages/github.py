"""Augment github statistics

Given a paper with `artifact_url`, get statistics from github repository.

Currently, we get the following statistics:
- `repo_name`: the repository name
- `github_star`: the number of stars
- `github_fork`: the number of forks
- `github_issues`: the number of issues
- `github_open_issues`: the number of open issues
- `github_update_date`: the date of the last update`
"""

import time
from datetime import datetime
import os

from tqdm import tqdm
from github import Github, Auth
from pydantic import BaseModel

from utils.file import *
from utils.github import *
from config import GITHUB_TOKEN

os.environ["https_proxy"] = "http://localhost:7890"
auth = Auth.Token(GITHUB_TOKEN)
GITHUB = Github(auth=auth)

class RepoInfo(BaseModel):
    repo_name: str
    stars: int
    forks: int
    watches: int
    issue_count: int
    open_issue_count: int
    update_date: datetime
    programming_language: str

def get_star_history(repo_name: str):
    try:
        repo = GITHUB.get_repo(repo_name)
    except:
        return None

    star_history = []
    for star in repo.get_stargazers_with_dates():
        star_history.append((star.starred_at, star.user.login))
    return star_history

def get_repo_info(repo_name: str) -> RepoInfo | None:
    try:
        repo = GITHUB.get_repo(repo_name)
    except:
        return None

    issue_count = len(list(repo.get_issues(state="all")))
    open_issue_count = len(list(repo.get_issues(state="open")))
    # update_date = repo.updated_at
    update_date = repo.pushed_at
    
    return RepoInfo(
        repo_name=repo_name, 
        stars=repo.stargazers_count, 
        forks=repo.forks_count, 
        watches=repo.subscribers_count,
        issue_count=issue_count,
        open_issue_count=open_issue_count,
        update_date=update_date,
        programming_language=repo.language if repo.language is not None else "",
    )

def date_to_str(date: datetime):
    return date.strftime("%Y-%m-%d")

def has_all_github_info(paper):
    return "repo_name" in paper and \
        "github_star" in paper and \
        "github_fork" in paper and \
        "github_issues" in paper and \
        "github_open_issues" in paper and \
        "github_update_date" in paper and \
        "programming_language" in paper and \
        paper["repo_name"] != ""

def handle_repo(repo_url):
    repo_name = parse_repository_name(repo_url)
    repo_info = get_repo_info(repo_name)
    if repo_info is None:
        return False
    paper = {}
    paper['repo_name'] = repo_info.repo_name
    paper['github_star'] = repo_info.stars
    paper['github_fork'] = repo_info.forks
    paper['github_issues'] = repo_info.issue_count
    paper['github_open_issues'] = repo_info.open_issue_count
    paper['github_update_date'] = date_to_str(repo_info.update_date)
    paper['programming_language'] = repo_info.programming_language
    return paper

def add_github_info_paper(paper):
    try:
        if has_all_github_info(paper):
            return False
        else:
            paper["repo_name"] = None
            paper["github_star"] = -1
            paper["github_fork"] = None
            paper["github_issues"] = None
            paper["github_open_issues"] = None
            paper["github_update_date"] = None
            paper["programming_language"] = None

        for artifact_url in paper["artifact_url"].split(";"):
            repo = handle_repo(artifact_url)
            if repo and (repo["github_star"] > paper["github_star"]):
                paper["repo_name"] = repo["repo_name"]
                paper["github_star"] = repo["github_star"]
                paper["github_fork"] = repo["github_fork"]
                paper["github_issues"] = repo["github_issues"]
                paper["github_open_issues"] = repo["github_open_issues"]
                paper["github_update_date"] = repo["github_update_date"]
                paper["programming_language"] = repo["programming_language"]

        if paper["github_star"] == -1: # no repo found
            paper["github_star"] = None
        return True
    except Exception as e:
        print(e)
        return False

def add_github_info(input_file, output_file):
    papers = load_json(input_file)
    last_checkpoint = time.time()
    CHECKPOINT_EVERY_SEC = 30
    for paper in tqdm(papers, "add github info"):
        result = add_github_info_paper(paper)
        if result and time.time() - last_checkpoint > CHECKPOINT_EVERY_SEC:
            dump_json(papers, output_file)
            last_checkpoint = time.time()
            print("checkpoint saved")
    dump_json(papers, output_file)

if __name__ == "__main__":
    add_github_info("data/papers.json", "data/papers.json")
