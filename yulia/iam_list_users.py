import boto3
def list_users():
    # aws_secret_key_id = 'AKIA3FLD3H6BTCH4QUN4'
    # aws_secret_access_key = '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'

    client = boto3.client('iam')
    response = client.list_users()
    users = response.get('Users')
    for user in users:
        print(user)

if __name__ == '__main__':
    list_users()