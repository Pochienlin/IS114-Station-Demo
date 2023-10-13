from twilio.rest import Client
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

# set your api key in the .env file
load_dotenv()
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
print(auth_token, account_sid)
client = Client(account_sid, auth_token)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/sendSMS', methods=['POST'])
def sendSMS():
    data = request.get_json()
    message = data.get('message')
    phone_number = data.get('phone_number')
    print(message,phone_number)
    message = client.messages.create(
        from_='+12052933454',
        body=message,
        to='+65'+ str(phone_number)
    )
    return message.sid

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)