from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='elasticsearch-tocsv',
    version='0.9.0',
    description='Simple python tool to extract massive amounts of documents from Elasticsearch into a csv file exploiting multiprocessing and leveraging the underneath elasticsearch-py package',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/fabiopipitone/elasticsearch-tocsv',
    author='Fabio Pipitone',
    author_email='fabio.pipitone93@gmail.com',
    keywords='elasticsearch, export, csv, report, kibana, elasticsearch-py',
    package_dir={'': 'elasticsearch-tocsv'},
    packages=find_packages(where='elasticsearch-tocsv'),
    python_requires='>=3.5, <4',
    install_requires=['requests>==2.22.0', 'elasticsearch>=7.9.1', 'tqdm>=4.49.0', 'pandas>=1.1.2', 'pytz>=2020.1'],
    entry_points={ 
        'console_scripts': [
            'elasticsearch-tocsv=elasticsearch-tocsv.elasticsearch-tocsv:main',
        ],
    },
)