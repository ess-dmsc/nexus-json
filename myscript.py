import nexusformat.nexus as nexus
from nexusjson.nexus_to_json import NexusToDictConverter, object_to_json_file
converter = NexusToDictConverter()
nexus_file = nexus.nxload("/Users/georgeoneill/ess-dmsc/hdf5-json/fixed_ymir_doubleFix.hdf")
tree = converter.convert(nexus_file, {}, {})
object_to_json_file(tree, "output_nexusjson.json")
