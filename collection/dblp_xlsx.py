import xlsxwriter

from configs.model import DblpPaperRecord

class DblpCsvWriter:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.file = open(filename, "w")
    
    def write_row(self, data: list):
        self.file.write(",".join(data) + "\n")

    def dump_papers(self, papers: list[DblpPaperRecord]):
        self.write_row(
            ["paper_id", "title", "venue", "issue", "year", "urls", "doi", "pages"]
        )
        for paper in papers:
            self.write_row(
                [
                    paper.paper_id,
                    paper.title,
                    paper.venue,
                    str(paper.issue),
                    str(paper.year),
                    ";".join(paper.urls),
                    paper.doi,
                    str(paper.pages),
                ]
            )

    def close(self):
        self.file.close()

class DblpXlsxWriter:
    def __init__(self, filename) -> None:
        self.row = 0
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet = self.workbook.add_worksheet()

    def write_row(self, data: list):
        for index, item in enumerate(data):
            self.worksheet.write(self.row, index, item)
        self.row += 1

    def dump_papers(self, papers: list[DblpPaperRecord]):
        self.write_row(
            ["paper_id", "title", "venue", "issue", "year", "urls", "doi", "pages"]
        )
        for paper in papers:
            self.write_row(
                [
                    paper.paper_id,
                    paper.title,
                    paper.venue,
                    paper.issue,
                    paper.year,
                    ";".join(paper.urls),
                    paper.doi,
                    paper.pages,
                ]
            )

    def close(self):
        self.workbook.close()
    
