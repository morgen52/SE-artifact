from pydantic import BaseModel

class DblpPaperRecord(BaseModel):
    title: str
    paper_id: str
    venue: str
    issue: int
    year: int
    urls: list[str]
    doi: str
    pages: int