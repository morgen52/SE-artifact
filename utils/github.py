import re

def parse_repository_name(url: str) -> str:
    result = re.match(r"https://github.com/([^/\.]*/[^/\.]*)(:?\.git)?/?", url)                    
    if result:
        return result.group(1)
    else:
        return None


