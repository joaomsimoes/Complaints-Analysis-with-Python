export PROJECT_ID=YOUR-PROJECT
export REGION=YOUR-REGION
export CONNECTION_NAME=YOUR-CONNECTION-NAME
export SERVICE_NAME=CHOOSE-SERVICE-NAME
export IMAGE=gcr.io/$PROJECT_ID/$SERVICE_NAME

gcloud builds submit \
  --tag $IMAGE \
  --project $PROJECT_ID

gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --project $PROJECT_ID \
  --region $REGION \
  --allow-unauthenticated \
  --cpu 2 \
  --memory 2Gi \
  --add-cloudsql-instances $CONNECTION_NAME \
  --set-env-vars CLOUD_SQL_CONNECTION_NAME=$CONNECTION_NAME, \
    DB_USER=user, \
    DB_PASS=pass, \
    DB_NAME=db
