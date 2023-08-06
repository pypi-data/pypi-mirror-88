"""
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_appsync
import aws_cdk.core


class AlpsGraphQL(
    aws_cdk.aws_appsync.GraphqlApi,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-alps-graph-ql.AlpsGraphQL",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        alps_spec_file: builtins.str,
        name: builtins.str,
        authorization_config: typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig] = None,
        log_config: typing.Optional[aws_cdk.aws_appsync.LogConfig] = None,
        schema: typing.Optional[aws_cdk.aws_appsync.Schema] = None,
        xray_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param alps_spec_file: ALPS Spec File. Must be YAML.
        :param name: (experimental) the name of the GraphQL API.
        :param authorization_config: (experimental) Optional authorization configuration. Default: - API Key authorization
        :param log_config: (experimental) Logging configuration for this api. Default: - None
        :param schema: (experimental) GraphQL schema definition. Specify how you want to define your schema. Schema.fromFile(filePath: string) allows schema definition through schema.graphql file Default: - schema will be generated code-first (i.e. addType, addObjectType, etc.)
        :param xray_enabled: (experimental) A flag indicating whether or not X-Ray tracing is enabled for the GraphQL API. Default: - false
        """
        props = AlpsGraphQLProps(
            alps_spec_file=alps_spec_file,
            name=name,
            authorization_config=authorization_config,
            log_config=log_config,
            schema=schema,
            xray_enabled=xray_enabled,
        )

        jsii.create(AlpsGraphQL, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-alps-graph-ql.AlpsGraphQLProps",
    jsii_struct_bases=[aws_cdk.aws_appsync.GraphqlApiProps],
    name_mapping={
        "name": "name",
        "authorization_config": "authorizationConfig",
        "log_config": "logConfig",
        "schema": "schema",
        "xray_enabled": "xrayEnabled",
        "alps_spec_file": "alpsSpecFile",
    },
)
class AlpsGraphQLProps(aws_cdk.aws_appsync.GraphqlApiProps):
    def __init__(
        self,
        *,
        name: builtins.str,
        authorization_config: typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig] = None,
        log_config: typing.Optional[aws_cdk.aws_appsync.LogConfig] = None,
        schema: typing.Optional[aws_cdk.aws_appsync.Schema] = None,
        xray_enabled: typing.Optional[builtins.bool] = None,
        alps_spec_file: builtins.str,
    ) -> None:
        """
        :param name: (experimental) the name of the GraphQL API.
        :param authorization_config: (experimental) Optional authorization configuration. Default: - API Key authorization
        :param log_config: (experimental) Logging configuration for this api. Default: - None
        :param schema: (experimental) GraphQL schema definition. Specify how you want to define your schema. Schema.fromFile(filePath: string) allows schema definition through schema.graphql file Default: - schema will be generated code-first (i.e. addType, addObjectType, etc.)
        :param xray_enabled: (experimental) A flag indicating whether or not X-Ray tracing is enabled for the GraphQL API. Default: - false
        :param alps_spec_file: ALPS Spec File. Must be YAML.
        """
        if isinstance(authorization_config, dict):
            authorization_config = aws_cdk.aws_appsync.AuthorizationConfig(**authorization_config)
        if isinstance(log_config, dict):
            log_config = aws_cdk.aws_appsync.LogConfig(**log_config)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "alps_spec_file": alps_spec_file,
        }
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config
        if log_config is not None:
            self._values["log_config"] = log_config
        if schema is not None:
            self._values["schema"] = schema
        if xray_enabled is not None:
            self._values["xray_enabled"] = xray_enabled

    @builtins.property
    def name(self) -> builtins.str:
        """(experimental) the name of the GraphQL API.

        :stability: experimental
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def authorization_config(
        self,
    ) -> typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig]:
        """(experimental) Optional authorization configuration.

        :default: - API Key authorization

        :stability: experimental
        """
        result = self._values.get("authorization_config")
        return result

    @builtins.property
    def log_config(self) -> typing.Optional[aws_cdk.aws_appsync.LogConfig]:
        """(experimental) Logging configuration for this api.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("log_config")
        return result

    @builtins.property
    def schema(self) -> typing.Optional[aws_cdk.aws_appsync.Schema]:
        """(experimental) GraphQL schema definition. Specify how you want to define your schema.

        Schema.fromFile(filePath: string) allows schema definition through schema.graphql file

        :default: - schema will be generated code-first (i.e. addType, addObjectType, etc.)

        :stability: experimental
        """
        result = self._values.get("schema")
        return result

    @builtins.property
    def xray_enabled(self) -> typing.Optional[builtins.bool]:
        """(experimental) A flag indicating whether or not X-Ray tracing is enabled for the GraphQL API.

        :default: - false

        :stability: experimental
        """
        result = self._values.get("xray_enabled")
        return result

    @builtins.property
    def alps_spec_file(self) -> builtins.str:
        """ALPS Spec File.

        Must be YAML.
        """
        result = self._values.get("alps_spec_file")
        assert result is not None, "Required property 'alps_spec_file' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlpsGraphQLProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AlpsGraphQL",
    "AlpsGraphQLProps",
]

publication.publish()
