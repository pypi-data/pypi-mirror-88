from setuptools import setup, find_namespace_packages

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='dataforge',
    version='0.0.3',
    author='Phil Schumm',
    author_email='pschumm@uchicago.edu',
    description='Tools for creating and packaging data products',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/phs-rcg/data-forge',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'click',
        'click-config-file',
        'confuse',
        'keyring',
        'requests',
        'xmarshal',
        'pandas',
        'gitpython',
    ],
    entry_points='''
        [console_scripts]
        redcap_export=dataforge.sources.redcap.api:export
    ''',
)
