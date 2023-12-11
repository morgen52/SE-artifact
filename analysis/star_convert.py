import openpyxl


def top_starred_transfer(): # transfer data from data/top_starred_fill.xlsx to csv
    wb = openpyxl.load_workbook("data/top_starred_fills.xlsx")
    ws = wb.active
    result = []
    for idx, row in enumerate(ws.rows):
        result.append([cell.value for cell in row])
    
    with open("data/top_starred_fills.csv", "w") as f:
        for row in result:
            f.write("\t".join([str(x) for x in row]) + "\n")

if __name__ == "__main__":
    top_starred_transfer()