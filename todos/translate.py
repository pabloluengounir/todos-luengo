import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    client = boto3.client('comprehend')    
    translate = boto3.client(service_name='translate', region_name='region', use_ssl=True)

    # fetch todo from the database
    item = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    scores = client.detect_dominant_language(
        Text=item
    )
    
    result = translate.translate_text(Text=item['text'], 
        SourceLanguageCode=scores.Languages[0].LanguageCode, 
        TargetLanguageCode=event['pathParameters']['toLanguage'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result.get('TranslatedText'),
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
