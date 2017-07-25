import nexusformat.nexus


def name_to_json(tree, indent=0):
    return ' ' * indent + '"name": "' + tree.nxname + '"'


def attrs_to_json():
    pass


def tree_to_json(tree, indent=0):
    result = [indent * ' ' + '{', name_to_json(tree, indent=indent + 2)]
    if tree.attrs:
        result.append(tree._str_attrs(indent=indent + 4))

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


if __name__ == "__main__":
    nexus_file = nexusformat.nexus.nxload('nexus_files/SANS2D_example.nxs')
    print(tree_to_json(nexus_file))
