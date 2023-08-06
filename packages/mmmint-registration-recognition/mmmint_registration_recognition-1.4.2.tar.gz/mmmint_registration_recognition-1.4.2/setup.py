from setuptools import setup, find_packages

import os
import re

WORKFLOW_RELEASE = "Release"
NAME_PROD = "mmmint_registration_recognition"
NAME_DEV = "mmmint_registration_recognition"


def getVariables():

    workflow_name = os.environ.get("GITHUB_WORKFLOW", "")

    if WORKFLOW_RELEASE == workflow_name:
        version = getVersionProd()
        name = NAME_PROD
    else:
        version = getVersionDev()
        name = NAME_DEV

    return name, version


def getVersionProd():
    REF_PREFIX = "refs/tags/"

    github_ref = os.environ.get("GITHUB_REF", 'refs/tags/0')
    return re.sub(REF_PREFIX, '', github_ref)


def getVersionDev():
    return os.environ.get("GITHUB_RUN_NUMBER", "0")


with open("sdk/mmmint/README.md", "r") as fh:
    long_description = fh.read()

with open('sdk/mmmint/requirements.txt') as f:
    required = f.read().splitlines()

NAME, VERSION = getVariables()

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
]

setup(
    name=NAME,
    version=VERSION,
    author="MMM Intelligence UG",
    author_email="info@mrfiktiv.com",
    classifiers=CLASSIFIERS,
    description="An interface to execute Fahrzeugschein API commands using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://api.mmmint.ai/fahrzeugschein/v1/docs",
    package_dir={'': 'sdk'},
    packages=find_packages(where='sdk'),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=required
)
