#!/usr/bin/python3
#
# aws-sso-cred-restore --profile <profile> [--export]
#
# This script restore credential file using AWS SSO command from aws cli version 2
#
# This script is intended to plug a (hopefully temporary) gap in the official aws2 tool. As such, it
# makes certain assumptions about the cache file and does not rely on boto3 because the aws2 tool
# packages a dev version.
#
# Copyright (c) 2020 Clayton Silva | Pagar.me , inspired in source from Linaro Ltd


import argparse
import configparser
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone


def process_arguments():
    """ Check and extract arguments provided. """
    parser = argparse.ArgumentParser(allow_abbrev=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--export", action="store_true")
    parser.add_argument("--profile", action="store", required=False)
    args = parser.parse_args()
    return args


def retrieve_attribute(profile, tag):
    """ Safely find and return the desired attribute from the AWS Config profile. """
    if tag not in profile:
        sys.exit("'%s' not in '%s' profile" % (tag, profile))
    return profile[tag]


def set_attribute(config, profile_name, tag, value):
    """ Safely find and set the desired attribute from the AWS profile credentials. """
    # Set Values in file in defined section
    config.set(profile_name, tag, "%s" % value)


def retrieve_all_profiles():
    config_path = os.path.abspath(os.path.expanduser("~/.aws/config"))
    config = configparser.ConfigParser()
    config.read(config_path)
    return map(lambda item: item.replace('profile ', ''), config.sections())


def retrieve_profile(profile_name):
    """ Find the AWS Config profile matching the specified profile name. """
    config_path = os.path.abspath(os.path.expanduser("~/.aws/config"))
    config = configparser.ConfigParser()
    config.read(config_path)
    # Look for the required profile
    if "profile %s" % profile_name not in config:
        sys.exit("Cannot find profile '%s' in ~/.aws/config" % profile_name)
    # Retrieve the values
    profile = config["profile %s" % profile_name]
    sso_start_url = retrieve_attribute(profile, "sso_start_url")
    sso_region = retrieve_attribute(profile, "sso_region")
    sso_account_id = retrieve_attribute(profile, "sso_account_id")
    sso_role_name = retrieve_attribute(profile, "sso_role_name")
    return sso_start_url, sso_region, sso_account_id, sso_role_name


def refresh_profile_credentials(profile_name, access_key, secret_access_key, session_token):
    """ Find the AWS Config credentials matching the specified profile name. """
    config_path = os.path.abspath(os.path.expanduser("~/.aws/credentials"))
    config = configparser.ConfigParser()
    config.read(config_path)
    # create section in creds if not exist
    if profile_name not in config.sections():
        config.add_section(profile_name)
    set_attribute(config, profile_name, "aws_access_key_id", access_key)
    set_attribute(config, profile_name,
                  "aws_secret_access_key", secret_access_key)
    set_attribute(config, profile_name, "aws_session_token", session_token)
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def retrieve_token_from_file(filename, sso_start_url, sso_region):
    """ Check specified file and, if valid, return the access token. """
    with open(filename, "r") as json_file:
        blob = json.load(json_file)
    if ("startUrl" not in blob or
            blob["startUrl"] != sso_start_url or
            "region" not in blob or
            blob["region"] != sso_region):
        return None
    expires_at = blob["expiresAt"]
    # This will be a string like "2020-03-26T13:28:35UTC"
    expire_datetime = datetime.strptime(
        expires_at.replace("UTC", "+0000"), "%Y-%m-%dT%H:%M:%S%z")
    if expire_datetime < datetime.now(timezone.utc):
        # This has expired
        return None
    # Everything looks OK ...
    return blob["accessToken"]


def retrieve_token(sso_start_url, sso_region, profile_name):
    """ Get the access token back from the SSO cache. """
    # Check each of the files in ~/.aws/sso/cache looking for one that references
    # the specific SSO URL and region. If found then check the expiration.
    cachedir_path = os.path.abspath(os.path.expanduser("~/.aws/sso/cache"))
    cachedir = pathlib.Path(cachedir_path)
    for cachefile in cachedir.iterdir():
        token = retrieve_token_from_file(cachefile, sso_start_url, sso_region)
        if token is not None:
            return token
    sys.exit("Please login with 'aws sso login --profile=%s'" % profile_name)


def get_role_credentials(profile_name, sso_role_name, sso_account_id, sso_access_token, sso_region):
    """ Get the role credentials. """
    # We call the aws2 CLI tool rather than trying to use boto3 because the latter is
    # currently a special version and this script is trying to avoid needing any extra
    # packages.
    result = subprocess.run(
        [
            "aws", "sso", "get-role-credentials",
            "--profile", profile_name,
            "--role-name", sso_role_name,
            "--account-id", sso_account_id,
            "--access-token", sso_access_token,
            "--region", sso_region,
            "--output", "json"
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    if result.returncode != 0:
        print(result.stderr.decode(), file=sys.stderr)
        sys.exit("Please login with 'aws sso login --profile=%s'" %
                 profile_name)

    output = result.stdout
    blob = json.loads(output)
    access_key = blob["roleCredentials"]["accessKeyId"]
    secret_access_key = blob["roleCredentials"]["secretAccessKey"]
    session_token = blob["roleCredentials"]["sessionToken"]
    return access_key, secret_access_key, session_token


def process_profile(profile, export):
    sso_start_url, sso_region, sso_account_id, sso_role_name = retrieve_profile(
        profile)
    sso_access_token = retrieve_token(sso_start_url, sso_region, profile)
    access_key, secret_access_key, session_token = get_role_credentials(
        profile,
        sso_role_name,
        sso_account_id,
        sso_access_token,
        sso_region)

    print("parsing creds file for profile %s" % profile)
    refresh_profile_credentials(
        profile, access_key, secret_access_key, session_token)
    if export:
        print("export AWS_ACCESS_KEY_ID=\"%s\"" % access_key)
        print("export AWS_SECRET_ACCESS_KEY=\"%s\"" %
              secret_access_key)
        print("export AWS_SESSION_TOKEN=\"%s\"" % session_token)


def main():
    """ Main! """
    args = process_arguments()
    all_profiles = retrieve_all_profiles()
    if not args.profile:
        for profile in all_profiles:
            process_profile(profile, args.export)
    else:
        for profile in filter(lambda k: args.profile in k, all_profiles):
            process_profile(profile, args.export)


if __name__ == '__main__':
    main()
