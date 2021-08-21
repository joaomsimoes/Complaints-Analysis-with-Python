export PROJECT_ID=portaldaqueixa-nlp
export REGION=europe-west1
export CONNECTION_NAME=portaldaqueixa-nlp:europe-west1:portaldaqueixa
export SERVICE_NAME=app-portaldaqueixa
export IMAGE=gcr.io/$PROJECT_ID/portaldaqueixa-app

gcloud builds submit \
  --tag $IMAGE \
  --project $PROJECT_ID

gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNECTION_NAME \
  --project $PROJECT_ID

gcloud beta run services update $SERVICE_NAME \
  --add-cloudsql-instances $CONNECTION_NAME
  --update-env-vars CLOUD_SQL_CONNECTION_NAME=$CONNECTION_NAME \
  --region $REGION \
  --update-secrets DB_USER=root:latest \
  --update-secrets DB_PASS=secretpassword:latest \
  --update-secrets DB_NAME=scrapper:latest