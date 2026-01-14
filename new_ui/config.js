// API Configuration
// This file can be updated after deployment to point to the correct API endpoint
window.RIAM_CONFIG = {
    // For local development, use localhost
    // For production, this will be replaced with the actual API URL
    apiBaseUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : 'https://your-api-url-here.com', // Update this after CDK deployment
};
