[![NPM version](https://badge.fury.io/js/cdk-alps-graph-ql.svg)](https://badge.fury.io/js/cdk-alps-graph-ql)
[![PyPI version](https://badge.fury.io/py/cdk-alps-graph-ql.svg)](https://badge.fury.io/py/cdk-alps-graph-ql)
![Release](https://github.com/mmuller88/cdk-alps-graph-ql/workflows/Release/badge.svg)

# CDK Alps Graph QL

The CDK Alps Graph QL construct generates an AWS Graph QL out of an ALPS API yaml file such src/todo-alps.yaml. ALPS API is an abstraction of APIs like REST API or Graph QL. More about the ALPS API see in the ALPS API section.

The AWS CDK construct repo was generated with [Projen](https://github.com/projen/projen) as **awscdk-construct**

# Thanks

* To Pahud for the helpful AWS CDK Construct video: https://www.youtube.com/watch?v=cTsSXYOYQPw
* Mike Amundsen for the ALPS API idea and help.

# ALPS API

The ALPS API converter is on GitHub on: https://github.com/mamund/alps-unified

Very useful to understand the idea of ALPS API is this video on YT: https://www.youtube.com/watch?v=oG6-r3UdenE

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "alps-graph-ql-stack", env=env)

AlpsGraphQL(stack, "AlpsGraphQL",
    name="demo",
    alps_spec_file="src/todo-alps.yaml"
)
```

# CDK stack commands

## Diff

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
npxcdk --applib / integ.default.js --profile < profile > diff
```

## Deploy

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
npxcdk --applib / integ.default.js --profile < profile > deploy
```

## Destroy

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
npxcdk --applib / integ.default.js --profile < profile > destroy
```

# Limitations / Issues / TODOS

* only ALPS YAML files are supported. ALPS JSON files will be added
