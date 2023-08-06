# Fetching AWS IAM permissions

## Introduction
Working with AWS, you typically has access to an ever-growing number of accounts and it is not advisable to create (IAM) users plus associated access keys in each of them.

Hence, you either work with AWS SSO, federated authentication, or you work with a central landing
zone, and from there you assume roles in the account you want to work with.

However, some applications (in this case the Redshift JDBC driver) expects real access keys for a particular profile, in order to make use of temporary database credentials.

A well beloved tool for [federated authentication](https://github.com/venth/aws-adfs) does
exist, but if you use native AWS authentication I couldn't find it.

This is a very simple tool that fetches temporary access keys for a particular profile and stores them in your ~/.aws/credentials file. So run the command, and refer to your profile (followed by `-tmp`).

## Usage

Usage is pretty simple, you need to know the (working!) aws profile name for which you want to fetch temporary credentials.

The `role_arn` is read from the profile and temporary credentials are retrieved, and written to `~/.aws/credentials` with the same profile name, followed by `-tmp`.

```bash
$ aws-tmp-keys-fetcher --profile my-profile
Use profile my-profile with role arn:aws:iam::1111111111:role/MY_ROLE_NAME
Enter MFA code for arn:aws:iam::0000000000000:mfa/pietje.puk:
Temporary credentials written to /Users/pietjepuk/.aws/credentials with profile my-profile-tmp
```

If you want to use the output to set environment variables, you can show the output and if desired use command substition to initialize your shell with it.

```bash
$ aws-tmp-keys-fetcher -p my-profile --show
AWS_ACCESS_KEY_ID=XXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYY
AWS_SESSION_TOKEN=ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ

# Use command substitution to load these values into your environment
$ $(aws-tmp-keys-fetcher -p my-profile --show)

$ env | grep -i aws
AWS_ACCESS_KEY_ID=XXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYY
AWS_SESSION_TOKEN=ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
```

or if you want to remove these credentials from your environment:

```bash
$ aws-tmp-keys-fetcher -p my-profile --reset
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN

$ $(aws-tmp-keys-fetcher -p my-profile --reset)
```
