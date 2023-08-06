import os

from setuptools import setup, find_packages

requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
with open(requirements_path) as requirements_file:
    requirements = requirements_file.readlines()

__version__ = '6.6.6'

setup(
    name='tzflaskoidc',
    version=__version__,
    description='Flask wrapper with pre-configured OIDC support',
    url='https://github.com/verdan/flaskoidc.git',
    author='Verdan Mahmood',
    author_email='verdan.mahmood@gmail.com',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    dependency_links=[],
    install_requires=requirements,
    python_requires=">=3.6",

)
