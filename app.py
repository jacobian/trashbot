import arrow
import ics
import requests
import dateparser
import flask
import dotenv
import twilio.rest
import os

dotenv.load_dotenv()
app = flask.Flask(__name__)

URL = "http://cal.my-waste.mobi/admin/calendars/561-BLAC-collection-426-S2337-collection-427-S3288-collection-430-S2360-collection-433-S2364.ics"


@app.route("/", defaults={"when": "tomorrow"})
@app.route("/<when>")
def index(when):
    date = arrow.get(dateparser.parse(when))
    cal = ics.Calendar(requests.get(URL).text)
    messages = [event.name.lower() for event in cal.timeline.on(date)]
    message = f"🗑🤖 {when.title()} is {', '.join(messages)}" if messages else ""

    response = {"date": date.date(), "when": when, "message": message}

    if message and "sms" in flask.request.args:
        client = twilio.rest.Client(
            username=os.getenv("TWILIO_ACCOUNT_SID"),
            password=os.getenv("TWILIO_AUTH_TOKEN"),
        )

        sids = []
        for recipient in os.getenv("SMS_RECIPIENTS").split(","):
            m = client.messages.create(
                to=recipient, from_=os.getenv("TWILIO_FROM_NUMBER"), body=message
            )
            sids.append(m.sid)
        response["status"] = "sms sent"
        response["sids"] = sids

    elif message:
        response["status"] = "testing"

    else:
        response["status"] = "no messages"

    return flask.jsonify(response)
