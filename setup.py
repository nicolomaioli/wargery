from setuptools import setup, find_packages

setup(
    name='wargery',
    version='1.0',
    description='Create a sensibly named war artifact for a grails project',
    author='Nicolo Maioli',
    author_email='nicolomaioli@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts':['wargery=wargery.app:run']
    }
)
