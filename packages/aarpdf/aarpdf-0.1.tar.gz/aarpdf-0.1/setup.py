# this is for publishing this to pypi
# we wand setup.py file in root
# import the setuptools installed earlier
# pass the keyword arguments
import setuptools
from pathlib import Path
setuptools.setup(
    name="aarpdf",
    version=0.1,
    # below description must be the content of the readme file so add Path
    long_descrption=Path("README.md").read_text(),
    # finally we have to say what packages we need to distribute
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
# what we put in read me file will show up in the homepage of the pypi
# also we need a licence file in the root of the poject
# 1)go to choosealicence.com ->sharing improvements->copytoclipboard and paste that in licence file
#############-----#############

# now we must generate a distribution package 1)source distribution 2)build distribution
# open terminal and type "python setup.py sdist bdist_wheel"
