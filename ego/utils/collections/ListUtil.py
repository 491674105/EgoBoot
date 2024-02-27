
def insert(sl, index, obj):
    length = len(sl)
    last_index = index - 1
    if length == last_index:
        sl.append(obj)
        return

    if length > last_index:
        sl.insert(index, obj)
        return

    differ = last_index - length
    while differ > 0:
        sl.append(-1)
        differ -= 1
    sl.append(obj)
