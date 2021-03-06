from setuptools import setup, find_packages

setup(
    name="nicotine",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'google-api-python-client',
        'pickledb'
    ],
    entry_points='''
    [console_scripts]
    nicotine=cli:cli
    '''
)