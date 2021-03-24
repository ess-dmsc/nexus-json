import nexusformat.nexus as nexus
from nexusjson.nexus_to_json import NexusToDictConverter, create_writer_commands, object_to_json_file

"""
Produce JSON commands for the file writer for a SANS2D NeXus file
"""

event_data_path = "/raw_data_1/instrument/detector_1"
event_data_stream_options = {
    "topic": "TEST_events",
    "source": "TEST",
    "module": "ev42",
    "nexus_path": event_data_path
}
streams = {event_data_path: event_data_stream_options}

converter = NexusToDictConverter()
nexus_file = nexus.nxload("nexus_files/SANS2D_example.nxs")
tree = converter.convert(nexus_file, streams, links={})
write_command, stop_command = create_writer_commands(tree, "SANS2D_example_output.nxs")
object_to_json_file(write_command, "SANS2D_example.json")
object_to_json_file(stop_command, "stop_SANS2D_example.json")
