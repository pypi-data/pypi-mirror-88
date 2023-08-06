from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='parler',
    version='1.0.1',
    description='Parler Social Media Python API SDK',
    url='https://gitlab.com/coffeemaninc/parler-api/',
    author='Caffman',
    author_email='caff@none.com',
    license='MIT',
    packages=['parler'],
    install_requires=['requests'],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
