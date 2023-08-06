# B.TwilioSdkLayer

An AWS CDK based lambda layer containing Twilio SDK for python.

### Description

This library is intended to simplify Twilio SDK dependency management
in AWS architectures where Twilio logic is being handled with lambda
functions. Simply include this layer when creating a lambda function
to enable Twilio functionality.

**NOTE!** In order to use this layer, a `docker` command must be available
on your machine. It is because the CDK runs a bundling command on a 
docker container to create the Twilio dependency.

### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science 
industry by sharing its IT knowledge with other companies and 
the community. This is an open source library intended to be used 
by anyone. Improvements and pull requests are welcome.

### Related technology

- Python 3
- AWS CDK
- Twilio

### Assumptions

The project assumes the following:

- You have basic-good knowledge in python programming.
- You have basic-good knowledge in AWS and AWS CDK.
- You have basic knowledge in Twilio.

### Useful sources

- Read more about Twilio SDK:<br>
https://www.twilio.com/docs/libraries/python

### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b_twilio_sdk_layer
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

Create a lambda function with this layer:
```python
from aws_cdk.aws_lambda import Function, Code, Runtime
from b_twilio_sdk_layer.layer import Layer as TwilioLayer

Function(
    scope=stack,
    id='MyCoolFunction',
    function_name='MyCoolFunction',
    code=Code.from_asset('/path/to/your/code'),
    handler='index.handler',
    runtime=Runtime.PYTHON_3_8,
    layers=[TwilioLayer(stack, 'MyCoolTwilioLayer')],
)
```

### Testing

The project currently has no tests.

### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us 
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.
