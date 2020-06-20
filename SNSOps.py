import boto3

def sendNotification( topicARN, messages ):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn= topicARN,
        Message= messages ,
        Subject='Cost alert from AWS',
        MessageStructure='string'
    )
