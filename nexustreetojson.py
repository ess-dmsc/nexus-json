import nexusformat.nexus
import json
import numpy as np


def _name_to_json(tree):
    return '"name": "' + tree.nxname + '"'


def _is_array(possible_array):
    return isinstance(possible_array, np.ndarray)


def _attrs_to_json(tree):
    names = sorted(tree.attrs)
    result = []
    for k in names:
        txt1 = u'{"' + k
        if nexusformat.nexus.tree.is_text(tree.attrs[k]):
            txt2 = u'": "' + nexusformat.nexus.tree.text(tree.attrs[k]) + '"'
        elif _is_array(tree.attrs[k]):
            array_string = np.array2string(tree.attrs[k], separator=', ').replace(' ', '')
            array_string = array_string.replace('.,', '.0,')
            array_string = array_string.replace('.]', '.0]')
            txt2 = u'": ' + array_string
        else:
            txt2 = u'": ' + nexusformat.nexus.tree.text(tree.attrs[k])
        txt = (txt1 + txt2).replace("u'", "'")
        txt += '}'
        result.append(txt)
    result[0] = '\"attributes\": [' + result[0]
    result[-1] += ']'
    return ', '.join(result)


def _tree_to_json_string(tree):
    result = ['{' + _name_to_json(tree)]
    if tree.attrs:
        result.append(_attrs_to_json(tree))

    if hasattr(tree, 'entries'):
        entries = tree.entries
        if entries:
            children = []
            names = sorted(entries)
            for k in names:
                children.append(_tree_to_json_string(entries[k]))
            result.append('"children": [' + ','.join(children) + ']')

    result[-1] += '}'
    return ', '.join(result)


def tree_to_json(tree):
    json_tree = tree_to_json(tree)
    parsed = json.loads(json_tree)
    beautified_json_tree = json.dumps(parsed, indent=4, sort_keys=True)
    print(beautified_json_tree)
    return beautified_json_tree


if __name__ == '__main__':
    nexus_file = nexusformat.nexus.nxload('nexus_files/SANS2D_example.nxs')
    tree_to_json(nexus_file)
