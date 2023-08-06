# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_tmp_keys_fetcher']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.22,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'configparser>=5.0.1,<6.0.0',
 'outdated>=0.2.0,<0.3.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['aws-tmp-keys-fetcher = '
                     'aws_tmp_keys_fetcher.cli:fetch_credentials']}

setup_kwargs = {
    'name': 'aws-tmp-keys-fetcher',
    'version': '0.0.4',
    'description': 'AWS temporary keys fetcher - simple command-line tool to fetch temporary aws credentials and stores them in your configs so that third party that require actual access keys can work with them.',
    'long_description': "# Fetching AWS IAM permissions\n\n## Introduction\nWorking with AWS, you typically has access to an ever-growing number of accounts and it is not advisable to create (IAM) users plus associated access keys in each of them.\n\nHence, you either work with AWS SSO, federated authentication, or you work with a central landing\nzone, and from there you assume roles in the account you want to work with.\n\nHowever, some applications (in this case the Redshift JDBC driver) expects real access keys for a particular profile, in order to make use of temporary database credentials.\n\nA well beloved tool for [federated authentication](https://github.com/venth/aws-adfs) does\nexist, but if you use native AWS authentication I couldn't find it.\n\nThis is a very simple tool that fetches temporary access keys for a particular profile and stores them in your ~/.aws/credentials file. So run the command, and refer to your profile (followed by `-tmp`).\n\n## Usage\n\nUsage is pretty simple, you need to know the (working!) aws profile name for which you want to fetch temporary credentials.\n\nThe `role_arn` is read from the profile and temporary credentials are retrieved, and written to `~/.aws/credentials` with the same profile name, followed by `-tmp`.\n\n```bash\n$ aws-tmp-keys-fetcher --profile my-profile\nUse profile my-profile with role arn:aws:iam::1111111111:role/MY_ROLE_NAME\nEnter MFA code for arn:aws:iam::0000000000000:mfa/pietje.puk:\nTemporary credentials written to /Users/pietjepuk/.aws/credentials with profile my-profile-tmp\n```\n\nIf you want to use the output to set environment variables, you can show the output and if desired use command substition to initialize your shell with it.\n\n```bash\n$ aws-tmp-keys-fetcher -p my-profile --show\nAWS_ACCESS_KEY_ID=XXXXXXXXXXXX\nAWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYY\nAWS_SESSION_TOKEN=ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\n\n# Use command substitution to load these values into your environment\n$ $(aws-tmp-keys-fetcher -p my-profile --show)\n\n$ env | grep -i aws\nAWS_ACCESS_KEY_ID=XXXXXXXXXXXX\nAWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYY\nAWS_SESSION_TOKEN=ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\n```\n\nor if you want to remove these credentials from your environment:\n\n```bash\n$ aws-tmp-keys-fetcher -p my-profile --reset\nunset AWS_ACCESS_KEY_ID\nunset AWS_SECRET_ACCESS_KEY\nunset AWS_SESSION_TOKEN\n\n$ $(aws-tmp-keys-fetcher -p my-profile --reset)\n```\n",
    'author': 'Gerco Grandia',
    'author_email': 'gerco.grandia@4synergy.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gercograndia/aws-tmp-keys-fetcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
