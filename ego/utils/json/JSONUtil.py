
def sort_json(src_json):
    tg = {}
    for key in sorted(src_json):
        tg[key] = src_json[key]

    return tg
