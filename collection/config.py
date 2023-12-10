conferences = ["ICSE", "ASE", "ISSTA", "FSE"]
years = range(2017, 2023) # 2017 ~ 2022

url_template = {
    "ICSE": "https://dblp.org/db/conf/icse/icse%d.html",
    "ASE": "https://dblp.org/db/conf/kbse/ase%d.html",
    "FSE": "https://dblp.org/db/conf/sigsoft/fse%d.html",
    "ISSTA": "https://dblp.org/db/conf/issta/issta%d.html"
}

entry_classes = {
    venue: "entry inproceedings" for venue in conferences
}
