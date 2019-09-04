# 🗑🤖

Remind me to put out the trash. Also a chance to fool with Google Cloud Run.

## Deploy notes

Have to enable Cloud Run, Cloud Build, and Cloud Scheduler in the console, and
`gcloud components install beta` beforehand.

Then:

```bash
# Build and Deploy
gcloud builds submit --tag gcr.io/{PROJECT-ID}/trashbot
gcloud beta run deploy --image gcr.io/{PROJECT-ID}/trashbot \
                       --platform managed \
                       --no-allow-unauthenticated

# Set env vars
gcloud beta run services update trashbot \
    --platform managed \
    --update-env-vars TWILIO_ACCOUNT_SID=...,TWILIO_AUTH_TOKEN=...,TWILIO_FROM_NUMBER=...,SMS_RECIPIENTS=...

# Create a service account and give it access to run the app
gcloud iam service-accounts create scheduler --display name "gcloud scheduler"
gcloud beta run services add-iam-policy-binding trashbot \
    --member=serviceAccount:scheduler@{PROJECT-ID}.iam.gserviceaccount.com \
    --role=roles/run.invoker

gcloud beta scheduler jobs create http nightly \
    --schedule "0 20 * * *" \
    --http-method=GET \
    --time-zone="America/New_York" \
    --uri="{SERVICE-URL}/?sms" \
    --oidc-service-account-email=scheduler@{PROJECT-ID}.iam.gserviceaccount.com \
    --oidc-token-audience={SERVICE-URL}
```
