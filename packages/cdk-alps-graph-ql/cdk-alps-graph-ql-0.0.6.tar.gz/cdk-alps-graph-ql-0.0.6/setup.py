import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-alps-graph-ql",
    "version": "0.0.6",
    "description": "cdk-alps-graph-ql",
    "license": "Apache-2.0",
    "url": "https://github.com/mmuller88/cdk-alps-graph-ql.git",
    "long_description_content_type": "text/markdown",
    "author": "Martin Mueller<damadden88@googlemail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mmuller88/cdk-alps-graph-ql.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_alps_graph_ql",
        "cdk_alps_graph_ql._jsii"
    ],
    "package_data": {
        "cdk_alps_graph_ql._jsii": [
            "cdk-alps-graph-ql@0.0.6.jsii.tgz"
        ],
        "cdk_alps_graph_ql": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-appsync>=1.75.0, <2.0.0",
        "aws-cdk.aws-iam>=1.75.0, <2.0.0",
        "aws-cdk.core>=1.75.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.16.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
