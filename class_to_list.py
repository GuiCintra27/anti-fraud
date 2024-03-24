def classToList(instanceList: list[object]):
    newList = []

    for instance in instanceList:
        l = list(instance.__dict__.values())
        l[2] = ' / '.join(l[2])
        newList.append(l)

    return newList
