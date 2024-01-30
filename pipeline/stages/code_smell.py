""" code smell

Add code smell info for Python and Java

"""
from typing import Tuple
import time
import os
import subprocess
from httpx import TimeoutException
from pydantic import BaseModel

from tqdm import tqdm
from utils.file import *
from utils.github import *
from collections import defaultdict
from config import PMD_PATH

ANALYZE_PYTHON = True
ANALYZE_JAVA = True
OVERRIDE = False


class CodeSmellCounter:
    def __init__(self):
        self.smells = []

    def add_code_smell(self, category: str, message: str):
        self.smells.append((category, message))

    def get_result(self):
        smells = defaultdict(lambda: defaultdict(int))
        for smell in self.smells:
            category, message = smell
            smells[category][message] += 1
        return smells


def find_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def get_python_code_smell_category(message_code):
    code_smell_type = {
        "C": "convention",
        "R": "refactor",
        "W": "warning",
        "E": "error",
        "F": "fatal",
        "I": "info",
    }
    return code_smell_type[message_code[0]]


def analyze_python_code_smells(directory) -> CodeSmellCounter:
    print(f"Analyzing Python code smells in {directory}")
    python_files = find_python_files(directory)

    counter = CodeSmellCounter()

    begin = time.time()
    message_pattern = re.compile(r"^.+?:(\d+):\d+:\s([CRWEFI]\d{4}):.+?\((.+?)\)")
    for file in python_files:
        if time.time() - begin > 60:
            print("Timeout analyzing python code smells")
            return None
        # Run pylint as a subprocess
        try:
            result = subprocess.run(
                ["pylint", file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60,
            )
        except TimeoutException as e:
            print(f"Timeout analyzing {file}")
            return None
        pylint_output = result.stdout

        # Parse the pylint output
        for line in pylint_output.split("\n"):
            match = message_pattern.match(line.strip())
            if match:
                line_number, message_code, message_type = match.groups(1)
                error_type = get_python_code_smell_category(message_code)
                counter.add_code_smell(error_type, message_code)

    return counter


java_code_smell_message_pattern = re.compile(r"^.+?:(\d+):\s+(\w+):.*?$")


def run_java_code_smell(dir: str, rulefile: str) -> list[str]:
    pmd_command = [
        PMD_PATH,
        "check",
        "-d",
        dir,
        "-R",
        rulefile,
        "-f",
        "text",
    ]
    try:
        result = subprocess.run(
            pmd_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
        )
        output = result.stdout
        messages = []
        for msg in output.split("\n"):
            match = java_code_smell_message_pattern.match(msg.strip())
            if match is not None:
                messages.append(match.group(2))
        return messages
    except TimeoutException as e:
        print(f"Timeout analyzing {dir}, rulefile: {rulefile}")
        return None


def analyze_java_code_smells(directory, only_src_dir: bool = False) -> CodeSmellCounter:
    rulefiles = [
        ("bestpractices", "category/java/bestpractices.xml"),
        ("codestyle", "category/java/codestyle.xml"),
        ("design", "category/java/design.xml"),
        ("documentation", "category/java/documentation.xml"),
        ("errorprone", "category/java/errorprone.xml"),
        ("multithreading", "category/java/multithreading.xml"),
        ("performance", "category/java/performance.xml"),
        ("security", "category/java/security.xml"),
    ]

    counter = CodeSmellCounter()
    src_directory = os.path.join(directory)
    if only_src_dir:
        src_directory = os.path.join(directory, "src")
    if not os.path.exists(src_directory):
        return None

    print(f"Analyzing Java code smells in {directory}")
    for rule, rulefile in rulefiles:
        code_smells = run_java_code_smell(src_directory, rulefile)
        if code_smells is None:
            return None
        for msg in code_smells:
            counter.add_code_smell(rule, msg)
        print(f"Rule {rule} finished, {len(code_smells)} code smells found")
    return counter


def download_repo(paper) -> bool:
    paper_id = paper["paper_id"]
    if os.path.exists(f"data/repo/{paper_id}"):
        return True
    print(f"downloading repo for paper {paper['paper_id']}")
    # repo_name = parse_repository_name(paper["artifact_url"])
    repo_name = paper.get("repo_name", None)
    if repo_name is None:
        return False
    code_url = f"https://github.com/{repo_name}"
    target_dir = f"data/repo/{paper_id}"
    command = ["git", "clone", "--depth", "1", code_url, target_dir]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"download repo {paper_id} failed")
        return False
    return True

def has_code_smell_info(paper):
    return (
        "code_smells" in paper
        and paper["code_smells"] is not None
    )

def add_code_smell_paper(paper):
    try:
        if "artifact_url" not in paper or "programming_language" not in paper:
            return False
        if not paper["programming_language"] in ["Python", "Java"]:
            return False
        if has_code_smell_info(paper) and not OVERRIDE:
            print(f"paper {paper['paper_id']} has code smell info, skipping")
            return False
        if not download_repo(paper):
            print(f"paper {paper['paper_id']} download repo failed")
            return False

        if OVERRIDE:
            paper["code_smells"] = None

        if paper["programming_language"] == "Python" and ANALYZE_PYTHON:
            counter = analyze_python_code_smells(f"data/repo/{paper['paper_id']}")
        elif paper["programming_language"] == "Java" and ANALYZE_JAVA:
            counter = analyze_java_code_smells(f"data/repo/{paper['paper_id']}")

        if counter is not None:
            paper["code_smells"] = counter.get_result()
        return True
    except BaseException as e:
        print(e)
        return False


def add_code_smell(input_file, output_file):
    print(
        f"Running code smell, analyze_python={ANALYZE_PYTHON}, analyze_java={ANALYZE_JAVA}, override={OVERRIDE}"
    )
    print(f"input_file: {input_file}, output_file: {output_file}")
    papers = load_json(input_file)
    last_checkpoint = time.time()
    CHECKPOINT_EVERY_SEC = 30
    for paper in tqdm(papers, "add code smell"):
        result = add_code_smell_paper(paper)
        if result and time.time() - last_checkpoint > CHECKPOINT_EVERY_SEC:
            dump_json(papers, output_file)
            last_checkpoint = time.time()
            print("checkpoint saved")
    dump_json(papers, output_file)


if __name__ == "__main__":
    add_code_smell("data/papers.json", "data/code_smell.json")
