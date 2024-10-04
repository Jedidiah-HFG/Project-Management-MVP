#!/bin/bash
# Purpose: To deploy the App to Cloud Run.

# Google Cloud Project ID
PROJECT=extreme-braid-436615-h5

# Google Cloud Region
LOCATION=us-east1

# Deploy app from source code
gcloud run deploy streamlit-app --source . --region=$LOCATION --project=$PROJECT --allow-unauthenticated