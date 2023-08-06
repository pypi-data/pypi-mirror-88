import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="scrapper-cf",
    version="1.0.4",
    description="This is one of the many packages that Codefree.io will release. This Packages is aimed at speeding up making of scrappers.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://test.pypi.org/manage/project/scrapper-cf/release/1.0.11/",
    author="Codefree.io",
    author_email="wilson@codefree.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["scrapper"],
    include_package_data=True,
    install_requires=[''],
    # data_files=[('Data', ['user_agents.csv'])],
    # package_data={'Scrapper': ['Data/*.csv']},
    python_requires='>3.5'
   
)