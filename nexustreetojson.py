import numpy
import nexusformat.nexus as nexus
import json


class NexusToDictConverter(object):
    """ Class used to convert nexus format root to python dict
    """

    def __init__(self):
        self._kafka_streams = {}

    def convert(self, nexus_root, streams):
        """ Converts the given nexus_root to dict with correct replacement of
         the streams
        :param nexus_root
        :param streams:
        :return: dictionary
        """
        self._kafka_streams = streams
        return {
            "children": [self._root_to_dict(entry)
                         for _, entry in nexus_root.entries.items()]
        }

    def _root_to_dict(self, root):
        if hasattr(root, 'entries'):
            root_dict = self._handle_group(root)
        else:
            root_dict = self._handle_dataset(root)

        # Assign the attributes
        if root.attrs:
            for attr_name, attr in root.attrs.items():
                if isinstance(attr, nexus.tree.NXattr):
                    attr = attr.nxdata
                if isinstance(attr, numpy.ndarray):
                    attr = attr.tolist()
                root_dict["attributes"][attr_name] = attr
        return root_dict

    def _handle_group(self, root):
        root_dict = {
            "type": "group",
            "name": root.nxname,
            "attributes": {
                "NX_class": root.nxclass
            },
            "children": []
        }
        # Add the entries
        entries = root.entries
        if root.nxpath in self._kafka_streams:
            root_dict["children"].append({
                "type": "stream",
                "stream": self._kafka_streams[root.nxpath]
            })
        elif entries:
            for entry in entries:
                child_dict = self._root_to_dict(entries[entry])
                root_dict["children"].append(child_dict)

        return root_dict

    @staticmethod
    def _handle_dataset(root):
        data = root.nxdata
        dataset_type = str(root.dtype)
        if isinstance(data, numpy.ndarray):
            data = data.tolist()
        if dataset_type[:2] == '|S':
            data = data.decode('utf-8')
            dataset_type = 'str'

        root_dict = {
            "type": "dataset",
            "name": root.nxname,
            "dataset": {
                "type": dataset_type
            },
            "values": data,
            "attributes": {}
        }
        return root_dict


def tree_to_json_file(tree_dict, filename):
    """
    Create a JSON file describing the NeXus file
    WARNING, output files can easily be 10 times the size of input NeXus file

    :param tree_dict: Root node of the tree
    :param filename: Name for the output file
    """
    with open(filename, 'w') as outfile:
        json.dump(tree_dict, outfile, indent=2, sort_keys=False)


if __name__ == '__main__':

    event_data_path = "/raw_data_1/detector_1_events"
    event_data_stream_options = {
        "topic": "TEST_events",
        "source": "TEST",
        "nexus_path": event_data_path
    }
    streams = {event_data_path: event_data_stream_options}

    converter = NexusToDictConverter()
    nexus_file = nexus.nxload("nexus_files/SANS2D_example.nxs")
    tree = converter.convert(nexus_file, streams)
    tree_to_json_file(tree, "SAN2D_example2.json")
