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


@app.route('/webhook')
def webhook():
    req = request.get_json(silent=True, force=True)
    print ("r>>",req)
    print("Request:")
    # req="What have hemophilia?"
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)
    print ("ffff>>>",res)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Range'] = 'application/json'
    print ("rt>>>",r)
    return r

def makeWebhookResult(req):
    print ("I am in")
    print('m in>>',req)
    if req.get("result").get("action") != "AHemophiliaHemophilia":
        return {}
    result = req.get("result")
    print ("result>>>",result)
    parameters = result.get("parameters")
    zone = parameters.get("qt")
    # For a Boto3 client.
    ddb = boto3.client('dynamodb', aws_access_key_id='AKIAJ7DUJKCSBGJZHUCQ', aws_secret_access_key='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', region_name='us-east-2')
    response = ddb.list_tables()

    # For a Boto3 service resource
    dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIAJ7DUJKCSBGJZHUCQ', aws_secret_access_key='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', region_name='us-east-2')

    table = dynamodb.Table('medical_qa_details')
    response = table.scan(
        FilterExpression=Attr('questions').eq(zone))

    speech = response['Items'][0]['answers']
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "medical"
    }

if __name__ == '__main__':
    # app.run()
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
    app.run(debug=True, port=port, host='0.0.0.0')