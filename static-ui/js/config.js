// Configuration
// Update this when deploying to point to the API endpoint
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'API_ENDPOINT_PLACEHOLDER'; // This will be replaced during CDK deployment
