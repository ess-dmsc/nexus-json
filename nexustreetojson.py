import nexusformat.nexus


def name_to_json(tree, indent=0):
    return ' ' * indent + '"name": "' + tree.nxname + '"'


def attrs_to_json(tree, indent=0):
    names = sorted(tree.attrs)
    result = ['\"attributes\": [']
    for k in names:
        txt1 = u' ' * indent
        txt2 = u'"' + k
        if nexusformat.nexus.tree.is_text(tree.attrs[k]):
            txt3 = u'" = "' + nexusformat.nexus.tree.text(tree.attrs[k]) + '"'
        else:
            txt3 = u'" = ' + nexusformat.nexus.tree.text(tree.attrs[k])
        txt = (txt1 + txt2 + txt3).replace("u'", "'")
        result.append(txt)
    result.append(']')
    return '\n'.join(result)


def tree_to_json(tree, indent=0):
    result = [indent * ' ' + '{', name_to_json(tree, indent=indent + 2)]
    if tree.attrs:
        result.append(attrs_to_json(tree, indent=indent + 4))

    if hasattr(tree, 'entries'):
        entries = tree.entries
        if entries:
            result.append((indent + 2) * ' ' + '"children": [')
            names = sorted(entries)
            for k in names:
                result.append(tree_to_json(entries[k], indent=indent + 4))
            result.append((indent + 2) * ' ' + ']')

    result.append(indent * ' ' + '}')
    return '\n'.join(result)


if __name__ == '__main__':
    nexus_file = nexusformat.nexus.nxload('nexus_files/SANS2D_example.nxs')
    print(tree_to_json(nexus_file))
