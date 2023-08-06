from setuptools import setup

long_description="""# PyOpenADR

PyOpenADR has changed its name to [OpenLEADR](https://pypi.org/project/openleadr). Installing pyopenadr will simply install the latest version of openLEADR.

Please update your dependencies, and please take a look [here](https://pypi.org/project/openleadr). Thanks.
"""
print("Warning: pyOpenADR has been renamed to openLEADR. Please use that package from now on.")

setup(name="pyopenadr",
      description="PyOpenADR is superseded by OpenLEADR",
      version='0.5.13',
      url='https://openleadr.org',
      packages=['pyopenadr'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=['openleadr==0.5.13'])
