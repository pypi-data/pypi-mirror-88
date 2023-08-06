from setuptools import setup, find_packages
import os
import json
from datetime import datetime

here = os.path.abspath(os.path.dirname(__file__))

# if os.path.isfile(os.path.join(here, 'version.json')):
#     with open("version.json", "r") as f:
#         version = json.load(f)
# else:
#     version = {"major": 0, "minor": 1, "patch": 2}
version_file = os.path.join(here, 'version.json')
with open(version_file, "r") as f:
    version = json.load(f)
version_name = '{major}.{minor}.{patch}'.format(**version)

# Get the long description from the README file
desc_file = os.path.join(here, 'pip_description.md')
with open(desc_file, "r", encoding='utf-8') as f:
    long_description = f.read()
    long_description = long_description.format(pypi_metdata_release_date=datetime.today().strftime('%Y-%m-%d'), pypi_metdata_version_number=version_name)

if os.path.isfile(os.path.join(here, 'requirements.txt')):
    with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        pipreq = f.readlines()
        # remove pip flag
        if '-i http' in pipreq[0]:
            pipreq.pop(0)
else:
    pipreq = []


setup(
    name="pickle_rick",
    version=version_name,
    description='Tools for pickling Python objects in completely different way',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license='Apache 2.0',
    keywords = ['Pickle', 'Python'],
    author='Zipfian Science',
    author_email='about@zipfian.science',
    zip_safe=False,
    # url='https:/zipfian.science',
    download_url='https://github.com/Zipfian-Science/pickle-rick/archive/v_01.tar.gz',
    packages=find_packages(".", exclude=("tests", "dist", "deploy", "egg-info")),
    include_package_data=True,
    install_requires=pipreq,
    package_dir={'.': 'pickle_rick'},
    data_files={
        "setup": ["*.yaml", version_file, desc_file],
    },
    classifiers=[
            'Intended Audience :: Science/Research',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Artificial Intelligence']
)
