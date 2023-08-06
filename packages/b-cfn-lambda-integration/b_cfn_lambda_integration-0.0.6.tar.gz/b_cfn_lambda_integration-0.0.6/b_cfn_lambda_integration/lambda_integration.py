import hashlib
from typing import Any
from aws_cdk.aws_apigatewayv2 import CfnIntegration
from aws_cdk.core import Stack


class LambdaIntegration(CfnIntegration):
    def __init__(
            self,
            scope: Stack,
            integration_name: str,
            api: Any,
            lambda_function: Any,
            integration_method: str = 'POST',
            integration_type: str = 'AWS_PROXY',
            connection_type='INTERNET',
            **kwargs
    ) -> None:
        self.__integration_name = integration_name
        self.__integration_method = integration_method
        self.__integration_type = integration_type
        self.__connection_type = connection_type

        try:
            # Works for higher level constructs.
            api_id = api.rest_api_id
        except AttributeError:
            try:
                # Works for CFN resources.
                api_id = api.ref
            except AttributeError:
                raise ValueError('Unsupported api type.')

        try:
            # Works for higher level constructs.
            fun_arn = lambda_function.function_arn
        except AttributeError:
            try:
                # Works for CFN resources.
                fun_arn = lambda_function.attr_arn
            except AttributeError:
                raise TypeError('Unsupported lambda function type.')

        super().__init__(
            scope=scope,
            id=integration_name,
            api_id=api_id,
            connection_type=connection_type,
            integration_type=integration_type,
            integration_method=integration_method,
            integration_uri=f'arn:aws:apigateway:{scope.region}:lambda:path/2015-03-31/functions/{fun_arn}/invocations',
            payload_format_version='1.0',
            **kwargs
        )

    @property
    def hash(self):
        hashable = (
            self.__integration_name +
            self.__integration_method +
            self.__integration_type +
            self.__connection_type
        ).encode('utf-8')

        return hashlib.sha256(hashable).hexdigest()
