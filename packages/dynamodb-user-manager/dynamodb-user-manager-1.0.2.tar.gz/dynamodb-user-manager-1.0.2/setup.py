#!/usr/bin/env python3
import os.path
from setuptools import setup

project_root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(project_root, "README.md"), encoding="utf-8") as fd:
    readme = fd.read()

setup(
    name="dynamodb-user-manager",
    description="Manage the local user database from DynamoDB",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="1.0.2",
    packages=["dynamodbusermanager"],
    entry_points={
        "console_scripts": [
            "dynamodb-user-manager = dynamodbusermanager.cli:main",
            "dynamodb-user-export = dynamodbusermanager.export:main",
        ]
    },
    install_requires=["boto3>=1.16","daemonize>=2.5.0","requests>=2.25"],
    tests_require=["coverage>=5.3", "moto>=1.3.16", "mypy>=0.790", "nose>=1.3.7", "pylint>=2.6.0"],
    python_requires=">=3.6",
    zip_safe=False,
    author="David Cuthbert",
    author_email="dacut@kanga.org",
    license="Apache-2.0",
    url="https://github.com/dacut/dynamodb-user-manager",
)
