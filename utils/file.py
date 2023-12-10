import json

def load_json(filename):
    return json.load(open(filename))

def dump_json(papers, filename):
    json.dump(papers, open(filename, 'w'), indent=4)

def dump_list_pydantic(ls, filename):
    ls_json = [e.model_dump(mode="json") for e in ls]
    json.dump(ls_json, open(filename, 'w'), indent=4)

def load_list_pydantic(model, filename):
    ls_json = json.load(open(filename))
    ls = [model(**e) for e in ls_json]
    return ls