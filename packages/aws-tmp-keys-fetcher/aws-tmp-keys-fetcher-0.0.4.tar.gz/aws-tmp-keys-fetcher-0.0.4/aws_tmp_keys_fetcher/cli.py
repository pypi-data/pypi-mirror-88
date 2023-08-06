#! /usr/bin/env python3

"""
Working with AWS, you typically has access to an ever-growing number of accounts and it is 
not advisable to create (IAM) users plus associated access keys in each of them.

Hence, you either work with AWS SSO, federated authentication, or you work with a central landing
zone, and from there you assume roles in the account you want to work with.

However, some applications (in this case the Redshift JDBC driver) expects real access keys for
a particular profile, in order to make use of temporary database credentials.

A well beloved tool for [federated authentication](https://github.com/venth/aws-adfs) does
exist, but if you use native AWS authentication I couldn't find it.

This is a very simple tool that fetches temporary access keys for a particular profile and
stores them in your ~/.aws/credentials file. So run the command, and refer to your profile (followed by `-tmp`).
"""

# pylint: disable=broad-except,C0103,E0401,R0912,R0913,R0914,R0915,R1702,W0603,W1203

from __future__ import annotations
import sys
import os

import json
import click
import configparser
import boto3

from typing import Dict, List, Tuple, Optional, Any
from outdated import check_outdated # type: ignore

from . import __version__

@click.command()
@click.option(
    '--profile', '-p',
    help='Name of profile.',
    )
@click.option(
    '--show', '-s',
    help='Show credentials as export statements for setting environment variables. Default: False',
    is_flag=True,
    default=False
    )
@click.option(
    '--reset', '-r',
    help='Outputs commands for resetting environment variables. Default: False',
    is_flag=True,
    default=False
    )
@click.version_option(version=__version__)
def fetch_credentials(
        profile: string,
        show: bool,
        reset: bool,
    ) -> int:
    """
    Fetches temporary credentials for the given profile
    """

    check_latest_version()

    try:
        if reset:
            click.echo(f"unset AWS_ACCESS_KEY_ID")
            click.echo(f"unset AWS_SECRET_ACCESS_KEY")
            click.echo(f"unset AWS_SESSION_TOKEN")
        else:
            # first get the role from the profile file
            config = configparser.ConfigParser()
            config_file = f"{os.path.expanduser('~')}/.aws/config"
            config.read(config_file)
            role_arn = config[f"profile {profile}"]["role_arn"]
            source_profile = config[f"profile {profile}"]["source_profile"]
            if not show:
                click.echo(f"Use profile {profile} (sourced from {source_profile}) with role {role_arn}")

            # then assume the role
            os.environ['AWS_PROFILE'] = source_profile
            client = boto3.client('sts')

            # Do we have MFA?
            mfa_serial = None
            mfa_token = None
            try:
                mfa_serial = config[f"profile {profile}"]["mfa_serial"]
                mfa_token = input(f"Please enter MFA code for {mfa_serial}: ")
            except KeyError:
                if show:
                    click.echo("No MFA configuration detected")
                pass
            
            if mfa_serial:
                response = client.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName='session_for',
                    DurationSeconds=3600,
                    SerialNumber=mfa_serial,
                    TokenCode=mfa_token,
                )
            else:
                response = client.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName='session_for',
                    DurationSeconds=3600,
                )

            # Now write it back to the credentials file
            credentials_config = configparser.ConfigParser()
            credentials_file = f"{os.path.expanduser('~')}/.aws/credentials"
            credentials_config.read(credentials_file)
            tmp_profile = f"{profile}-tmp"
            credentials_config[tmp_profile] = {
                'aws_access_key_id': response['Credentials']['AccessKeyId'],
                'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
                'aws_session_token': response['Credentials']['SessionToken'],
            }
            with open(credentials_file, 'w') as credentials_config_file:
                credentials_config.write(credentials_config_file)

            if show:
                click.echo(f"export AWS_ACCESS_KEY_ID=#{response['Credentials']['AccessKeyId']}")
                click.echo(f"export AWS_SECRET_ACCESS_KEY=#{response['Credentials']['SecretAccessKey']}")
                click.echo(f"export AWS_SESSION_TOKEN=#{response['Credentials']['SessionToken']}")
            else:
                click.secho(
                    f"Temporary credentials written to {credentials_file} with profile {tmp_profile}",
                    fg="green"
                )
    except KeyError as ke:
        click.secho(f"Key error occured: {ke}", fg="red")
        click.secho(
            "Note: this tool assumes the 'role_arn', 'source_profile' and 'mfa_serial' to be present in your ~/.aws/config file.",
            fg="red"
        )
        raise
    except Exception as e:
        click.secho(f"Exception occured: {e}", fg="red")


def check_latest_version():
    # check for newer versions
    try:
        is_outdated, latest_version = check_outdated('aws-tmp-keys-fetcher', __version__)
        if is_outdated:
            click.echo(
                f'Your local version ({__version__}) is out of date! Latest is {latest_version}!'
            )
    except ValueError:
        # this happens when your local version is ahead of the pypi version,
        # which happens only in development
        pass
