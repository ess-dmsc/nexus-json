import nexusformat.nexus
import json
import numpy as np


def _name_to_json(tree):
    return '"name": "' + tree.nxname + '"'


def _is_array(possible_array):
    return isinstance(possible_array, np.ndarray)


def _attrs_to_json(tree):
    result = []
    if tree.attrs:
        for k in tree.attrs:
            if nexusformat.nexus.tree.is_text(tree.attrs[k]):
                attr_string = u'": "' + nexusformat.nexus.tree.text(tree.attrs[k]) + '"'
            elif _is_array(tree.attrs[k]):
                array_string = np.array2string(tree.attrs[k], separator=', ').replace(' ', '')
                array_string = array_string.replace('.,', '.0,')
                array_string = array_string.replace('.]', '.0]')
                attr_string = u'": ' + array_string
            else:
                attr_string = u'": ' + nexusformat.nexus.tree.text(tree.attrs[k])
            txt = (u'"' + k + attr_string).replace("u'", "'")
            result.append(txt)
    if tree.nxclass != "NXfield":
        result.append('"NX_class": "' + tree.nxclass + '"')
    if result:
        result[0] = '\"attributes\": {' + result[0]
        result[-1] += '}'
        return_lines = ', '.join(result)
    else:
        return_lines = None
    return return_lines


def _tree_to_json_string(tree):
    result = []
    children_prepend = ""
    children_append = ""
    if tree.nxname is "root" and tree.nxclass is not "NXfield":
        children_prepend = '{"nexus_structure": {'
        children_append = '}'
    else:
        result.append('{' + _name_to_json(tree))
        attrs_json = _attrs_to_json(tree)
        if attrs_json:
            result.append(attrs_json)
        if tree.nxclass is "NXfield":
            result.append('"type": "dataset"')
        else:
            result.append('"type": "group"')

    if hasattr(tree, 'entries'):
        entries = tree.entries
        if entries:
            children = []
            names = sorted(entries)
            for k in names:
                children.append(_tree_to_json_string(entries[k]))
            result.append(children_prepend + '"children": [' + ','.join(children) + ']' + children_append)

    result[-1] += '}'
    return ', '.join(result)


def tree_to_json(tree):
    json_tree = _tree_to_json_string(tree)
    parsed = json.loads(json_tree)
    beautified_json_tree = json.dumps(parsed, indent=2, sort_keys=False)
    return beautified_json_tree


if __name__ == '__main__':
    nexus_file = nexusformat.nexus.nxload('nexus_files/SANS2D_example.nxs')
    json_schema = tree_to_json(nexus_file)
    print(json_schema)
