from configs.model import DblpPaperRecord
from typing import Callable

from pydantic import BaseModel
from collection.dblp_xlsx import DblpXlsxWriter, DblpCsvWriter
from utils.file import *

import pandas as pd
from pandas import DataFrame

class DblpDataset(BaseModel):

    paper_list: list[DblpPaperRecord] = []

    def add_paper(self, paper: DblpPaperRecord):
        self.paper_list.append(paper)

    def add_papers(self, papers: list[DblpPaperRecord]):
        self.paper_list.extend(papers)

    def get_paper_list(self) -> list[DblpPaperRecord]:
        return self.paper_list

    def dump_xlsx(self, filename: str):
        xlsx_writer = DblpXlsxWriter(filename)
        xlsx_writer.dump_papers(self.paper_list)
        xlsx_writer.close()

    def dump_csv(self, filename: str):
        csv_writer = DblpCsvWriter(filename)
        csv_writer.dump_papers(self.paper_list)
        csv_writer.close()

    def dump_json(self, filename: str):
        dump_list_pydantic(self.paper_list, filename)
    
    def get_subset(self, predicate: Callable[[DblpPaperRecord], bool]) -> "DblpDataset":
        paper_list = [p for p in self.paper_list if predicate(p)]
        return DblpDataset(paper_list=paper_list)

def load_dblp_dataset_from_json(filename: str) -> DblpDataset:
    paper_list = load_list_pydantic(DblpPaperRecord, filename)
    dblp_dataset = DblpDataset(paper_list=paper_list)
    return dblp_dataset
