#!/bin/bash
# Script to update API endpoint in static UI before deployment

if [ -z "$1" ]; then
    echo "Usage: ./update-api-endpoint.sh <API_ENDPOINT_URL>"
    exit 1
fi

API_ENDPOINT=$1

echo "Updating API endpoint to: $API_ENDPOINT"

# Update config.js with the actual API endpoint
sed -i.bak "s|API_ENDPOINT_PLACEHOLDER|$API_ENDPOINT|g" static-ui/js/config.js

echo "API endpoint updated successfully"
