import urllib
import json
import os
from boto3 import dynamodb
import boto3.dynamodb.table
from boto3.dynamodb.conditions import Key, Attr

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST','GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print "jell>>",r
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "AHemophiliaHemophilia":
        return {}
    result = req.get("result")
    # parameters = result.get("parameters")
    # zone = parameters.get("qt")
    # For a Boto3 client.
    ddb = boto3.client('dynamodb', aws_access_key_id='AKIAJ7DUJKCSBGJZHUCQ', aws_secret_access_key='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', region_name='us-east-2')
    response = ddb.list_tables()

    # For a Boto3 service resource
    dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIAJ7DUJKCSBGJZHUCQ', aws_secret_access_key='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', region_name='us-east-2')

    table = dynamodb.Table('medical_qa_details')
    response = table.scan(
        FilterExpression=Attr('questions').eq(result))
    speech = response['Items'][0]['answers']
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "MedicalDisease"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
    app.run(debug=True, port=port, host='0.0.0.0')
    r = webhook()
    makeWebhookResult(r)