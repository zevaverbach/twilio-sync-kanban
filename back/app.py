import os

from dotenv import load_dotenv, find_dotenv
from faker import Faker
from flask import Flask, jsonify, request
from flask_cors import CORS
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant

app = Flask(__name__)
CORS(app)

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)
fake = Faker()


@app.route("/token")
def randomToken():
    identity = fake.user_name()
    token = AccessToken(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_API_KEY"],
        os.environ["TWILIO_API_SECRET"],
    )
    token.identity = identity

    sync_grant = SyncGrant(service_sid=os.environ["TWILIO_SYNC_SERVICE_SID"])
    token.add_grant(sync_grant)
    token = token.to_jwt().decode("utf-8")
    return jsonify(identity=identity, token=token)


def provision_sync_default_service():
    client = Client(
        os.environ["TWILIO_API_KEY"],
        os.environ["TWILIO_API_SECRET"],
        os.environ["TWILIO_ACCOUNT_SID"],
    )
    client.sync.services("default").fetch()


if __name__ == "__main__":
    provision_sync_default_service()
    app.run(debug=True, host="0.0.0.0", port=5001)

