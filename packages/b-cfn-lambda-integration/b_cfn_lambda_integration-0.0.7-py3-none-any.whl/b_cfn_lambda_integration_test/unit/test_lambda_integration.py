from aws_cdk.aws_apigatewayv2 import CfnApi
from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk.core import Stack, App

from b_cfn_lambda_integration.lambda_integration import LambdaIntegration


def test_FUNC_hash_WITH_valid_parameters_EXPECT_hash_created():
    """
    Test that hashing is consistent and works as expected.

    :return: No return.
    """
    stack = Stack(App(), 'TestStack')

    integration = LambdaIntegration(
        scope=stack,
        integration_name='TestIntegration',
        api=CfnApi(stack, 'TestApi'),
        lambda_function=Function(
            stack,
            'TestLambdaFunction',
            code=Code.from_inline('def handler(*args, **kwargs): return 123'),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_6
        )
    )

    assert integration.hash == 'ab93cecc508e529c3791ba48a1275deec88cdd6b43a7e1d443906df48fa300e4'
