# Fetching AWS IAM permissions

## Introduction
Working with AWS, you typically has access to an ever-growing number of accounts and it is not advisable to create (IAM) users plus associated access keys in each of them.

Hence, you either work with AWS SSO, federated authentication, or you work with a central landing
zone, and from there you assume roles in the account you want to work with.

However, some applications (in this case the Redshift JDBC driver) expects real access keys for a particular profile, in order to make use of temporary database credentials.

A well beloved tool for [federated authentication](https://github.com/venth/aws-adfs) does
exist, but if you use native AWS authentication I couldn't find it.

This is a very simple tool that fetches temporary access keys for a particular profile and stores them in your ~/.aws/credentials file. So run the command, and refer to your profile (followed by `-tmp`).
