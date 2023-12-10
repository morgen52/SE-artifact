from cgitb import text
import json
import re

def get_text_color(background_color):
    return "black"
    (r, g, b) = background_color
    text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
    return text_color

def set_minimum_height(heights, min_value):
    heights[(heights < min_value) & (heights != 0)] = min_value

    excess = heights.sum() - 100

    heights_above_min = heights[heights > min_value]
    heights[heights > min_value] -= (heights_above_min / heights_above_min.sum()) * excess

    heights_adjustment = 100 - heights.sum()
    heights[heights.idxmax()] += heights_adjustment

    return heights


def has_artifact(paper):
    return paper["artifact_url"].strip() != ""

def get_storage_website(paper):
    storage_websites = [
        ("GitHub", re.compile(r"github\.com")), # https://github.com/Lizenan1995/DNNOpAcc
        ("Zenodo", re.compile(r"zenodo")), # https://doi.org/10.5281/zenodo.3979097
        ("GitHub.io", re.compile(r"github.io")), # https://smokeml.github.io/
        ("Google.com", re.compile(r"sites\.google\.com")), # https://sites.google.com/view/darcy-project/home
    ]
    result = set()
    if "artifact_url" not in paper:
        return []
    for link in paper["artifact_url"].split("\n"):
        if link.strip() == "":
            continue
        link_type = "Others"
        for website, pattern in storage_websites:
            if pattern.search(link):
                link_type = website
                break
        result.add(link_type)
    return list(result)

def get_programming_language(paper):
    if paper["programming_language"] == "":
        return None
    language = paper["programming_language"]
    if language == "C++" or language == "C":
        return "C/C++"
    elif language == "Python":
        return "Python"
    elif language == "Java":
        return "Java"
    else:
        return None

def artifact_url_valid(paper):
    if "artifact_url_valid" in paper:
        if paper["artifact_url_valid"] == "True":
            return True
        elif paper["artifact_url_valid"] == "False":
            return False
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    papers = json.load(open("data/papers.json"))
    for paper in papers:
        websites = get_storage_website(paper)