# NeXus-JSON

Produce JSON schema for NeXus files using [nexusformat](https://github.com/nexpy/nexusformat). The schema are intended to be used with our [NeXus file writer](https://github.com/ess-dmsc/kafka-to-nexus).

This should work for Python3, but has only been tested against Python 3.11.  It can be run via installation via:

```
pip install .
```

and calling

```
nexus2json INPUT_FILENAME (OUTPUT_FILENAME)
```

If OUTPUT_FILENAME is not given then a default file output.json will be created.