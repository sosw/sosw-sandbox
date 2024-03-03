import boto3
def list_users():

    client = boto3.client('iam')
    response = client.list_users()
    users = response.get('Users')
    for user in users:
        print(user)

if __name__ == '__main__':
    list_users()