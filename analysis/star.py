import json
import openpyxl

papers = json.load(open("data/processed_papers.json"))
venues = ["ASE", "FSE", "ICSE", "ISSTA"]
years = [2017, 2018, 2019, 2020, 2021, 2022]

def sort_github_stars():
    data = {}
    for paper in papers:
        if paper["github_star"] is None:
            continue
        paper_id = paper["paper_id"]
        star = paper["github_star"]
        repo_name = paper['repo_name']
        fork = paper['github_fork']
        issue = paper['github_issues'] + paper['github_open_issues']
        update_date = paper['github_update_date']
        data[paper_id] = [star, repo_name, fork, issue, update_date]

    result = sorted(data.items(), key=lambda x: -x[1][0])
    for rank in range(len(result)):
        paper_id, info = result[rank]
        result[rank] = [rank+1, paper_id, info[0], info[1]] # star, repo_name
        
    with open("data/github_star_ranking.csv", "w") as f:
        f.write("rank,paper_id,star,repo_name\n") # headline
        for rank, paper_id, star, repo_name in result:
            f.write(f"{rank},{paper_id},{star},{repo_name}\n")

    # write top-starred artifacts (star number > 100) to data/top_starred.xlsx for manual checking
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "top_starred"
    ws.append(["rank", "paper_id", "star", "repo_name", "fork", "issue", "update_date"])
    for rank, paper_id, star, repo_name in result:
        if star < 100: break
        fork, issue, update_date = data[paper_id][2:]
        ws.append([rank, paper_id, star, f"https://github.com/{repo_name}", fork, issue, update_date])
    wb.save("data/top_starred.xlsx")

if __name__ == "__main__":
    sort_github_stars()
