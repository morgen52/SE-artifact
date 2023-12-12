# Software Artifacts

This repository contains the scripts, data, and results for our paper *Research Artifacts in Software Engineering Publications: Status and Trends*. 

**Remark**: 
- If you are only interested in the data we provided, `archive/processed_papers.json` is all you need. Our analysis scripts are based on this data.
- See our website that provides extented information based on this artifact: [CS-Artifacts](http://ra.bdware.cn/)

## Milestones
- 2023.12.12 release version "0.1.0" as the artifact for submission to JSS. [![DOI](https://zenodo.org/badge/729880425.svg)](https://zenodo.org/doi/10.5281/zenodo.10365503)


## Directory Structure

- `archive`: our data for paper lists (`archive/papers.json`) and paper metadata (`archive/processed_papers.json`)
- `collection`: scripts for data collection
- `pipeline`: scripts for data processing
- `analysis`: scripts for data analysis
- `data`: data files
- `images`: images used in our paper
- `utils` and `configs`: utility scripts
- `config.py`: configuration file for data processing scripts

## Installation

1. Our envrionment: Python 3.10+, Ubuntu 22.04
2. Clone this repository with git
3. Create your Python virtual environment and install the required packages

```bash
cd SE-artifact
pip install -r requirements.txt
```

## Reproduce Stages

We conduct our study in three stages: data collection, data processing, and data analysis.

### 1 Data Collection

#### 1.1 Get paper lists from DBLP

```bash
python3 -m collection.dblp_crawler
```

This script retrieves the paper lists for ICSE, ASE, ISSTA, and FSE from 2017-2022, excluding those with fewer than 6 pages.
The results will be saved in data/dblp.xlsx, data/dblp.json, and data/dblp.csv.

After that, you may see the following error:

```bash
Invalid page range: xxix-xxx
Error: ICSE-2022-0
Invalid page range: xxxi-xxxii
Error: ICSE-2022-1
```

After manual verification, the errors are associated with two entries: "Message from the ICSE 2022 General Chair" and "Message from the ICSE 2022 Program Chairs." Since these entries are not submitted papers for ICSE 2022, they can be disregarded.

#### 1.2 Manually download papers and check

We manually downloaded the papers according to the paper lists and mark them for the following:

- paper_id
- title
- artifact_url
- artifact_url_valid
- URL_location
- URL_format

```
URL location: a(abstract), i(introduction), c(conclusion), o(others), t(title). 
URL format: f(footnote), r(reference), t(in-text), h(hyperlink), s(section). 
```

We annotated the papers in paper.xlsx.
For the ease of parsing, we transfer it into "data/papers.json" and "data/papers.csv" by running

```bash
python3 -m collection.transfer_format
```

### 2 Data Processing

Based on "data/papers.json", we add the **github_info**(repo_name, repo_url, stars, forks, watches, issue_count, open_issue_count, update_date, programming_language), **storage_website_type**(Github, Artifact service, Personal homepage, Temporary drive and others), and **code smells** (Python, Java) of artifacts, and save to "data/processed_papers.json" .

In "pipeline/pipeline.py", there are three processing stages:

```python
add_github_info(input_file, output_file)
add_storage_website_type(input_file, output_file)
add_code_smell(input_file, output_file)
```

**Remarks**:

- The "add_github_info" script obtain github_info by github APIs. Before running the script, you need to add your github token in "config.py".
- The "add_code_smell" script obtain code smells by Pylint(Python code smell detector) and PMD(Java code smell detector). Before running the script, you need to make sure you can run "pylint" in your command line, and provide the path of PMD in "config.py".
- The "add_code_smell" script must be run after the "add_github_info" script.

For example, you may complete "config.py" as follows:

```python
PMD_PATH = "/the/path/to/your/bin/pmd"
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" // your github token
```

Then, you can add the infos by running the following commands:

```bash
python3 -m pipeline.pipeline
```

If you want to know more about the messages provided by Pylint and PMD, please refer to the following links:

- https://pylint.pycqa.org/en/latest/user_guide/messages/messages_overview.html
- https://pmd.github.io/pmd/pmd_rules_java.html

### 3 Data Analysis

### 3.1 Documentary

We first run the following command to generate the documentary template ("data/documentary.xlsx").

```bash
python3 -m analysis.documentary
```

Then, we manually check and fill in the documentary situation of Github artifacts from ICSE, and save the results in "data/documentary_fills.xlsx".

We convert the "data/documentary_fills.xlsx" into "data/documentary_fills.json" for the ease of parsing.

```bash
python3 -m analysis.documentary_convert
```

#### 3.2 Images

We use the following command to generate the images and tables used in our paper.

```bash
python3 -m draw.draw
```

This command will save the figures and tables in "images/*".

#### 3.3 Top-starred artifacts

We use the following command to generate the star ranking list ("data/github_star_ranking.csv").

```bash
python3 -m analysis.star
```

This script will generate "data/top_starred.xlsx" as a template. 
We manually fill in the characteristic infomation of top-starred artifacts (whose star number surpasses 100), and save the results in "data/top_starred_fills.xlsx".

We convert the "data/top_starred_fills.xlsx" into "data/top_starred_fills.csv" by running the following command:

```bash
python3 -m analysis.star_convert
```

#### 3.4 Other analysis

You can find other analysis in "analysis/statistics.py", which can be run by the following command:

```bash
python3 -m analysis.statistics
```


## Contact

If you have any questions, please submit issues or email to [lmg@pku.edu.cn](lmg@pku.edu.cn) .