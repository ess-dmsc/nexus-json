from setuptools import setup

setup(name='nexusjson',
      version='0.1',
      description='Create json representations of NeXus files',
      url='https://github.com/ess-dmsc/nexus-json',
      author='Matthew D Jones',
      license='BSD-2-Clause',
      packages=['nexusjson'],
      zip_safe=False,
      install_requires=['numpy',
                        'nexusformat']
      )
