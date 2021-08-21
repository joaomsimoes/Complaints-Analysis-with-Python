export PROJECT_ID=portaldaqueixa-nlp
export REGION=europe-west1
export CONNECTION_NAME=portaldaqueixa-nlp:europe-west1:portaldaqueixa
export SERVICE_NAME=app-portaldaqueixa
export IMAGE=gcr.io/$PROJECT_ID/$SERVICE_NAME

gcloud builds submit \
  --tag $IMAGE \
  --project $PROJECT_ID

gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --project $PROJECT_ID \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNECTION_NAME \
  --set-env-vars CLOUD_SQL_CONNECTION_NAME=$CONNECTION_NAME \
  --set-env-vars DB_USER="root" \
  --set-env-vars DB_PASS="secretpassword" \
  --set-env-vars DB_NAME="scrapper"