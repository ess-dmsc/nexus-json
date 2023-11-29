import nexusformat.nexus as nexus
from nexusjson.nexus_to_json import NexusToDictConverter, create_writer_commands, object_to_json_file
converter = NexusToDictConverter()
nexus_file = nexus.nxload("/Users/georgeoneill/ess-dmsc/hdf5-json/038243_00010907.hdf")
tree = converter.convert(nexus_file, {}, {})
object_to_json_file(tree, "test.json")
