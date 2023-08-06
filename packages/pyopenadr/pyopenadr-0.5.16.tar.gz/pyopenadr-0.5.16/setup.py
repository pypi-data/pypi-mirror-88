from setuptools import setup

long_description="""# PyOpenADR

PyOpenADR has changed its name to [OpenLEADR](https://pypi.org/project/openleadr). You can still use pyopenadr as an alias to openleadr if you want.

Please update your dependencies, and please take a look [here](https://pypi.org/project/openleadr). Thanks.
"""

setup(name="pyopenadr",
      description="pyOpenADR is a package that ",
      version='0.5.16',
      url='https://openleadr.org',
      packages=['pyopenadr'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=['openleadr==0.5.16'])
