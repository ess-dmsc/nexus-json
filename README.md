# NeXus-JSON

Produce JSON schema for NeXus files using [nexusformat](https://github.com/nexpy/nexusformat). The schema are intended to be used with our [NeXus file writer](https://github.com/ess-dmsc/kafka-to-nexus).

Written and tested with Python 3.5 only.
Dependencies can be installed with `pip`:
```
pip install -r requirements.txt
```

### Example usage

Produce a JSON schema from an existing file:
```python
from nexustreetojson import tree_to_json
from nexusformat.nexus import nxload

nexus_file = nxload('nexus_files/SANS2D_example.nxs')
json_schema = tree_to_json(nexus_file) 
print(json_schema)

```

Produce a JSON schema from a NeXus tree built using nexusformat:
```python
from nexustreetojson import tree_to_json
from nexusformat.nexus import *

tree = NXentry(NXsample(temperature=40.0),
               NXinstrument(NXdetector(distance=10.8)))
json_schema = tree_to_json(tree) 
print(json_schema)

```
