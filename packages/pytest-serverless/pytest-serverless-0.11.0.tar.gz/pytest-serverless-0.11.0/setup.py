# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_serverless']
install_requires = \
['boto3>=1.9,<2.0',
 'moto>=1.3,<2.0',
 'python-box>=5.2,<6.0',
 'pyyaml>=5.1,<6.0']

entry_points = \
{'pytest11': ['serverless = pytest_serverless']}

setup_kwargs = {
    'name': 'pytest-serverless',
    'version': '0.11.0',
    'description': 'Automatically mocks resources from serverless.yml in pytest using moto.',
    'long_description': 'pytest-serverless\n---\nAutomatically mocks resources from serverless.yml in pytest using moto.\n\n| master | PyPI | Python | pytest | Licence |\n| --- | --- | --- | --- | --- |\n| ![Master](https://github.com/whisller/pytest-serverless/workflows/Master/badge.svg) | [![PyPI](https://img.shields.io/pypi/v/pytest-serverless.svg)](https://pypi.org/project/pytest-serverless/) | ![](https://img.shields.io/pypi/pyversions/pytest-serverless.svg) | `6.2` | ![](https://img.shields.io/pypi/l/pytest-serverless.svg) |\n\n\n## Installation\n```sh\npip install pytest-serverless\n```\n\nYour project has to have `pytest` installed.\n\n## What problem it tries to solve?\nWhen building your project with [serverless](https://serverless.com/) most likely you will create\n[resources](https://serverless.com/framework/docs/providers/aws/guide/resources/) like dynamodb tables, sqs queues, sns topics.\n\nDuring writing tests you will have to mock those in [moto](https://github.com/spulec/moto). \n\nThis pytest plugin tries to automate this process by reading `serverless.yml` file and create\nmoto mocks of resources for you.\n\n## Usage\nAssuming your `serverless.yml` file looks like:\n```yaml\nservice: my-microservice\nresources:\n Resources:\n   TableA:\n     Type: \'AWS::DynamoDB::Table\'\n     DeletionPolicy: Delete\n     Properties:\n       TableName: ${self:service}.my-table\n       AttributeDefinitions:\n         - AttributeName: id\n           AttributeType: S\n         - AttributeName: company_id\n           AttributeType: S\n       KeySchema:\n         - AttributeName: id\n           KeyType: HASH\n       GlobalSecondaryIndexes:\n         - IndexName: company_id\n           KeySchema:\n             - AttributeName: company_id\n               KeyType: HASH\n           Projection:\n             ProjectionType: ALL\n           ProvisionedThroughput:\n             ReadCapacityUnits: 10\n             WriteCapacityUnits: 30\n       ProvisionedThroughput:\n         ReadCapacityUnits: 10\n         WriteCapacityUnits: 30\n```\n\nTo start using `my-microservice.my-table` table in your tests just mark your test with `@pytest.mark.usefixtures("serverless")`, and rest will be done by plugin.\n```python\nimport boto3\nimport pytest\n\n\n@pytest.mark.usefixtures("serverless")\ndef test():\n    table = boto3.resource("dynamodb").Table("my-microservice.my-table")\n    count_of_items = len(table.scan()["Items"])\n    assert count_of_items == 0\n```\n\n## Supported resources\n### AWS::DynamoDB::Table\n### AWS::SQS::Queue\n### AWS::SNS::Topic\n### AWS::S3::Bucket\n\n## Issues?\nPlugin is in early stage of development, so you might find some bugs or missing functionality.\n\nIf possible create pull request (with tests) that fixes particular problem.\n',
    'author': 'Daniel Ancuta',
    'author_email': 'whisller@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whisller/pytest-serverless',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
