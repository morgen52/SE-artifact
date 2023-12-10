import difflib

def almost_identical(str1, str2, threshold=0.8):
    similarity_ratio = difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    return similarity_ratio > threshold
