def safe_list_get(l, idx, default=None):
    try:
        return l[idx]
    except IndexError:
        return default