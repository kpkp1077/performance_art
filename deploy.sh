#!/bin/bash

# QuotaPath Deployment Script for Google App Engine

echo "🚀 Starting QuotaPath deployment to Google App Engine..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 &> /dev/null; then
    echo "❌ You are not authenticated with Google Cloud. Please run:"
    echo "gcloud auth login"
    exit 1
fi

# Check if project is set
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No Google Cloud project is set. Please run:"
    echo "gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📁 Project ID: $PROJECT_ID"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations (if using Cloud SQL)
echo "🗄️ Running database migrations..."
python manage.py migrate

# Deploy to App Engine
echo "🌐 Deploying to Google App Engine..."
gcloud app deploy app.yaml --quiet

# Get the deployed URL
echo "✅ Deployment complete!"
echo "🔗 Your application is available at:"
gcloud app browse --no-launch-browser

echo ""
echo "📋 Post-deployment steps:"
echo "1. Update your frontend API URL to point to the deployed backend"
echo "2. Configure your Cloud SQL database connection"
echo "3. Set up Cloud Memorystore for Redis"
echo "4. Update CORS settings in production settings"
echo "5. Configure your custom domain (if needed)"

echo ""
echo "🔧 Useful commands:"
echo "  View logs: gcloud app logs tail -s default"
echo "  Open in browser: gcloud app browse"
echo "  Check versions: gcloud app versions list"