""""Convert HDF files produced at ESS back to the JSON template"""
import json
import numpy as np
from nexusformat import nexus


class NexusToDictConverter:
    """
    Class used to convert nexus format root to python dict
    """

    def __init__(self, truncate_large_datasets: bool = False, large: int = 10):
        """
        :param truncate_large_datasets: if True truncates datasets with any dimension larger than large
        :param large: dimensions larger than this are considered large
        """
        self.truncate_large_datasets = truncate_large_datasets
        self.large = large

    def convert(self, nexus_root: nexus.NXroot) -> dict:
        """
        Converts the given nexus_root to dict with correct replacement of
        the streams
        :param nexus_root
        :return: dictionary
        """
        return {
            "children": [self._root_to_dict(entry)
                         for _, entry in nexus_root.entries.items()]
        }

    def _root_to_dict(self, root: nexus.NXgroup) -> dict:
        if hasattr(root, 'entries'):
            root_dict = self._handle_group(root)
        else:
            root_dict = self._handle_dataset(root)

        root_dict = self._handle_attributes(root, root_dict)
        return root_dict

    @staticmethod
    def truncate_if_large(size, data):
        """
        :param size: new maximum dimension
        :param data: data to shrink
        """
        for dim_number, dim_size in enumerate(size):
            if dim_size > 10:
                size[dim_number] = 10
        data.resize(size)

    def _get_data_and_type(self, root):
        size = 1
        data = root.nxdata
        dtype = str(root.dtype)
        if isinstance(data, np.ndarray):
            size = data.shape
            if self.truncate_large_datasets:
                self.truncate_if_large(size, data)
            data = data.tolist()
        if isinstance(data, (list, tuple)) and len(data) == 1:
            data = data[0]
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        if dtype[:2] == '|S':
            if isinstance(data, list):
                data = [str_item.decode('utf-8') for str_item in data]
            dtype = "string"
        elif dtype == "float64":
            dtype = "double"
        elif dtype == "float32":
            dtype = "float"
        if dtype == "object":
            dtype = "string"
        if isinstance(data, list):
            data = [float(piece) if isinstance(piece, str) and piece.replace('.', '').isnumeric() else piece for piece in data]
        elif isinstance(data, str) and data.replace('.', '').isnumeric():
            data = float(data)
        return data, dtype

    def _handle_attributes(self, root, root_dict):
        if root.nxclass and root.nxclass != "NXfield" and root.nxclass != "NXgroup":
            root_dict["attributes"] = [{"name": "NX_class",
                                        "values": root.nxclass}]
        if root.attrs:
            if "attributes" not in root_dict:
                root_dict["attributes"] = []

            for attr_name, attr in root.attrs.items():
                data, dtype = self._get_data_and_type(attr)
                new_attribute = {"name": attr_name,
                                 "values": data}
                if dtype != "object":
                    new_attribute["type"] = dtype
                root_dict["attributes"].append(new_attribute)
        return root_dict

    def _handle_group(self, root):
        root_dict = {
            "type": "group",
            "name": root.nxname,
            "children": []
        }
        # Add the entries
        entries = root.entries
        if entries:
            for entry in entries:
                child_dict = self._root_to_dict(entries[entry])
                root_dict["children"].append(child_dict)

        return root_dict

    def _handle_dataset(self, root):
        data, dataset_type = self._get_data_and_type(root)
        root_dict = {
            "module": "dataset",
            "config": {
                "name": root.nxname,
                "type": dataset_type,
                "values": data
            }
        }

        return root_dict


def object_to_json_file(tree_dict, filename):
    """
    Create a JSON file describing the NeXus file
    WARNING, output files can easily be 10 times the size of input NeXus file

    :param tree_dict: Root node of the tree
    :param filename: Name for the output file
    """
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(tree_dict, outfile, indent=2, sort_keys=False)
