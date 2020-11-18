from setuptools import setup

setup(
    name='yourscript',
    version='0.1',
    py_modules=['script'],
    install_requires=['Click', 'boto3'],
    entry_points='''
        [console_scripts]
        boto_script=boto_script:cli
    ''',
)