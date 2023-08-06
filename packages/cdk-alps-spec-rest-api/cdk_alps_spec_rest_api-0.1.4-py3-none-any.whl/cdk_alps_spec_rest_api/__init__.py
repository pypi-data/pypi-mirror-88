"""
[![NPM version](https://badge.fury.io/js/cdk-alps-spec-rest-api.svg)](https://badge.fury.io/js/cdk-alps-spec-rest-api)
[![PyPI version](https://badge.fury.io/py/cdk-alps-spec-rest-api.svg)](https://badge.fury.io/py/cdk-alps-spec-rest-api)
![Release](https://github.com/mmuller88/cdk-alps-spec-rest-api/workflows/Release/badge.svg)

# CDK Alps Spec Rest Api

The CDK Alps Spec Rest Api construct generates an AWS API Gateway out of an ALPS API yaml file such src/todo-alps.yaml. ALPS API is an abstraction of APIs like REST API or Graph QL. More about the ALPS API see in the ALPS API section.

The AWS CDK construct repo was generated with [Projen](https://github.com/projen/projen) as **awscdk-construct**

# Thanks

* To Pahud for the helpful AWS CDK Construct video: https://www.youtube.com/watch?v=cTsSXYOYQPw
* Mike Amundsen for the ALPS API idea and help

# ALPS API

The ALPS API converter is on GitHub on: https://github.com/mamund/alps-unified

Very useful to understand the idea of ALPS API is this video on YouTube: https://www.youtube.com/watch?v=oG6-r3UdenE

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "my-demo-stack", env=env)

AlpsSpecRestApi(stack, "AlpsSpecRestApi",
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

* (AWS) Authorizer and Validator are not supported yet
* only alps YAML files are supported. alps JSON files will be added
* only Lambda integrations are supported and the endpoints are per default mapped to lambdas with the same name as the operationId.
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

import aws_cdk.core


class AlpsSpecRestApi(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-alps-spec-rest-api.AlpsSpecRestApi",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        alps_spec_file: builtins.str,
        operation_id_lambda_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param alps_spec_file: ALPS Spec File. Must be YAML.
        :param operation_id_lambda_mapping: Optional mapping from openApi spec operationId to Lambda name. Per default it uses a Lambda integration with using the openApi spec operationId property as Lambda name
        """
        props = AlpsSpecRestApiProps(
            alps_spec_file=alps_spec_file,
            operation_id_lambda_mapping=operation_id_lambda_mapping,
        )

        jsii.create(AlpsSpecRestApi, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="operationIdLambdaMapping")
    def operation_id_lambda_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return jsii.get(self, "operationIdLambdaMapping")

    @operation_id_lambda_mapping.setter # type: ignore
    def operation_id_lambda_mapping(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        jsii.set(self, "operationIdLambdaMapping", value)


@jsii.data_type(
    jsii_type="cdk-alps-spec-rest-api.AlpsSpecRestApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "alps_spec_file": "alpsSpecFile",
        "operation_id_lambda_mapping": "operationIdLambdaMapping",
    },
)
class AlpsSpecRestApiProps:
    def __init__(
        self,
        *,
        alps_spec_file: builtins.str,
        operation_id_lambda_mapping: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """
        :param alps_spec_file: ALPS Spec File. Must be YAML.
        :param operation_id_lambda_mapping: Optional mapping from openApi spec operationId to Lambda name. Per default it uses a Lambda integration with using the openApi spec operationId property as Lambda name
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alps_spec_file": alps_spec_file,
        }
        if operation_id_lambda_mapping is not None:
            self._values["operation_id_lambda_mapping"] = operation_id_lambda_mapping

    @builtins.property
    def alps_spec_file(self) -> builtins.str:
        """ALPS Spec File.

        Must be YAML.
        """
        result = self._values.get("alps_spec_file")
        assert result is not None, "Required property 'alps_spec_file' is missing"
        return result

    @builtins.property
    def operation_id_lambda_mapping(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Optional mapping from openApi spec operationId to Lambda name.

        Per default it uses a Lambda integration with using the openApi spec operationId property as Lambda name
        """
        result = self._values.get("operation_id_lambda_mapping")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlpsSpecRestApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AlpsSpecRestApi",
    "AlpsSpecRestApiProps",
]

publication.publish()
