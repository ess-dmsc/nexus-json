"""Controller for NeXus to JSON converter"""
import sys

from nexusformat import nexus
from nexus_json.NexusToDictConverter import NexusToDictConverter, object_to_json_file

def main():
	converter = NexusToDictConverter()
	nexus_file = nexus.nxload(sys.argv[1])  # change this line to your file

	tree = converter.convert(nexus_file)

	if len(sys.argv) > 2:
		output = sys.argv[2]
	else:
		output = "output.json"

	object_to_json_file(tree, output)