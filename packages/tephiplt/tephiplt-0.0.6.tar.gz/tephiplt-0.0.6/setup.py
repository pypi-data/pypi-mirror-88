'''module to state tephiplt package metadata'''
from setuptools import setup
from setuptools import find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tephiplt",
    version="0.0.6",
    author="Simon O'Meara",
    author_email="simon.omeara@manchester.ac.uk",
    description="plotting a tephigram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['python', 'meteorology', 'tephigram', 'atmospheric physics'],
    url="https://github.com/simonom/outreach",
    packages = find_packages(include=['tephiplt']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    
# state dependencies for tephiplt
install_requires=["numpy","matplotlib","ipdb","scipy"]
)