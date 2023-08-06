# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_export_credentials']

package_data = \
{'': ['*']}

install_requires = \
['botocore>=1.17']

entry_points = \
{'console_scripts': ['aws-export-credentials = aws_export_credentials:main']}

setup_kwargs = {
    'name': 'aws-export-credentials',
    'version': '0.4.0',
    'description': 'Get AWS credentials from a profile to inject into other programs',
    'long_description': '# aws-export-credentials\n**Get AWS credentials from a profile to inject into other programs**\n\nThere are a number of other projects that extract AWS credentials and/or\ninject them into programs, but all the ones I\'ve seen use the CLI\'s cache\nfiles directly, rather than leveraging botocore\'s ability to retrieve and\nrefresh credentials. So I wrote this to do that.\n\n[botocore (the underlying Python SDK library)](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html) has added support for loading credentials cached by [`aws sso login`](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sso/login.html) as of [version 1.17.0](https://github.com/boto/botocore/blob/develop/CHANGELOG.rst#1170).\n`aws-export-credentials` now requires botocore >= 1.17.0, and so supports AWS SSO credentials as well.\nIf all you want is AWS SSO support for an SDK other than Python, take a look at [aws-sso-credential-process](https://github.com/benkehoe/aws-sso-credential-process), which doesn\'t require the credential injection process that `aws-export-credentials` does.\n\n## Quickstart\n\nI recommend you install [`pipx`](https://pipxproject.github.io/pipx/), which installs the tool in an isolated virtualenv while linking the script you need.\n\n```bash\n# with pipx\npipx install aws-export-credentials\n\n# without pipx\npython3 -m pip install --user aws-export-credentials\n\n# run it\naws-export-credentials\n{\n  "Version": 1,\n  "AccessKeyId": "<your access key here>",\n  "SecretAccessKey": "<shhh it\'s your secret key>",\n  "SessionToken": "<do you ever wonder what\'s inside the session token?>"\n}\n```\n\n## Usage\n### Profile\nProfiles work like in the AWS CLI (since it uses botocore); it will pick up the `AWS_PROFILE`\nor `AWS_DEFAULT_PROFILE` env vars, but the `--profile` argument takes precedence.\n\n### JSON\n```\naws-export-credentials --profile my-profile --json [--pretty]\n```\nPrint the credentials to stdout as a JSON object compatible with the `credential_process`\nspec. If `--pretty` is added, it\'ll be pretty-printed.\n\n### Env vars\n```\naws-export-credentials --profile my-profile --env\neval $(aws-export-credentials --profile my-profile --env-export)\n```\nPrint the credentials as environment variables. With `--env-export`, the lines are prefixed\nby "`export `", suitable for eval-ing into your shell.\n\n### Exec wrapper\n```\naws-export-credentials --profile my-profile --exec echo \'my access key id is $AWS_ACCESS_KEY_ID\'\n```\nExecute the arguments after `--exec` using `os.system()`, injecting the credentials through\nenvironment variables.\n',
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/aws-export-credentials',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
