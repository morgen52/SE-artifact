import json

papers = json.load(open("data/processed_papers.json"))
docs = json.load(open("data/documentary_fills.json"))
venues = ["ASE", "FSE", "ICSE", "ISSTA"]
years = [2017, 2018, 2019, 2020, 2021, 2022]

def how_many_papers():
    print(f"Total number of papers: {len(papers)}")

def how_many_artifacts():
    artifacts = 0
    valid_urls = 0
    github_repos = 0
    python_repos = 0
    java_repos = 0
    for paper in papers:
        if paper["artifact_url"]!= "":
            artifacts += 1
        if "artifact_url_valid" not in paper:
            print(paper)
        if paper["artifact_url_valid"] == "True":
            valid_urls += 1
        if ("repo_name" in paper) and paper["repo_name"]:
            github_repos += 1
        if ("code_smells" in paper) and paper["code_smells"]:
            if "Python" in paper["programming_language"]:
                python_repos += 1
            if "Java" in paper["programming_language"]:
                java_repos += 1

    print(f"Total number of artifacts: {artifacts}")
    print(f"Total number of valid artifact URLs: {valid_urls}")
    print(f"Total number of GitHub repos: {github_repos}")
    print(f"Total number of Python repos: {python_repos}")
    print(f"Total number of Java repos: {java_repos}")

def how_many_papers_offer_more_than_one_type_of_storage():
    papers_offer_more_than_one_type_of_storage = 0
    for paper in papers:
        if ("storage_website_type" in paper) and paper["storage_website_type"]:
            if len(paper["storage_website_type"].split(";")) > 1:
                papers_offer_more_than_one_type_of_storage += 1
    print(f"Total percentage of papers offer more than one type of storage: {papers_offer_more_than_one_type_of_storage/len(papers)*100:.1f}%")

# Github
def how_many_github_infos():
    programming_languages = 0
    github_update_date = 0
    star = 0
    star_over_300 = 0
    for paper in papers:
        if ("programming_language" in paper) and paper["programming_language"]:
            programming_languages += 1
        if ("github_update_date" in paper) and paper["github_update_date"]:
            github_update_date += 1
        if ("github_star" in paper) and paper["github_star"]:
            star += 1
            if paper["github_star"] >= 300:
                star_over_300 += 1
    print(f"Total number of programming languages: {programming_languages}")
    print(f"Total number of GitHub update dates: {github_update_date}")
    print(f"Total number of GitHub stars: {star}")
    print(f"Total number of GitHub stars over 300: {star_over_300}")

def how_many_zenodo():
    year2017 = 0
    zenodo2017 = 0
    for paper in papers:
        year = int(paper["paper_id"].split('-')[1])
        if (year==2017) and ("storage_website_type" in paper) and paper["storage_website_type"]:
            if "Zenodo" in paper["storage_website_type"]:
                zenodo2017 += 1
            year2017 += 1
    print(f"Zenodo ratio of papers from 2017: {zenodo2017/year2017*100:.1f}%")

def how_many_url_section():
    url_section17_21 = 0
    url_section22 = 0
    year17_21 = 0
    year22 = 0
    url_hyperlink = 0
    for paper in papers:
        if ("url_format" in paper) and paper["url_format"]:
            year = int(paper["paper_id"].split('-')[1])
            if (year==2017) or (year==2018) or (year==2019) or (year==2020) or (year==2021):
                year17_21 += 1
                if paper["url_format"] == "s":
                    url_section17_21 += 1
            elif year==2022:
                year22 += 1
                if paper["url_format"] == "s":
                    url_section22 += 1
            
            if paper["url_format"] == "h":
                url_hyperlink += 1

    print(f"papers with URL in Section (2017-2021): {url_section17_21/year17_21*100:.1f}%")
    print(f"papers with URL in Section (2022): {url_section22/year22*100:.1f}%")
    print(f"papers with URL as hyperlink: {url_hyperlink}, {url_hyperlink/(year17_21+year22)*100:.1f}%")

def how_many_link_rot():
    total = 0
    link_rot = 0
    for paper in papers:
        if ("artifact_url_valid" in paper) and paper["artifact_url_valid"]:
            if paper["artifact_url_valid"] == "False":
                link_rot += 1
            total += 1
    print(f"papers with link rot: {link_rot/total*100:.1f}%")

def how_many_document_quality():
    meet_examples = 0
    meet_examples_and_usability = 0
    for doc in docs:
        if doc["use_example"] == "Y":
            meet_examples += 1
            if doc["usability"] == "Y":
                meet_examples_and_usability += 1
    print(f"document quality meets exam.+usa. / exam.: {meet_examples_and_usability/meet_examples*100:.1f}%")


if __name__ == "__main__":
    how_many_papers()
    how_many_artifacts()
    how_many_papers_offer_more_than_one_type_of_storage()
    how_many_github_infos()
    how_many_zenodo()
    how_many_url_section()
    how_many_link_rot()
    how_many_document_quality()
