def find_all_ngrams(tree):
    result = []
    if type(tree) == str:
        return ["LEAF"]
    for child in tree:
        previous = find_all_ngrams(child)
        if previous:
            for prev in previous:
                result.append(prev + " " + tree.label())

    return result
