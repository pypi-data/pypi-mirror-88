def sort_dict_by_values(dictionary,asc=False):
    '''Takes a dictionary and returns it sorted in descending or ascending order'''
    if asc: return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}
    else: return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1],reverse=True)}
