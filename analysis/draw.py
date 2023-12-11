""" Draw figures and tables for the paper. 
TODO
1. optimize plot style
"""
from collections import defaultdict
import os
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from collection.dblp_dataset import *
from typing import Callable, Tuple

import analysis.utils as utils

SNS_THEME = "dark"
FONT_FAMILY = "Arial"
OVERRIDE = True
OUTPUT_DIR = "images"

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIG_SIZE = 12

LABEL_SIZE = BIG_SIZE
TICK_SIZE = MEDIUM_SIZE

# sns.set(font=FONT_FAMILY)

font = {"family": "Arial", "size": 10}
mpl.rc("font", **font)

grayscale_palette = ['#bfbfbf', '#8c8c8c', '#595959', '#1f1f1f']
soft_color_palette = ['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a']
sns.set_palette(soft_color_palette)

papers = json.load(open("data/processed_papers.json"))
venues = ["ICSE", "FSE", "ASE", "ISSTA"]
storage_websites = ["GitHub", "Zenodo", "GitHub.io", "Google.com", "Others"]
programming_languages = ["Python", "Java", "C/C++"]
java_code_smells = [
    "bestpractices",
    "codestyle",
    "design",
    "documentation",
    "errorprone",
    "multithreading",
    "performance",
]
java_code_smells_label = [
    "Best Practices",
    "Code Style",
    "Design",
    "Documentation",
    "Error Prone",
    "Multithreading",
    "Performance",
]
python_code_smells = ["convention", "warning", "refactor"]
python_code_smells_label = ["Convention", "Warning", "Refactor"]
years = [2017, 2018, 2019, 2020, 2021, 2022]

def draw_stacked_bar_chart(df, ax, colnames, yaxis_type):
    all_percentage = df.copy(True).div(df.sum(axis=1), axis=0).multiply(100)
    if yaxis_type == "percentage":
        all_heights = all_percentage.copy(True).apply(
            lambda row: utils.set_minimum_height(row, 7), axis=1
        )
    elif yaxis_type == "count":
        all_heights = df
    else:
        raise ValueError("yaxis_type should be either 'percentage' or 'count'")

    height_cum = all_heights.cumsum(axis=1)

    for i, (colname, color) in enumerate(zip(colnames, sns.color_palette())):
        percentage = all_percentage[colname]
        height = all_heights[colname]
        starts = height_cum[colname] - height

        rects = ax.bar(years, height, bottom=starts, label=colname, color=color)
        text_color = utils.get_text_color(color)

        for rect, h, p in zip(rects, height, percentage):
            if p != 0:
                ax.annotate(
                    "%.1lf%%" % (p,),
                    xy=(rect.get_x() + rect.get_width() / 2, rect.get_y() + h / 2),
                    ha="center",
                    va="center",
                    fontsize=MEDIUM_SIZE,
                    color=text_color,
                )

def figure_ratio_with_artifact(filename):
    """
    Figure 1: Number and ratio of top-tier publications with and
    without artifacts from 2017 to 2022.
    """

    papers_df = pd.DataFrame(papers)
    papers_df["Artifact Present"] = papers_df.apply(
        lambda x: utils.has_no_artifact(x), axis=1
    )
    df = (
        papers_df.groupby("year")["Artifact Present"]
        .value_counts()
        .unstack(fill_value=0)
    )
    df = df.div(df.sum(axis=1), axis=0).multiply(100)
    df.rename(columns={False: "With Artifact", True: "Without Artifact"}, inplace=True)

    ax = df.plot(kind="bar", stacked=True, figsize=(5, 3), width=0.7)

    ax.bar_label(
        ax.containers[-2], fmt="%.1f%%", label_type="center", fontsize=MEDIUM_SIZE,
    )
    ax.bar_label(
        ax.containers[-1],
        fmt="%.1f%%",
        label_type="center",
        fontsize=MEDIUM_SIZE,
        padding=-10,
    )

    # ax.set_yticklabels([])
    # ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), ncol=2, fontsize=TICK_SIZE)
    ax.legend(loc="upper center", ncol=2, fontsize=TICK_SIZE)
              
    plt.xticks(rotation=0, fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    ax.set_ylabel("Percentage (%)", fontsize=LABEL_SIZE)
    plt.tight_layout()
    plt.savefig(filename)

def figure_distribution_storage_website(filename):
    """
    Figure 3: Distribution and trend of storage website adoption for SE
    artifacts from 2017 to 2022.
    """
    papers_df = pd.DataFrame(papers)
    papers_df["Storage Website"] = papers_df.apply(
        lambda x: utils.get_storage_website(x), axis=1
    )
    df = (
        papers_df.explode("Storage Website")
        .groupby("year")["Storage Website"]
        .value_counts()
        .unstack(fill_value=0)
    )
    df = df[storage_websites]
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_stacked_bar_chart(df, ax, storage_websites, "percentage")
    lgd = ax.legend(
        ncols=len(storage_websites),
        bbox_to_anchor=(0.5, 1.1),
        loc="upper center",
        fontsize=SMALL_SIZE,
        columnspacing=0.8,
    )
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    # ax.set_xlabel("Year", fontsize=LABEL_SIZE)
    ax.set_ylabel("Percentage (%)", fontsize=LABEL_SIZE)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", bbox_extra_artists=(lgd,))

def figure_artifact_by_programming_language(filename):
    """
    Figure 4: The number and ratio of artifacts with different programming
    languages.
    """
    papers_df = pd.DataFrame(papers)
    papers_df["Programming Language"] = papers_df.apply(
        lambda x: utils.get_programming_language(x), axis=1
    )
    df = (
        papers_df[papers_df["Programming Language"].notnull()]
        .groupby("year")["Programming Language"]
        .value_counts()
        .unstack(fill_value=0)
    )

    all_percentage = df.copy(True).div(df.sum(axis=1), axis=0).multiply(100)
    df = df[programming_languages]

    fig, ax = plt.subplots(figsize=(5, 5))

    height_cum = df.cumsum(axis=1)

    for i, (colname, color) in enumerate(zip(programming_languages, sns.color_palette())):
        percentage = all_percentage[colname]
        height = df[colname]
        starts = height_cum[colname] - height

        rects = ax.bar(years, height, bottom=starts, label=colname, color=color)
        text_color = utils.get_text_color(color)

        for rect, h, p in zip(rects, height, percentage):
            if p != 0:
                ax.annotate(
                    "%.1lf%%" % (p,),
                    xy=(rect.get_x() + rect.get_width() / 2, rect.get_y() + h / 2),
                    ha="center",
                    va="center",
                    fontsize=MEDIUM_SIZE,
                    color=text_color,
                )

    lgd = ax.legend(fontsize=MEDIUM_SIZE)
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    # ax.set_xlabel("Year", fontsize=LABEL_SIZE)
    ax.set_ylabel("Number", fontsize=LABEL_SIZE)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", bbox_extra_artists=(lgd,))

def figure_invalid_url_ratio_by_year(filename):
    """
    Figure 6: The ratio of invalid URLs from 2017 to 2022.
    """
    label_available = "Available artifacts"
    label_unavailable = "Unavailable artifacts"
    columns = [label_available, label_unavailable]

    df = pd.DataFrame(papers)
    df["Invalid URL"] = df.apply(lambda x: utils.artifact_url_valid(x), axis=1)
    df = (
        df[df["Invalid URL"].notnull()]
        .groupby("year")["Invalid URL"]
        .value_counts()
        .unstack(fill_value=0)
    )
    df.rename(columns={True: label_available, False: label_unavailable}, inplace=True)
    df = df[columns]
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_stacked_bar_chart(df, ax, columns, "percentage")

    lgd = ax.legend(fontsize=MEDIUM_SIZE, loc="lower right")
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    # ax.set_xlabel("Year", fontsize=LABEL_SIZE)
    ax.set_ylabel("Percentage (%)", fontsize=LABEL_SIZE)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", bbox_extra_artists=(lgd,))

def figure_invalid_url_ratio_by_storage_website(filename):
    """
    Figure 7: The proportions of unavailable artifacts in different
    types of storage websites
    """
    count = {}
    for paper in papers:
        valid = paper.get("artifact_url_valid", None)
        if not valid:
            continue
        if ("storage_website_type" in paper) and paper["storage_website_type"]:
            types = paper["storage_website_type"].split(";")
            for type in types:
                if type not in count:
                    count[type] = {"True": 0, "False": 0}
                count[type][valid] += 1
    # to percentage
    for key in count:
        total = count[key]["True"] + count[key]["False"]
        count[key]["True"] =  count[key]["True"] / total * 100
        count[key]["False"] =  count[key]["False"] / total * 100

    fig, ax = plt.subplots(figsize=(5, 5))
    sort_key = ["github", "artifact_service", "personal_homepage", "temporary_drive_and_others"]
    x_labels = ["Github", "Artifact\nservice", "Personal\nhomepage", "Temporary\nDrive&Others"]
    width = 0.4
    x = [width + 1.2 * i * width for i in range(len(sort_key))]
    valid_url = [count[key]["True"] for key in sort_key]
    invalid_url = [count[key]["False"] for key in sort_key]
    ax.bar(x, valid_url, width, label="Available artifacts")
    ax.bar(x, invalid_url, width, bottom=valid_url, label="Unavailable artifacts")
    # set text
    for i, (valid, invalid) in enumerate(zip(valid_url, invalid_url)):
        ax.text(x[i], valid / 2, f"{valid:.1f}%", ha="center", va="center", fontsize=MEDIUM_SIZE)
        ax.text(x[i], (valid + invalid / 2), f"{invalid:.1f}%", ha="center", va="center", fontsize=MEDIUM_SIZE)
    lgd = ax.legend(fontsize=MEDIUM_SIZE, loc="lower right")
    plt.xticks(x, x_labels, fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    # ax.set_xlabel("Storage Website", fontsize=LABEL_SIZE)
    plt.ylabel("Percentage (%)", fontsize=LABEL_SIZE)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", bbox_extra_artists=(lgd,))

def draw_pie_graph(ax, data, startangle):
    wedges, text = ax.pie(
        data, colors=sns.color_palette("Set2", 8), startangle=startangle
    )

    kw = dict(arrowprops=dict(arrowstyle="-"), va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(
            "%.1lf%%" % data[i],
            xy=(x, y),
            xytext=(1.2 * np.sign(x), 1.3 * y),
            horizontalalignment=horizontalalignment,
            **kw,
            fontsize=SMALL_SIZE,
        )
    return wedges

def draw_code_smell_pie_graph(ax, df, categories, categories_label, startangle):
    counts = defaultdict(int)
    for index, row in df.iterrows():
        for category, subcategory in row["code_smells"].items():
            counts[category] += sum(subcategory.values())

    counts = [counts[category] for category in categories]
    total = sum(counts)
    counts = [(count / total) * 100 for count in counts]
    
    wedges = draw_pie_graph(ax, counts, startangle)

    ax.legend(
        wedges,
        categories_label,
        ncols=2,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.5),
        fontsize=SMALL_SIZE,
        columnspacing=0.8,
    )

def figure_java_code_smell(filename):
    """
    Figure 8: Ratio of different types of Python (a) and Java (b)
    messages from 2017 to 2022.
    """
    fig, ax = plt.subplots(figsize=(2.5, 3))
    df = pd.DataFrame(papers)
    df = df[df["programming_language"] == "Java"]
    df = df[df["code_smells"].notnull()]
    draw_code_smell_pie_graph(ax, df, java_code_smells, java_code_smells_label, 20)
    plt.tight_layout()
    plt.savefig(filename)

def figure_python_code_smell(filename):
    """
    Figure 8: Ratio of different types of Python (a) and Java (b)
    messages from 2017 to 2022.
    """
    fig, ax = plt.subplots(figsize=(2.5, 3))
    df = pd.DataFrame(papers)
    df = df[df["programming_language"] == "Python"]
    df = df[df["code_smells"].notnull()]
    draw_code_smell_pie_graph(ax, df, python_code_smells, python_code_smells_label, -40)
    plt.tight_layout()
    plt.savefig(filename)

def figure_url_location(filename):
    """
    Figure 5: Distribution of artifact locations of URLs
    provided in a paper
    """
    df = pd.DataFrame(papers)
    df = df.apply(
        lambda x: utils.get_url_location(x), axis=1
    )
    df = df.explode("url_location").value_counts()
    counts = df.values / df.values.sum() * 100
    fig, ax = plt.subplots(figsize=(2.5, 3))
    wedges = draw_pie_graph(ax, counts, 20)
    ax.legend(
        wedges,
        df.index,
        ncols=2,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.5),
        fontsize=SMALL_SIZE,
        columnspacing=0.8,
    )
    plt.tight_layout()
    plt.savefig(filename)

def figure_url_format(filename):
    """
    Figure 5: Distribution of artifact format of URLs
    provided in a paper
    """
    df = pd.DataFrame(papers)
    df = df.apply(
        lambda x: utils.get_url_format(x), axis=1
    )
    df = df.explode("url_format").value_counts()
    counts = df.values / df.values.sum() * 100
    fig, ax = plt.subplots(figsize=(2.5, 3))
    wedges = draw_pie_graph(ax, counts, 20)
    ax.legend(
        wedges,
        df.index,
        ncols=2,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.5),
        fontsize=SMALL_SIZE,
        columnspacing=0.8,
    )
    plt.tight_layout()
    plt.savefig(filename)

def table_artifact_ratio_by_conference_and_year(filename):
    """
    Table 2
    Results of our paper collection. In each cell, the first number presents
    the number of papers with artifacts, and the second number represents the
    total number of papers.
    """
    papers_df = pd.DataFrame(papers)
    papers_df["Artifact Present"] = papers_df.apply(
        lambda x: utils.has_artifact(x), axis=1
    )
    df = (
        papers_df.groupby(["year", "venue"])["Artifact Present"]
        .value_counts()
        .unstack(fill_value=0)
    )
    
    writer = csv.writer(open(filename, "w"))
    columns = ["venue", "2017", "2018", "2019", "2020", "2021", "2022", "total"]
    writer.writerow(columns)
    for venue in venues:
        row = [venue]
        for year in years:
            cnt_artifact = df.loc[year, venue][True]
            cnt_all = df.loc[year, venue].sum()
            row.append(
                "%d/%d (%.1lf%%)"
                % (cnt_artifact, cnt_all, cnt_artifact / cnt_all * 100)
            )
        df.xs(venue, level=1)
        venue_artifact = df.xs(venue, level=1)[True].sum()
        venue_all = df.xs(venue, level=1).sum().sum()
        row.append(
            "%d/%d (%.1lf%%)"
            % (venue_artifact, venue_all, venue_artifact / venue_all * 100)
        )
        writer.writerow(row)

    row = ["total"]
    for year in years:
        cnt_artifact = df.loc[year, :][True].sum()
        cnt_all = df.loc[year, :].sum().sum()
        row.append(
            "%d/%d (%.1lf%%)" % (cnt_artifact, cnt_all, cnt_artifact / cnt_all * 100)
        )
    all_artifact = df[True].sum()
    all_papers = df.sum().sum()
    row.append(
        "%d/%d (%.1lf%%)" % (all_artifact, all_papers, all_artifact / all_papers * 100)
    )
    writer.writerow(row)

def table_maintenance_situation(filename):
    """
    Table 3
    The maintenance situation of ASE, FSE, ICSE and ISSTA
    2017-2022. Each number presents the ratio of artifacts that
    gets updated after each key time point
    """
    dates = ["Submission_deadline", "Paper_notification", "Camera-ready_deadline", "Conference_time"]
    with open("data/conf_dates.json", "r") as f:
        conf_dates = json.load(f)
    confs = ["ASE", "FSE", "ICSE", "ISSTA"]

    results = {}
    count = {}
    for venue in confs:
        results[venue] = {}
        count[venue] = {}
        for year in years:
            results[venue][year] = {}
            count[venue][year] = 0
            for date in dates:
                results[venue][year][date] = 0
    
    def later_than(date1, date2): # return date1 > date2
        y1, m1, d1 = map(int, date1.split("-"))
        y2, m2, d2 = map(int, date2.split("-"))
        if y1 > y2:
            return True
        elif y1 == y2:
            if m1 > m2:
                return True
            elif m1 == m2:
                if d1 > d2:
                    return True
        return False
    
    for paper in papers:
        venue, year, _ = paper["paper_id"].split("-")
        year = int(year)
        if paper["github_update_date"]:
            count[venue][year] += 1
            for date in dates:
                if later_than(paper["github_update_date"], conf_dates[venue][str(year)][date]):
                    results[venue][year][date] += 1
    
    writer = csv.writer(open(filename, "w"))
    head_row = ["Conference", "Year", "Submission deadline", "Paper notification", "Camera-ready deadline", "Conference time"]
    writer.writerow(head_row)
    for venue in confs:
        for year in years:
            row = [venue, year]
            for date in dates:
                row.append("%.1lf%%" % (results[venue][year][date] / count[venue][year] * 100))
            writer.writerow(row)
        row = [venue, "Average"]
        for date in dates:
            row.append("%.1lf%%" % (sum(results[venue][y][date] for y in years) / sum(count[venue][y] for y in years) * 100))
        writer.writerow(row)

def table_star_distribution(filename):
    """
    Table 4
    The distribution of star numbers of SE artifacts from 2017 to
    2022. Each number presents the ratio of artifacts whose star
    numbers belong to the range in the first column.
    """
    star_ranges = [(0, 0), (1, 5), (6, 10), (11, 20), (21, 50), (51, 100), (100, -1)]

    def get_star_range(index) -> Tuple[str, Callable[[int], bool]]:
        if index == 0:
            return "0", lambda x: x == 0
        if index == 6:
            return "100+", lambda x: x >= 100
        l, r = star_ranges[index]
        return f"{l}-{r}", lambda x: l <= x <= r

    def get_star_index(star):
        for i in range(len(star_ranges)):
            _, func = get_star_range(i)
            if func(star):
                return i
        return -1

    df = pd.DataFrame(papers)
    df = df[df["github_star"].notnull()]
    df["star_index"] = df.apply(lambda x: get_star_index(x["github_star"]), axis=1)
    df = df.groupby("year")["star_index"].value_counts().unstack(fill_value=0)
    total = df.sum().sum()

    last_row = ["average"]
    for i in range(len(star_ranges)):
        last_row.append("%.1lf%%" % (df.loc[:, i].sum() / total * 100))

    df = df.div(df.sum(axis=1), axis=0).multiply(100)

    writer = csv.writer(open(filename, "w"))

    head_row = ["year"] + [get_star_range(i)[0] for i in range(len(star_ranges))]
    writer.writerow(head_row)

    for year in years:
        row = [year]
        for i in range(len(star_ranges)):
            row.append("%.1lf%%" % df.loc[year, i])
        writer.writerow(row)

    writer.writerow(last_row)

def table_document_situation(filename):
    """
    Table 5
    The documentation situation for ICSE from 2017 to 2022.
    Each number presents the ratio of artifacts that meet the
    criterion in the first column.
    """

    with open("data/documentary_fills.json", "r") as f:
        documentary_fills = json.load(f)
        
    categories = [
        "completeness",
        "structure",
        "usability",
        "use_example",
        "certificate",
        "contact",
    ]
    category_labels = [
        "Completeness",
        "Structure",
        "Usability",
        "Example",
        "Certificate",
        "Contact",
    ]

    writer = csv.writer(open(filename, "w"))

    head_row = ["year"] + category_labels
    writer.writerow(head_row)

    total_counts = {category: 0 for category in categories}
    doc_num_year = {year: 0 for year in years}

    doc_data = {}
    for year in years:
        doc_data[year] = {category: 0 for category in categories}
    for paper in documentary_fills:
        year = int(paper["paper_id"].split("-")[1])
        doc_num_year[year] += 1
        for category in categories:
            if paper[category] == "Y":
                doc_data[year][category] += 1
                total_counts[category] += 1
    total_doc_num = sum(doc_num_year.values())

    for year in years:
        row = [year]
        for category in categories:
            row.append("%.1lf%%" % (doc_data[year][category] / doc_num_year[year] * 100))
        writer.writerow(row)

    last_row = ["average"]
    for category in categories:
        last_row.append("%.1lf%%" % (total_counts[category] / total_doc_num * 100))
    writer.writerow(last_row)

def write_table_top_code_smell(df, writer, language, categories, categories_labels):
    for category, label in zip(categories, categories_labels):
        total_smells = 0
        category_count = 0
        counts = defaultdict(int)
        for index, row in df.iterrows():
            if category in row["code_smells"]:
                category_count += 1
                for subcategory, cnt in row["code_smells"][category].items():
                    counts[subcategory] += cnt
                    total_smells += cnt

        top3 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for subcategory in top3:
            row = [
                language,
                label,
                "%d/%d" % (category_count, len(df)),
                subcategory[0],
                "%.1lf%%" % (subcategory[1] / total_smells * 100),
            ]
            writer.writerow(row)

def table_top_code_smell(filename):
    """
    Table 6
    The top three most common alert messages under each smell category for
    Python (top three rows) and Java (bottom seven rows).
    """
    df = pd.DataFrame(papers)
    df = df[df["code_smells"].notnull()]

    writer = csv.writer(open(filename, "w"))

    head_row = [
        "language",
        "category",
        "category_prevalence",
        "subcategory",
        "subcategory_percentage",
    ]
    writer.writerow(head_row)

    write_table_top_code_smell(
        df[df["programming_language"] == "Python"],
        writer,
        "Python",
        python_code_smells,
        python_code_smells_label,
    )
    write_table_top_code_smell(
        df[df["programming_language"] == "Java"],
        writer,
        "Java",
        java_code_smells,
        java_code_smells_label,
    )

def figure_artifact_ratio_by_conference_and_year(filename):
    papers_df = pd.DataFrame(papers)
    papers_df["Artifact Present"] = papers_df.apply(
        lambda x: utils.has_artifact(x), axis=1
    )
    df = (
        papers_df.groupby(["venue", "year"])["Artifact Present"]
        .value_counts()
        .unstack(fill_value=0)
    )

    # print(df)

    plt.figure(figsize=(10, 5))
    bar_width = 0.2  # Width of each bar

    conf_loc = [(len(years)*bar_width/2) + i*((len(years)+1)*bar_width) for i in range(len(venues))]
    year_loc = [-(len(years)*bar_width/2) + (i + 0.5) * bar_width for i in range(len(years))]
    # print(conf_loc)
    # print(year_loc)

    real_locs = []
    with_artifacts = []
    without_artifacts = []
    for i, (conf, year) in enumerate(df.index):
        real_loc = conf_loc[venues.index(conf)] + year_loc[years.index(year)]
        real_locs.append(real_loc)
        with_artifacts.append(df.loc[conf, year][True])
        without_artifacts.append(df.loc[conf, year][False])
    # draw the stacked bar
    plt.bar(real_locs, with_artifacts, bar_width, label="With Artifacts", edgecolor="white")
    plt.bar(real_locs, without_artifacts, bar_width, bottom=with_artifacts, label="Without Artifacts", edgecolor="white")
    plt.legend(loc="upper right", fontsize=LABEL_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    plt.ylabel("Number of Papers", fontsize=LABEL_SIZE)

    # double y-axis, draw the line of ratio
    ax2 = plt.twinx()
    ratio = [with_artifacts[i] / (with_artifacts[i] + without_artifacts[i]) for i in range(len(with_artifacts))]
    for i in range(len(venues)):
        ax2.plot(real_locs[i*len(years):(i+1)*len(years)], ratio[i*len(years):(i+1)*len(years)], color="black", marker="o", linewidth=2, markersize=4)
    ax2.set_ylim(0, 1)
    ax2.set_yticks(np.arange(0, 1.1, 0.1))
    ax2.set_ylabel("Ratio of Papers with Artifacts", fontsize=LABEL_SIZE)
    ax2.tick_params(axis="y", labelsize=TICK_SIZE)

    # Adding labels and title
    xticks_loc = real_locs + conf_loc
    xticks_label = [f"{year}"[2:] for conf in venues for year in years] + [f"\n{conf}" for conf in venues]
    plt.xticks(xticks_loc, xticks_label, fontsize=TICK_SIZE)
    plt.tight_layout()
    # plt.savefig(filename, bbox_inches="tight")
    # save to gray style pdf
    plt.savefig(filename, bbox_inches="tight")

def figure_document_situation(filename):
    with open("data/documentary_fills.json", "r") as f:
        documentary_fills = json.load(f)
        
    categories = [
        "completeness",
        "structure",
        "usability",
        "use_example",
        "certificate",
        "contact",
    ]
    category_labels = [
        "Complete.", # Completeness
        "Struct.", # Structure
        "Usability",
        "Example",
        "Cert.", # Certificate
        "Contact",
    ]

    total_counts = {category: 0 for category in categories}
    total_doc_num = len(documentary_fills)
    for paper in documentary_fills:
        for category in categories:
            if paper[category] == "Y":
                total_counts[category] += 1
    total_counts = {category: total_counts[category] / total_doc_num * 100 for category in categories}

    # draw the bar
    plt.figure(figsize=(5, 2))
    plt.bar(category_labels, total_counts.values(), label="Meet the Standard")
    plt.legend(fontsize=TICK_SIZE)

    # text on the bar
    for i, (category, count) in enumerate(total_counts.items()):
        plt.text(i, count+1, f"{count:.1f}%", ha="center", fontsize=MEDIUM_SIZE)
    plt.xticks(fontsize=TICK_SIZE)
    plt.ylim(0, 100)
    plt.yticks(fontsize=TICK_SIZE)
    plt.ylabel("Percentage (%)", fontsize=LABEL_SIZE)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")


def table_issue_distribution(filename):
    """
    Table 4
    The distribution of issue numbers of SE artifacts from 2017 to
    2022. Each number presents the ratio of artifacts whose star
    numbers belong to the range in the first column.
    """
    issue_ranges = [(0, 0), (1, 5), (6, 10), (11, 20), (21, 50), (51, 100), (100, -1)]

    def get_issue_range(index) -> Tuple[str, Callable[[int], bool]]:
        if index == 0:
            return "0", lambda x: x == 0
        if index == 6:
            return "100+", lambda x: x >= 100
        l, r = issue_ranges[index]
        return f"{l}-{r}", lambda x: l <= x <= r

    def get_issue_index(issue):
        for i in range(len(issue_ranges)):
            _, func = get_issue_range(i)
            if func(issue):
                return i
        return -1

    df = pd.DataFrame(papers)
    df["github_issues"] = df.apply(lambda x: x["github_issues"]+x["github_open_issues"] if x["github_issues"] else 0, axis=1)
    df = df[df["github_issues"].notnull()]
    df["issue_index"] = df.apply(lambda x: get_issue_index(x["github_issues"]), axis=1)

    df = df.groupby("year")["issue_index"].value_counts().unstack(fill_value=0)
    total = df.sum().sum()

    last_row = ["average"]
    for i in range(len(issue_ranges)):
        last_row.append("%.1lf%%" % (df.loc[:, i].sum() / total * 100))

    df = df.div(df.sum(axis=1), axis=0).multiply(100)

    writer = csv.writer(open(filename, "w"))

    head_row = ["year"] + [get_issue_range(i)[0] for i in range(len(issue_ranges))]
    writer.writerow(head_row)

    for year in years:
        row = [year]
        for i in range(len(issue_ranges)):
            row.append("%.1lf%%" % df.loc[year, i])
        writer.writerow(row)

    writer.writerow(last_row)


def table_fork_distribution(filename):
    fork_ranges = [(0, 0), (1, 5), (6, 10), (11, 20), (21, 50), (51, 100), (100, -1)]

    def get_fork_range(index) -> Tuple[str, Callable[[int], bool]]:
        if index == 0:
            return "0", lambda x: x == 0
        if index == 6:
            return "100+", lambda x: x >= 100
        l, r = fork_ranges[index]
        return f"{l}-{r}", lambda x: l <= x <= r

    def get_fork_index(fork):
        for i in range(len(fork_ranges)):
            _, func = get_fork_range(i)
            if func(fork):
                return i
        return -1

    df = pd.DataFrame(papers)
    df = df[df["github_fork"].notnull()]
    df["fork_index"] = df.apply(lambda x: get_fork_index(x["github_fork"]), axis=1)
    df = df.groupby("year")["fork_index"].value_counts().unstack(fill_value=0)
    total = df.sum().sum()

    last_row = ["average"]
    for i in range(len(fork_ranges)):
        last_row.append("%.1lf%%" % (df.loc[:, i].sum() / total * 100))

    df = df.div(df.sum(axis=1), axis=0).multiply(100)

    writer = csv.writer(open(filename, "w"))

    head_row = ["year"] + [get_fork_range(i)[0] for i in range(len(fork_ranges))]
    writer.writerow(head_row)

    for year in years:
        row = [year]
        for i in range(len(fork_ranges)):
            row.append("%.1lf%%" % df.loc[year, i])
        writer.writerow(row)

    writer.writerow(last_row)

figures = [
    # figure_ratio_with_artifact,
    # figure_distribution_storage_website,
    # figure_artifact_by_programming_language,
    # [figure_url_location, figure_url_format],
    # figure_invalid_url_ratio_by_year,
    # figure_invalid_url_ratio_by_storage_website,
    # [figure_java_code_smell, figure_python_code_smell],
    # figure_artifact_ratio_by_conference_and_year,
    # figure_document_situation,
]

tables = [
    # table_artifact_ratio_by_conference_and_year,
    # table_maintenance_situation,
    table_star_distribution,
    # table_document_situation,
    # table_top_code_smell,
    table_issue_distribution,
    table_fork_distribution,
]

def draw():
    for idx, figure in enumerate(figures, 1):
        if isinstance(figure, list):
            for label, subfigure in zip('abcdefg', figure):
                filename = f"{OUTPUT_DIR}/figure_{idx}{label}.pdf"
                if not OVERRIDE and os.path.exists(filename):
                    continue
                print(f"drawing figure {idx}{label}: {subfigure.__name__}")
                subfigure(filename)
        else:
            filename = f"{OUTPUT_DIR}/figure_{idx}.pdf"
            if not OVERRIDE and os.path.exists(filename):
                continue
            print(f"drawing figure {idx}: {figure.__name__}")
            figure(filename)

    for idx, table in enumerate(tables, 1):
        filename = f"{OUTPUT_DIR}/table_{idx}.csv"
        if not OVERRIDE and os.path.exists(filename):
            continue
        print(f"drawing table {idx}: {table.__name__}")
        table(filename)

if __name__ == "__main__":
    draw()
