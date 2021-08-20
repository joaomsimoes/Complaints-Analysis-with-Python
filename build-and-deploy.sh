#! /bin/bash

export PROJECT_ID=portaldaqueixa-nlp
export REGION=europe-west1
export CONNECTION_NAME=portaldaqueixa-nlp:europe-west1:portaldaqueixa

gcloud builds submit \
  --tag gcr.io/$PROJECT_ID/portaldaqueixa \
  --project $PROJECT_ID

gcloud run deploy poll \
  --image gcr.io/$PROJECT_ID/portaldaqueixa \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNECTION_NAME \
  --project $PROJECT_ID