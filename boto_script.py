from datetime import datetime, timedelta, timezone

import boto3
import click

client = boto3.client('iam')
iam = boto3.resource('iam')


@click.group()
def cli():
    click.echo("Would Access AWS in Minute")


@cli.command()
@click.option('username',
              '--username',
              '-u',
              default='none',
              help='check a user or all users')
@click.option('age',
              '--age',
              '-a',
              default=90,
              help='the lowest age for access key(in days)')
def start(username: str, age: int):
    picked_keys = []
    if username == 'none':
        users = client.list_users()
        users = users['Users']
        for user in users:
            keys_response = client.list_access_keys(UserName=user['UserName'])
            user_keys = keys_response['AccessKeyMetadata']
            for key in user_keys:
                if datetime.now(timezone.utc) - key['CreateDate'] <= timedelta(
                        days=age):
                    key_dict = {
                        'user_name': key['UserName'],
                        'access_key_id': key['AccessKeyId']
                    }
                    picked_keys.append(key_dict)
        delete_keys(picked_keys)

    else:
        keys_response = client.list_access_keys(UserName=username)
        user_keys = keys_response['AccessKeyMetadata']
        for key in user_keys:
            if datetime.now(timezone.utc) - key['CreateDate'] <= timedelta(
                    days=age):
                key_dict = {
                    'user_name': key['UserName'],
                    'access_key_id': key['AccessKeyId']
                }
                picked_keys.append(key_dict)
        delete_keys(picked_keys)

    keys = len(picked_keys)
    click.echo(f"{keys} Access Key(s) Deleted")


def delete_keys(keys):
    for key in keys:
        access_key = iam.AccessKey(key['user_name'], key['access_key_id'])
        access_key.delete()
    click.echo("Sucessful Deleted")


if __name__ == "__main__":
    cli()
