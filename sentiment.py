import os, requests, uuid, json
from config import TEXT_ANALYTICS_SUBSCRIPTION_KEY


# Don't forget to replace with your Cog Services subscription key!
subscription_key = TEXT_ANALYTICS_SUBSCRIPTION_KEY

# subscription_key = 'YOUR_TEXT_ANALYTICS_SUBSCRIPTION_KEY'

# Our Flask route will supply four arguments: input_text, input_language,
# output_text, output_language.
# When the run sentiment analysis button is pressed in our Flask app,
# the Ajax request will grab these values from our web app, and use them
# in the request. See main.js for Ajax calls.

def get_sentiment(input_text, input_language):
    base_url = 'https://australiaeast.api.cognitive.microsoft.com/text/analytics'
    path = '/v2.0/sentiment'
    constructed_url = base_url + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': 'AustraliaEast',
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = {
        'documents': [
            {
                'language': input_language,
                'id': '1',
                'text': input_text
            }
        ]
    }
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()
